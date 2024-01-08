import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions
from apache_beam.transforms.window import FixedWindows
from apache_beam.io import WriteToBigQuery
import os
import sys
import argparse
from google.auth import exceptions
from pathlib import Path
import logging
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from credentials import BIGQUERY_NETWORK_RENDERS, BIGQUERY_FEATURE_SELECTIONS, NETWORK_TOPIC_SUB, FEATURE_TOPIC_SUB, GOOGLE_CLOUD_PROJECT_ID, STAGING_LOCATION, TEMP_LOCATION

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

# Define pipeline options
def get_pipeline_options():
    options = PipelineOptions(
        runner='DirectRunner', #DataflowRunner when running job in server
        streaming = True,
        
    )
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = GOOGLE_CLOUD_PROJECT_ID
    google_cloud_options.staging_location = STAGING_LOCATION
    google_cloud_options.temp_location = TEMP_LOCATION
    google_cloud_options.region = 'us-west1'
    google_cloud_options.job_name = 'features-kpi-job-new'

    return google_cloud_options
    
# Define your pipeline
def run_pipeline(argv=None):
    google_cloud_options = get_pipeline_options()
    
    with beam.Pipeline(options=google_cloud_options) as pipeline:
        # Extract: Read from Pub/Sub topic, use subscriber                                                                       
        feature_messages = (
            pipeline
            | 'ReadFeatureSub' >> beam.io.ReadFromPubSub(subscription=FEATURE_TOPIC_SUB,
                                                        with_attributes=True)
            | 'Apply Windowing to Feature Messages' >> beam.WindowInto(FixedWindows(5))  # 86400 seconds = 1 day
        )
        
        # Transform: Count all instances of feature selections by feature and date
        # -> transform data to fit into output schema
        feature_count = (
            feature_messages
            | "CountFeatureElements" >> beam.ParDo(CountElements())
            | "GroupNetworkByFeature" >> beam.GroupByKey() # Group count by date
            | "FeatureCount" >> beam.Map(lambda count_elements_output: (count_elements_output[0], sum(count_elements_output[1])))
            | "SerializeToOutputSchema" >> beam.ParDo(ParseElements())            
        )
        
        # Load
        feature_count | "WriteNetworkToBigQuery" >> beam.io.WriteToBigQuery(
                    BIGQUERY_FEATURE_SELECTIONS,
                    schema='date:string,feature:string,count:integer',
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                    additional_bq_parameters={
                        'timePartitioning': {
                        'type': 'DAY',  # Adjust based on your desired partitioning
                        'field': 'date'  # Specify the key column as a string
                        },
                        'clustering': {
                            'fields': ['feature']
                        }
                    }
        )
        
    # Run the pipeline using the DataflowRunner
    result = pipeline.run()
    result.wait_until_finish()
    
class CountElements(beam.DoFn):
    
    def process(self, element):
        attributes = element.attributes
        date = attributes['date']
        feature = attributes['feature']
        yield (date, feature), 1
        
class ParseElements(beam.DoFn):
    
    def process(self, element):
        serialized_data = {
            'date': element[0][0],
            'feature': element[0][1],
            'count': element[1],
        }
        yield serialized_data

if __name__ == '__main__':
  run_pipeline()

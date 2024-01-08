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
    google_cloud_options.job_name = 'network-report-job-new'

    return google_cloud_options
    
# Define your pipeline
def run_pipeline(argv=None):
    google_cloud_options = get_pipeline_options()
    
    with beam.Pipeline(options=google_cloud_options) as pipeline:
        # Extract: Read from BigQuery source
        network_renders_source = (
            pipeline
            | 'Read Daily Network Count' >> beam.io.Read(
                beam.io.BigQuerySource(
                    query="""SELECT date, count FROM `spotifynetwork.spotifynetwork_data.network_renders`""",
                    use_standard_sql=True
                )
            )
        )                                                             
        
        # Transform: Count all instances of network selections by timeframe and date
        # -> transform data to fit into output schema
        network_reports = (
            network_renders_source
            | "CountNetworkElements" >> beam.ParDo(CountElements())
            # | "GroupNetworkByTimeframe" >> beam.GroupByKey() # Group count by date
            # | "NetworkCount" >> beam.Map(lambda count_elements_output: (count_elements_output[0], sum(count_elements_output[1])))
            # | "SerializeToOutputSchema" >> beam.ParDo(ParseElements())            
        )
        
        # Load
        # network_count | "WriteNetworkToBigQuery" >> beam.io.WriteToBigQuery(
        #             BIGQUERY_NETWORK_RENDERS,
        #             schema='date:string,timeframe:string,count:integer',
        #             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        #             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
                
    # Run the pipeline using the DataflowRunner
    result = pipeline.run()
    result.wait_until_finish()
    
class CountElements(beam.DoFn):
    
    def process(self, element):
        print(f"Received message: {element}")
        yield element
        
class ParseElements(beam.DoFn):
    
    def process(self, element):
        serialized_data = {
            'date': element[0][0],
            'timeframe': element[0][1],
            'count': element[1],
        }
        yield serialized_data

if __name__ == '__main__':
  run_pipeline()

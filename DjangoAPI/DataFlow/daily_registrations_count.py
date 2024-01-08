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
from credentials import BIGQUERY_REGISTRATIONS, REGISTER_TOPIC_SUB, GOOGLE_CLOUD_PROJECT_ID, STAGING_LOCATION, TEMP_LOCATION

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
    google_cloud_options.job_name = 'signup-kpi-job-new'

    return google_cloud_options
    
# Define your pipeline
def run_pipeline(argv=None):
    google_cloud_options = get_pipeline_options()
    
    with beam.Pipeline(options=google_cloud_options) as pipeline:
        # Extract: Read from Pub/Sub topic, use subscriber
        signup_messages = (
            pipeline
            | 'ReadSignupSub' >> beam.io.ReadFromPubSub(subscription=REGISTER_TOPIC_SUB,
                                                        with_attributes=True)
            | 'Apply Windowing to Signup Messages' >> beam.WindowInto(FixedWindows(5))  # PRODUCTION: 86400 seconds = 1 day  
        )                                                                                # TESTING: 5 seconds
        
        # Transform: Count all instances of registrations
        # -> transform data to fit into output schema
        signup_count = (
            signup_messages
            | "CountSignupElements" >> beam.ParDo(CountElements())
            | "GroupSignupByDate" >> beam.GroupByKey() # Group count by date
            | "SignupCount" >> beam.Map(lambda count_elements_output: (count_elements_output[0], sum(count_elements_output[1])))
            | "SerializeToOutputSchema" >> beam.ParDo(ParseElements())            
        )
        
        # Load
        signup_count | "WriteSignupsToBigQuery" >> beam.io.WriteToBigQuery(
                    BIGQUERY_REGISTRATIONS,
                    schema='date:string,count:integer',
                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
                
    # Run the pipeline using the DataflowRunner
    result = pipeline.run()
    result.wait_until_finish()
    
class CountElements(beam.DoFn):
    
    def process(self, element):
        attributes = element.attributes
        date = attributes['date']
        yield date, 1
        
class ParseElements(beam.DoFn):
    
    def process(self, element):
        serialized_data = {
            'date': element[0][0],
            'count': element[1],
        }
        yield serialized_data

if __name__ == '__main__':
  run_pipeline()

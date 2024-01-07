import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions
from datetime import datetime
from apache_beam.transforms.window import FixedWindows
import os
import sys
import argparse
from google.auth import exceptions
from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from credentials import LOGIN_TOPIC_SUB, REGISTER_TOPIC_SUB, GOOGLE_CLOUD_PROJECT_ID, STAGING_LOCATION, TEMP_LOCATION
        
# Define pipeline options
def get_pipeline_options():
    options = PipelineOptions(
        runner='DataflowRunner',
        streaming = True
    )
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = GOOGLE_CLOUD_PROJECT_ID
    google_cloud_options.staging_location = STAGING_LOCATION
    google_cloud_options.temp_location = TEMP_LOCATION
    google_cloud_options.region = 'us-west1'
    google_cloud_options.job_name = 'kpi-users-job-1'

    return google_cloud_options
    
# Define your pipeline
def run_pipeline(argv=None):
    google_cloud_options = get_pipeline_options()
    
    with beam.Pipeline(options=google_cloud_options) as pipeline:
        # Extract: Read from Pub/Sub topic, use subscriber
        login_messages = (
            pipeline
            | 'ReadLoginSub' >> beam.io.ReadFromPubSub(subscription=LOGIN_TOPIC_SUB, timestamp_attribute='publish_time',
                                                        with_attributes=True)
            | 'Apply Windowing to Login Messages' >> beam.WindowInto(FixedWindows(86400))  # 86400 seconds = 1 day
        )
        
        register_messages = (
            pipeline
            | 'ReadRegisterSub' >> beam.io.ReadFromPubSub(subscription=REGISTER_TOPIC_SUB, timestamp_attribute='publish_time',
                                                        with_attributes=True)
            | 'Apply Windowing to Register Messages' >> beam.WindowInto(FixedWindows(86400))  # 86400 seconds = 1 day
        )
        
        # Transform: Count all instances of logins and registrations
        daily_login_count = (
            login_messages
            | "CountLoginElements" >> beam.ParDo(CountElements())
            | "GroupLoginByDate" >> beam.GroupByKey() # Group count by date
            | "LoginCount" >> beam.Map(lambda count_elements_output: (count_elements_output[0], sum(count_elements_output[1])))         
        )
        
        daily_regiser_count = (
            register_messages
            | "CountRegisterElements" >> beam.ParDo(CountElements())
            | "GroupRegisterByDate" >> beam.GroupByKey() # Group count by date
            | "RegisterCount" >> beam.Map(lambda count_elements_output: (count_elements_output[0], sum(count_elements_output[1])))         
        )
        
        # Load
        daily_login_count | "PrintDailyLogin" >> beam.Map(print)
        daily_regiser_count | "PrintDailyRegistrations" >> beam.Map(print)
        
    # Run the pipeline using the DataflowRunner
    result = pipeline.run()
    result.wait_until_finish()
        
class CountElements(beam.DoFn):
    def process(self, element):
        publish_time = element.publishTime
        date = datetime.strptime(publish_time, '%Y-%m-%d').date()
        yield date, 1
        
class CountElementsTest(beam.DoFn):
    def process(self, element):
        yield "count_all", 1

if __name__ == '__main__':
  run_pipeline()

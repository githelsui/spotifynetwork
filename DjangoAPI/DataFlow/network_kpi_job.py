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
from credentials import BIGQUERY_NETWORK_RENDERS, BIGQUERY_NETWORK_REPORTS, GOOGLE_CLOUD_PROJECT_ID, STAGING_LOCATION, TEMP_LOCATION

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
                    query="""
                    SELECT date, timeframe, MAX(count) AS max_count 
                    FROM `spotifynetwork.spotifynetwork_data.network_renders`
                    GROUP BY date, timeframe""",
                    use_standard_sql=True
                )
            )
        )                                                             
        
        # Transform: Count all instances of network selections by timeframe and date
        
        # Step 1: Calculate total occurrences per date
        total_per_date = (
            network_renders_source
            | 'ExtractDate' >> beam.Map(lambda x: (x['date'], x['max_count']))
            | 'GroupByDate' >> beam.CombinePerKey(sum)
        )
        
        # -> Calculate percentage for network selections 
        # Step 2: Calculate percentage
        network_percentages = (
            network_renders_source
            | 'CalculatePercentage' >> beam.ParDo(CalculatePercentage(),
                                                  total_occurrences_per_date=beam.pvalue.AsDict(total_per_date))
        )
        
        # Step 3: Serialize the data to fit into output schema
        # network_reports = (
        #     network_percentages
        #     | 'SerializeResults' >> beam.ParDo(SerializeElement())
        # )
        # Print the results
        network_reports | beam.Map(print)
        
        
        # Load
        # network_count | "WriteNetworkToBigQuery" >> beam.io.WriteToBigQuery(
        #             BIGQUERY_NETWORK_REPORTS,
        #             schema='date:string,timeframe_percent:json',
        #             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        #             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
                
    # Run the pipeline using the DataflowRunner
    result = pipeline.run()
    result.wait_until_finish()
    
class CalculatePercentage(beam.DoFn):
    def process(self, element, total_occurrences_per_date):
        print(f"Received total_count: {total_occurrences_per_date}")
        print(f"Received element: {element}")
        date = element['date']
        timeframe = element['timeframe']
        max_count = element['max_count']
        total_occurrences = total_occurrences_per_date[date]
        percentage = (max_count / total_occurrences) * 100 if total_occurrences != 0 else 0
        yield {'date': date, 'timeframe': timeframe, 'percentage': percentage}
        
# class SerializeElement(beam.DoFn):
#     def process(self, elements):
#         timeframe_percent = {}
#         # serialized_data = {
#         #     'date': date,
#         #     'timeframe_percent': timeframe_percent
#         # }
#         for element in elements:
#             # Process each element as needed
#             processed_element = {'processed': element}
#             date = element['date']
#             timeframe = element['timeframe']
#             percentage = element['percentage']
#             yield processed_element
#         # yield serialized_data
    

if __name__ == '__main__':
  run_pipeline()

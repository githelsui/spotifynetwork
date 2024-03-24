from google.cloud import pubsub_v1,exceptions
from django.http import HttpResponse
from concurrent import futures
from datetime import datetime
from .logger import Logger

class Publisher:
    
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = 'spotifynetwork'
        self.logger = Logger()
        
    def publish(self, message, operation, attributes=None):
        return ""
        
    # def publish(self, message, operation, attributes=None):
        
    #     topic_path = 'projects/{project_id}/topics/{topic_name}'.format(
    #         project_id=self.project_id,
    #         topic_name=operation
    #     )
        
    #     try:
    #         data = message.encode('utf-8')
    #         current_dt = datetime.now()
    #         formatted_dt = current_dt.strftime("%m-%d-%Y %H:%M:%S")
    #         date = current_dt.date().strftime("%m-%d-%Y")
    #         time = current_dt.time().strftime("%H:%M:%S")
    #         if attributes:
    #             attributes['date'] = date
    #             attributes['time'] = time
    #             attributes['timestamp'] = formatted_dt
    #         else:
    #             attributes = {  
    #                             'date': date,
    #                             'time': time,
    #                             'timestamp': formatted_dt
    #                          }
    #         self.publisher.publish(topic_path, data, **attributes)
    #         self.logger.log(f'Cloud PubSub message published. Topic: {operation}', 'info', 'cross-cutting concerns', operation, 1)
    #     except exceptions.GoogleCloudError as e:
    #         self.logger.log(f'Cloud PubSub message failed to publish. Error: {e}', 'error', 'cross-cutting concerns', operation, 0)
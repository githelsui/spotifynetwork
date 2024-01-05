from google.cloud import pubsub_v1,exceptions
from django.http import HttpResponse
from concurrent import futures
from .logger import Logger

class Publisher:
    
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = 'spotifynetwork'
        self.logger = Logger()
        
    def publish(self, message, operation, attributes=None):
        
        topic_path = 'projects/{project_id}/topics/{topic_name}'.format(
            project_id=self.project_id,
            topic_name=operation
        )
        
        try:
            data = message.encode('utf-8')
            if attributes:
                self.publisher.publish(topic_path, data, **attributes)
            else:
                self.publisher.publish(topic_path, data)
        except exceptions.GoogleCloudError as e:
            self.logger.log(f'Cloud PubSub message failed to publish. Error: {e}', 'error', 'cross-cutting concerns', operation, 0)
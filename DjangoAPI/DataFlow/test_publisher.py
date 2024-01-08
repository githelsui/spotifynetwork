import json
import time
from datetime import datetime
import random
from google.auth import jwt
from google.cloud import pubsub_v1
from credentials import GOOGLE_APPLICATION_CREDENTIALS,  GOOGLE_CLOUD_PROJECT_ID, FEATURE_TOPIC

# --- Base variables and auth path
MAX_MESSAGES = 10000
FEATURES = ['artist-details', 'link-details', 'artist-connection', 'genre-highlight']

# --- PubSub Utils Classes
class PubSubPublisher:
    def __init__(self, credentials_path, project_id, topic_id):
        credentials = jwt.Credentials.from_service_account_info(
            json.load(open(credentials_path)),
            audience="https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
        )
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish(self, data: str, attributes: any):
        result = self.publisher.publish(self.topic_path, data, **attributes)
        return result


# --- Main publishing script
def main():
    i = 0
    publisher = PubSubPublisher(GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT_ID, FEATURE_TOPIC)
    while i < MAX_MESSAGES:
        data = "test message".encode('utf-8')
        current_dt = datetime.now()
        formatted_dt = current_dt.strftime("%m-%d-%Y %H:%M:%S")
        cDate = current_dt.date().strftime("%m-%d-%Y")
        cTime = current_dt.time().strftime("%H:%M:%S")
        rand_feature= random.choice(FEATURES)
        attributes = { 
                      'date': cDate,
                     'time': cTime,
                      'feature': rand_feature,
                       'timestamp': formatted_dt
                    }
        publisher.publish(data, attributes)
        print("Message published")
        time.sleep(random.random())
        i += 1

if __name__ == "__main__":
    main()
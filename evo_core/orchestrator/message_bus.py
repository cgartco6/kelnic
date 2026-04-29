import redis
import json
import os

class MessageBus:
    def __init__(self):
        self.client = redis.from_url(os.getenv("REDIS_URL"))

    def publish(self, channel, message):
        self.client.publish(channel, json.dumps(message))

    def subscribe(self, channel, callback):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                callback(data)

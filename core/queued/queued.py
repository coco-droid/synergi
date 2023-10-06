import redis
import json

class QueueManager:
    def __init__(self, redis_url):
        self.redis = redis.StrictRedis.from_url(redis_url)
        self.queue_name = 'message_queue'

    def publish(self, event, message):
        data = {'event': event, 'message': message}
        self.redis.lpush(self.queue_name, json.dumps(data))

    def get_messages(self):
        messages = []
        while True:
            message = self.redis.rpop(self.queue_name)
            if message is None:
                break
            messages.append(json.loads(message))
        return messages

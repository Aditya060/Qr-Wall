# consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

class RevealConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        segment_id = data['segment_id']
        # Send the reveal command to the large screen
        self.send(text_data=json.dumps({
            'segment': segment_id
        }))

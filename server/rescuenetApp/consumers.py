from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DisasterConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Connects the consumer to the "disaster_updates" group.
        """
        self.disaster_group_name = "disaster_updates"
        await self.channel_layer.group_add(
            self.disaster_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Disconnects the consumer from the "disaster_updates" group.
        """
        await self.channel_layer.group_discard(
            self.disaster_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles any incoming messages from the client (optional).
        In this example, we don't have any client-side communication,
        so this method is left empty.
        """
        pass

    async def disaster_update(self, event):
        """
        Receive disaster update data and sends it to all connected clients.
        """
        disaster_data = event['disaster_data']
        await self.send(text_data=json.dumps(disaster_data))

class CommunicationEnablerConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Connects the consumer to the specified group.
        """
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Disconnects the consumer from the group.
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles incoming messages within the group and broadcasts them.
        """
        if text_data:
            # Parse incoming JSON data
            try:
                json_data = json.loads(text_data)
            except json.JSONDecodeError:
                # Handle invalid JSON data
                return

            # Broadcast the received message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'group.message',
                    'sender': json_data.get('sender'),
                    'time': json_data.get('time'),
                    'message': json_data.get('message')
                }
            )

    async def group_message(self, event):
        """
        Receives a message from the group and sends it to the client.
        """
        sender = event.get('sender')
        time = event.get('time')
        message = event.get('message')

        # Ensure all required fields are present
        if sender is None or time is None or message is None:
            return

        # Construct the JSON message
        json_message = {
            'sender': sender,
            'time': time,
            'message': message
        }

        # Send the JSON message to the client
        await self.send(text_data=json.dumps(json_message))

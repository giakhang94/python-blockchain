import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import uuid

subscribe_key = 'sub-c-2ee2d495-e0a9-492f-9248-2a365af89099'
publish_key = 'pub-c-6ee9d1df-769b-4ebc-b030-1fd362af7b55'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key
pubnub = PubNub(pnconfig)

TEST_CHANNEL = 'TEST_CHANNEL'

# Subscribe sau khi thêm listener
# pubnub.subscribe().channels([TEST_CHANNEL]).execute()


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n-- Incoming message_object: {message_object.channel} | message: {message_object.message}')

# Thêm listener trước khi subscribe
pubnub.add_listener(Listener())

class PubSub():
    """
    Handles the publish/subscribe layer of the application
    Provides communication between the nodes of the blockchain network
    """
    def __init__(self):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

def main():
    pubsub = PubSub()
    time.sleep(1)
    print('main function is running')

    # Gửi tin nhắn
    pubsub.publish(TEST_CHANNEL, {'foo': 'bar'})

if __name__ == '__main__':
    main()

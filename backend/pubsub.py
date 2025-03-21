import time
from backend.blockchain.block import Block
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback


subscribe_key = 'sub-c-2ee2d495-e0a9-492f-9248-2a365af89099'
publish_key = 'pub-c-6ee9d1df-769b-4ebc-b030-1fd362af7b55'

pnconfig = PNConfiguration() #khai báo config object cho PubNub()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key
pubnub = PubNub(pnconfig) #PubNub() nhận 1 argument là pnconfig chứa các thông tin như subscribe_key, publish_key, uuid (với các version sau này)

# TEST_CHANNEL = 'TEST_CHANNEL'
# BLOCK_CHANNEL = "BLOCK_CHANNEL"

# Create chat channels  
CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': "BLOCK"
}


#Listener class, kế thừa thằng SubscribeCallback để xử lý khi subscribed channels nhận được message
class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        #this is a default method 
        print(f'\n-- Incoming message_object: {message_object.channel} | message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            # handle the incoming block message
            # the goal is to add thí block to the local chain
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]  #[:len(self.blockchain.chain)]
            potential_chain.append(block)
            # sau đó, node nhận message đem so với block hiện có (local chain) của mình
            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Successfully replace the local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')


# Xử lý khi subscribers nhận được message từ publishers on the subscribed channel
#add_listener nhận 1 argument là instance của Listener class
# pubnub.add_listener(Listener())

class PubSub():
    """
    Handles the publish/subscribe layer of the application
    Provides communication between the nodes of the blockchain network
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
         #PubNub() nhận 1 argument là pnconfig chứa các thông tin như subscribe_key, publish_key, uuid (với các version sau này)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()
        #Đây là cú pháp, copy rồi xài thôi. 
        #có gọi sync() thì các nodes khác mới nhận được message.


    def broadcast_block(self, block): #truyền tin
        """
        broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

def main():
    pubsub = PubSub()
    time.sleep(1)
    print('main function is running')

    # Gửi tin nhắn
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})

if __name__ == '__main__':
    main()

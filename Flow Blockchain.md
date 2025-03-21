## 1. Project structure

- root/backend
  - backend/blockchain
    - blockchain.py
    - block.py
  - backend/util
    - crypto_hash.py
    - hex_to_binary.py
    - config.py
  - backend/test (tương tự backend folder, nhưng chứa các file test)
- root/blockchain-env (for testing)

## Flow

1. create blockchain.py file

- create Blockchain class
- in Blockchain class, define **init** and `add_block` method
- `add_block` used to add a new block to the blockchain

```py
from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self,data):
        # chain_length = len(self.chain)
        # or we can use array[-1] to get the latest element
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')


if __name__ == "__main__":
    main()

```

2. block.py, define

- mine_block => create a block for adding to the blockchain
  - calculate the difficulty
  - give the hash algorithm for PoW
- genesis_block => define the first block for the blockchain
- a block contains: timestamp, last_hash, hash, difficulty, nonce

```py
import time
from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': "genesis_last_hash",
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': "genesis_nonce"
}

class Block:
    """
    Block: a unit of storage
    Store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.data = data
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )


    @staticmethod
    def mine_block(lash_block, data):
        """
        mine a block based on the given last_block and data
        until a block hash is found that meets the leading 0's proof of work requirement.
        """
        timestamp = time.time_ns()
        last_hash = lash_block.hash
        difficulty = Block.adjust_difficulty(lash_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0'*difficulty:
            nonce = nonce + 1
            # timestamp = time.time_ns()
            # nếu giữ timestamp này thì thời gian giữa 2 lần addblock rất gần, không đúng, difficulty luôn tăng
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)



        return  Block(timestamp, last_hash, hash, data, difficulty, nonce)


    @staticmethod
    def genesis():
        """
        generate the very first block
        """
        # print(Block(**GENESIS_DATA))
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE
        Increase the difficulty for quickly mined blocks
        Decrease the difficulty for slowly mined blocks
        """
        print('adjusting difficulty...')
        previous_mine_time = new_timestamp - last_block.timestamp
        print(previous_mine_time)
        if previous_mine_time  < MINE_RATE:
            return last_block.difficulty + 1
        if last_block.difficulty - 1 > 0 :
            return last_block.difficulty - 1
        return 1

def main():
    # print(f'block.py __name__: {__name__}')
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(block)

if __name__ == "__main__":
    main()
```

3. crypto_hash

- converts all the input to string value
- encodes this string value using encode utf-8
- hash this encoded value using `hash256`

```py
import hashlib
import json


def crypto_hash(*arguments):
    """
    Return a Sha-256 hash of the given data.
    """
    # stringified_data = json.dumps(data)

    stringify_arguments = sorted(map(lambda data: json.dumps(data),arguments))
    joined_data = ''.join(stringify_arguments)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash('one', 'two', 'three'): {crypto_hash(123, [{"taO": 123}], False)}")

# a = "hello"
# print(a.encode('utf-8'))
# print(hashlib.sha256(a.encode('utf-8')))
# print(hashlib.sha256(a.encode('utf-8')).hexdigest())

if __name__ == "__main__":
    main()


```

### Demo script

- backend/scripts/average_block_rate.py

```py
import time
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()
print(SECONDS)
times = []
for i in range(1000):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time)/SECONDS
    times.append(time_to_mine)

    average_time = sum(times)/len(times)
    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time to mine new block: {time_to_mine}s')
    print(f'Average time to add blocks: {average_time}s\n')
```

### Config.py file

- contain information regarding the time
- backend/util/config.py

```py
NANOSECONDS = 1
MICROSECONDS = 1000*NANOSECONDS
MILLISECONDS = 1000*MICROSECONDS
SECONDS = 1000*MILLISECONDS

MINE_RATE = 4 * SECONDS
```

### requirements and readme file

root/requirements.txt => like `package.json` in javascript
root/README.md

### hex to binary file

```py
from backend.util.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',  # Lowercase letters (optional)
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}


def hex_to_binary(hex_string) :
    binary_string = ''

    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[character]

    return binary_string

def main():
    number = 451
    hex_number = hex(number)[2:]
    print(f'hex number: {hex_number}')

    binary_number = hex_to_binary(hex_number)
    print(f'binary number {binary_number}')

    hex_to_binary_crypto_hash = hex_to_binary(crypto_hash('test-data'))
    print(f'hex_to_binary_crypto_hash: {hex_to_binary_crypto_hash}')

if __name__ == "__main__":
    main()
```

## validate chain

1.  in backend/block.py
    add is_valid_block static method for the Block class

```py


    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block by enforcing the following rule
        - The block must have the proper lash_hash reference
        - The block must meet the Proof of Work requirement
        - The difficulty must only adjust by 1
        - The block hash must be a valid combination of the block fields
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of requirement was not met')

        if abs(last_block.difficulty - block.difficulty >1):
            raise Exception('The block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.hash,
            # block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')
```

Then test it in main function

```py
def main():
    # print(f'block.py __name__: {__name__}')
    genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, 'foo')
    # print(block)

    # validating blocks
    bad_block = Block.mine_block(Block.genesis(), 'foo')
    bad_block.last_hash = 'evil_data'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')
```

2. Validate the entire blockchain

- go to backend/blockchain/blockchain.py => add is_valid_chain for the Blockchain class
- to block.py => add `__eq__` instance method

```py
block.py
    def __eq__(self, other):
        print(self)
        return self.__dict__ == other.__dict__


blockchain.py
   @staticmethod
    def is_valid_chain(chain):
        """
        validate the incoming chain
        Enforce the following rules of the block chain:
            - The chain must start with the genesis block
            - blocks must be formatted correctly
        """
        if(chain[0] != Block.genesis()):
            raise Exception("The genesis block must be valid")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)
```

## Replace chain

in blockchain.py
add `replace_chain(self, chain)` method for the `Blockchain` class

````py
    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
            - The incoming chain is longer than the local one.
            - The incoming chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer')
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')
        self.chain = chain
        ```
````

# Blockchain network

## Flask - building blockchain API (like Web Apps)

### install and setting `flask` module

1. activate test environment `blockchain-env\Scripts\activate`
2. `pip3 install Flask`. In this course `pip3 install Flask==1.1.1`
   or run for python3 => `python3 -m pip install Flask`
3. check packages: `pip3 freeze`
4. create root/backend/app/**init**.py

```py
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def default():
        return 'Welcome to the blockchain'

    @app.route('/cac')
    def cac():
        return 'cac'

    @app.route('/test')
    def test():
        return 'test'
    app.run()
```

### create blockchain instance for callers to get data (a instance of the blockchain)

1. serialize a block in the the dictionary of its attributes

- go to `block.py`, add `to_json(self)` as a new method of the Block class

```py
   def to_json(self):
       return self.__dict__
```

- go to `blockchain.py`, add another `to_json(self)` with different logic as a new method of the Blockchain class

```py
def to_json(self):
    serialize_chain = []
    for block in self.chain:
        serialize_chain.append(block.to_json())
        # cover a block to dictionary then add to the serialize_chain array
    return serialize_chain
        # after that, we can covert this returned value to json

# or we can use an alternative way to do this task
    return list(map(lamda block: block.to_json(), self.chain))

```

- in router: using `jsonify` from `flask` => `return jsonify(blockchain.to_json())`

### Mine a new block end point lecture 54

### realtime message (code I store on chatGPT or Zalo Cloud)

1. register an account on Hubnub.com
2. create new app named 'python-blockchain'
3. copy Publish key and Subscribe key
4. install pubnub module `python3 -m pip install pubnub`
5. tạo pub sub, pubsub class xong thì qua bên **init**.py để tạo 1 instance của PubSub class
   => để đồng bộ gửi và nhận message (code bên dưới)

### realtime socket using PEER

backend/app/**init**.py

```py
import os
import random
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub =   PubSub()

for i in range(5):
    blockchain.add_block(i)

@app.route('/')
def default():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'

    blockchain.add_block(transaction_data)
    return jsonify(blockchain.chain[-1].to_json())
# from here
PORT = 5000

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

app.run(port = PORT) #to here
```

```py
pubsub.py
import time
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
    def message(self, pubnub, message_object):
        #this is a default method
        print(f'\n-- Incoming message_object: {message_object.channel} | message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = message_object.message
            potential_chain = self.blockchain.chain[:]  #[:len(self.blockchain.chain)]

            self.blockchain.replace_chain(potential_chain)

# Xử lý khi subscribers nhận được message từ publishers on the subscribed channel
#add_listener nhận 1 argument là instance của Listener class
pubnub.add_listener(Listener())

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
        self.pubnub.publish().channel(channel).message(message).sync() #Đây là cú pháp, copy rồi xài thôi.
        #có gọi sync() thì các nodes khác mới nhận được message.

    def broadcast_block(self, block):
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
```

### multiple peers

- **init**.py
- add these code

```py
import os
import random

PORT = 5000
if os.environ.get('PEER') == 'True'
    PORT = random(5001, 6000)
app.run(port=PORT)

# to run another command (peer):
# windows: $env:PEER=True; python -m backend.app
# MacOS: export PEER=True && python -m backend.app

```

### broadcast

- Phát sóng/Truyền phát dữ liệu đến toàn bộ mạng lưới của blockchain đó.

1. Go to pubsub.py

- tạo 1 object chứa các channels => `CHANNELS = {"TEST": "TEST", "BLOCK": "BLOCK"}`

```py pubsub.py
class PubSub():
    def __init__(self):
        self.pubnub.subscribe().channels(CHANNELS.values()).execute().sync()
```

2. define a broadcast_block method in PubSub class

```py
def broadcast_block(self, block):
    """
    Broadcast a block object to all nodes
    """
    self.publish(CHANNELS['BLOCK'], block.to_json())
```

3. update the app/**init**.py file

```py
@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'

    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1] #add this line
    pubsub.broadcast_block(block) #add this line
    return jsonify(block.to_json()) #edit this line
```

4. add the received block: Once a block message is received on the block channel
   -> the block should be validated
   -> If the block is valid (the block follows all the rules) => It will be added to the local blockchain of the receiving nodes
   -> xử lý logic ở Listener class
   - add block vào instance của blockchain
   - Nhưng hiện tại Listener class chưa truy cập được vào instance của blockchain => cẩn phải thêm code
     -> thêm **init**() method
     -> sau đó qua PubSub class, ở `__init__` cũng thêm `blockchain` as the second argument
     -> sau đó qua `app/__init__` thêm `blockchain` as an argument of the pubsub instance
     ```py
         app = Flask(__name__)
         blockchain = Blockchain()
         pubsub =   PubSub(blockchain) # thêm ở đây
     ```

```py
class Listener(SubscribeCallback):
    #thêm ở đây
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        #this is a default method
        print(f'\n-- Incoming message_object: {message_object.channel} | message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = message_object.message
            potential_chain = self.blockchain.chain[:]  #[:len(self.blockchain.chain)]

            self.blockchain.replace_chain(potential_chain)

# Xử lý khi subscribers nhận được message từ publishers on the subscribed channel
#add_listener nhận 1 argument là instance của Listener class
pubnub.add_listener(Listener())

class PubSub():
    """
    Handles the publish/subscribe layer of the application
    Provides communication between the nodes of the blockchain network
    """
    def __init__(self, blockchain): #thêm ở đây
        self.pubnub = PubNub(pnconfig)
         #PubNub() nhận 1 argument là pnconfig chứa các thông tin như subscribe_key, publish_key, uuid (với các version sau này)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain)) #thêm ở đây
```

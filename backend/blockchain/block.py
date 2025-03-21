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

    def __eq__(self, other):
        print(self)
        return self.__dict__ == other.__dict__
    
    def to_json(self):
        """
        Serialize the block into a dictionary of its attributes
        """
        return self.__dict__
    
    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation back into a block instance
        """
        return Block(**block_json)

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
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash: 
            raise Exception('The block hash must be correct')


def main():
    # print(f'block.py __name__: {__name__}')
    genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, 'foo')
    # print(block)

    # validating blocks
    bad_block = Block.mine_block(Block.genesis(), 'foo')
    # bad_block.last_hash = 'evil_data'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')

if __name__ == "__main__":
    main()


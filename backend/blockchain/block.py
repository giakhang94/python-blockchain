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
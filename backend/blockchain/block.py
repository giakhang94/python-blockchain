import time
from backend.util.crypto_hash import crypto_hash



class Block: 
    """
    Block: a unit of storage
    Store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, timestamp, last_hash, hash, data):
        self.data = data
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
    
    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data})'
        )


    @staticmethod
    def mine_block(lash_block, data):
        """
        mine a block based on the given last_block and data.
        """
        last_hash = lash_block.hash
        timestamp = time.time_ns()
        hash = crypto_hash(timestamp, last_hash, data)
        return  Block(timestamp, last_hash, hash, data)


    @staticmethod
    def genesis():
        """
        generate the very first block
        """
        timestamp = time.time_ns()
    
        return Block(timestamp, 'genesis_lash_hash', 'genesis_hash', [])
    

def main():

    # print(f'block.py __name__: {__name__}')
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    print(block)

if __name__ == "__main__":
    main()
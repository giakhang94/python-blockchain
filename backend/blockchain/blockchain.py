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

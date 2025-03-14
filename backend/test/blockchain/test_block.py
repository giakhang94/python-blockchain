from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hex_to_binary import hex_to_binary
import time
from backend.config import MINE_RATE, SECONDS


def test_mine_block():
    last_block = Block.genesis()
    data  = 'test-data'
    block = Block.mine_block(last_block, data)


    assert isinstance(block,Block)
    assert block.last_hash == last_block.hash
    assert block.data == data
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty



def test_genesis():
    assert isinstance(Block.genesis(), Block)
    assert Block.genesis().timestamp == GENESIS_DATA['timestamp']
    assert Block.genesis().last_hash == GENESIS_DATA['last_hash']
    assert Block.genesis().hash == GENESIS_DATA['hash']
    assert Block.genesis().data == GENESIS_DATA['data']

    for key, value in GENESIS_DATA.items():
        getattr(Block.genesis(), key) == value

def test_quickly_mined_block():
    last_block  = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block  = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE/SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')
    assert mined_block.difficulty  == last_block.difficulty - 1
    
def test_mined_block_difficulty_limits_at_1():
    
    last_block  = Block(time.time_ns(), 'test_last_hash', 'test_hash', 'test_data', 1, 0)
    time.sleep(MINE_RATE/SECONDS)

    assert last_block.difficulty ==1

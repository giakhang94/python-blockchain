from backend.blockchain.block import Block, GENESIS_DATA


def test_mine_block():
    last_block = Block.genesis()
    data  = 'test-data'
    block = Block.mine_block(last_block, data)


    assert isinstance(block,Block)
    assert block.last_hash == last_block.hash
    assert block.data == data


def test_genesis():
    assert isinstance(Block.genesis(), Block)
    assert Block.genesis().timestamp == GENESIS_DATA['timestamp']
    assert Block.genesis().last_hash == GENESIS_DATA['last_hash']
    assert Block.genesis().hash == GENESIS_DATA['hash']
    assert Block.genesis().data == GENESIS_DATA['data']

    for key, value in GENESIS_DATA.items():
        getattr(Block.genesis(), key) == value
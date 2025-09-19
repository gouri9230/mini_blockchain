from config import GENESIS_BLOCK
from hash_generator import hash_function
from datetime import datetime

class Block:
    def __init__(self, block_no, timestamp, data, prev_hash, hash):
        self.block_no = block_no
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.data = data
        self.hash = hash
    
    def __str__(self):
        return str({"block_no": self.block_no, "timestamp": self.timestamp, "data": self.data, "prev_hash": self.prev_hash, "block_hash": self.hash})
    
    ##__repr__ = __str__
    
    @staticmethod
    def genesis_block():
        return GENESIS_BLOCK
    
    @staticmethod
    def mine_block(prev_block, data):
      timestamp =  int(datetime.now().timestamp())
      prev_hash = prev_block["block_hash"]
      block_num = prev_block["block_no"] + 1
      new_block = Block(block_num, 
                        timestamp, 
                        data, 
                        prev_hash, 
                        hash_function([block_num, timestamp, data, prev_hash]))
      print(new_block)
      return new_block

#print("\n Genesis block -> \n", Block.genesis_block())
#bloc = Block.mine_block(GENESIS_BLOCK, "testing block")
#print(bloc)
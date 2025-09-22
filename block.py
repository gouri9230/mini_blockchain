from hash_generator import hash_function
from datetime import datetime

DIFFICULTY = 4
NONCE = 0
MINING_RATE = 2000 # 2 sec

class Block:
    def __init__(self, block_no, timestamp, data, prev_hash, hash, nonce, difficulty):
        self.block_no = block_no
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.data = data
        self.hash = hash
        self.nonce = nonce
        self.difficulty = difficulty
    
    def __str__(self):
        return str({"block_no": self.block_no, "timestamp": self.timestamp, "data": self.data, "prev_hash": self.prev_hash, "hash": self.hash, "nonce": self.nonce, "difficulty": self.difficulty})
    
    @staticmethod
    def genesis_block():
        return Block(0, 1000, [], "0x0000", "1dd327f2d4772295a8ec7a96e0338fef7291c1652976ccc498dbd9849b01f5e9", NONCE, DIFFICULTY)
    
    @staticmethod
    def mine_block(prev_block, data):
      prev_hash = prev_block.hash
      block_no = prev_block.block_no + 1
      golden_nonce = 0
      while True:
          golden_nonce += 1
          timestamp =  int(datetime.now().timestamp() * 1000)
          difficulty = Block.adjust_difficulty(prev_block, timestamp)
          target = "0" * difficulty
          calculated_hash = hash_function([block_no, timestamp, data, prev_hash, golden_nonce, difficulty])
          hex_to_binary = bin(int(calculated_hash, 16))[2:].zfill(256)
          if hex_to_binary.startswith(str(target)):
            new_block = Block(block_no, timestamp, data, prev_hash, calculated_hash, golden_nonce, difficulty)
            return new_block
    
    @staticmethod
    def adjust_difficulty(block, timestamp):
       time_taken = timestamp - block.timestamp
       if block.difficulty <= 1:
            return block.difficulty
       
       if time_taken > MINING_RATE:
            return block.difficulty - 1
       else:
           return block.difficulty + 1
    
       
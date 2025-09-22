from hash_generator import hash_function
from datetime import datetime

# some initial values set
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
        """
        creates a genesis block with some predetermined values. 
        """
        return Block(0, 1000, [], "0x0000", "1dd327f2d4772295a8ec7a96e0338fef7291c1652976ccc498dbd9849b01f5e9", NONCE, DIFFICULTY)
    
    @staticmethod
    def mine_block(prev_block, data):
      prev_hash = prev_block.hash
      block_no = prev_block.block_no + 1
      # find a golden nonce to mine a block
      golden_nonce = 0
      while True:
          golden_nonce += 1
          timestamp =  int(datetime.now().timestamp() * 1000)
          # adjust the difficulty level of mining the block based on the time it took to mine previous block
          difficulty = Block.adjust_difficulty(prev_block, timestamp)
          # target set based on the difficulty to find golden nonce
          target = "0" * difficulty
          calculated_hash = hash_function([block_no, timestamp, data, prev_hash, golden_nonce, difficulty])
          hex_to_binary = bin(int(calculated_hash, 16))[2:].zfill(256)
          # check if the generated hash meets the target constraint
          if hex_to_binary.startswith(str(target)):
            new_block = Block(block_no, timestamp, data, prev_hash, calculated_hash, golden_nonce, difficulty)
            return new_block
    
    @staticmethod
    def adjust_difficulty(block, timestamp):
       # calculate time taken to mine a block
       time_taken = timestamp - block.timestamp
       # if the time_taken is in negative then consider difficulty as 1 
       if block.difficulty <= 1:
            return block.difficulty
       # if the time taken is greater than the mining rate, then decrease the difficulty level, if not, increase
       if time_taken > MINING_RATE:
            return block.difficulty - 1
       else:
           return block.difficulty + 1
    
       
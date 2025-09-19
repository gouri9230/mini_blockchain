from main import Block
from hash_generator import hash_function

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis_block()]

    def __str__(self):
        return f"blockchain is: {self.chain}"
    
    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block.mine_block(prev_block, data)
        print("new block:", new_block)
        self.chain.append(new_block)
        print("chain: ", dict(self.chain))

    @staticmethod
    def is_valid_chain(chain):
        if chain[0] != Block.genesis_block():
            return "Chain is invalid"
        else:
            for i in range(1,len(chain)):
                print("inside: ", chain)
                if chain[i-1]["block_hash"] != chain[i]["block_hash"]:
                    return "your chain is broken"
                current_block_hash = hash_function([chain[i]["block_num"], chain[i]["timestamp"], chain[i]["data"], chain[i]["prev_hash"]])
                if current_block_hash != chain[i]["block_hash"]:
                    return "current block is invalid"
            return "Blockchain is validated without issues!"


bc = Blockchain()
bc.add_block("this is block added after blockchain class")
result = Blockchain.is_valid_chain(bc.chain)
print(result)
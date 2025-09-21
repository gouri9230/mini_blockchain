from block import Block
from hash_generator import hash_function

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis_block()]

    def __str__(self):
        return f"blockchain is: {self.chain.__dict__}"
    
    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block.mine_block(prev_block, data)
        self.chain.append(new_block)

    def replace_chain(self, chain):
        if len(chain)<= len(self.chain):
            return "The incoming chain is not longer than the existing chain"
        
        if Blockchain.is_valid_chain() != True:
            return "The incoming chain is not valid"
        
        self.chain = chain
            
    @staticmethod
    def is_valid_chain(chain):
        chain_dicts = [block.__dict__ for block in chain]

        if chain_dicts[0] != Block.genesis_block().__dict__:
            print("Chain is invalid") 
            return False
        
        for i in range(1,len(chain)):
            if chain_dicts[i-1]["hash"] != chain_dicts[i]["prev_hash"]:
                print("your chain is broken") 
                return False
            
            prev_difficulty = chain_dicts[i-1]["difficulty"]
            current_difficulty = chain_dicts[i]["difficulty"]
            current_block_hash = hash_function([chain_dicts[i]["block_no"], 
                                                chain_dicts[i]["timestamp"], 
                                                chain_dicts[i]["data"], 
                                                chain_dicts[i]["prev_hash"], 
                                                chain_dicts[i]["nonce"],
                                                chain_dicts[i]["difficulty"]])
            
            if current_block_hash != chain_dicts[i]["hash"]:
                print("current block is invalid") 
                return False
            if abs(current_difficulty - prev_difficulty) > 1:
                print("Difficulty level has been compromised")
                return False

        print("Blockchain is validated without issues!") 
        return True

bc = Blockchain()
bc.add_block("this is block added after blockchain class")
bc.add_block("mining another block")
result = Blockchain.is_valid_chain(bc.chain)
#print(result)
#print([block.__dict__ for block in bc.chain])
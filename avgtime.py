from blockchain import Blockchain

blockchain = Blockchain()
timestamps = []

# to avoid getting genesis block
blockchain.add_block("testing block")
for i in range(1000):
    print("inside for loop")
    # get recently added block as previous block
    prev_block = blockchain.chain[-1]
    prev_block_data = prev_block.__dict__
    prev_timestamp = prev_block_data["timestamp"]
    # add another block to compare how much time it takes to add new block
    blockchain.add_block(f"testing block {i}")
    next_block = blockchain.chain[-1]
    next_block_data = next_block.__dict__
    new_timestamp = next_block_data["timestamp"]
    time_difference = new_timestamp - prev_timestamp
    timestamps.append(time_difference)
    avg = sum(timestamps) / len(timestamps)
    print(f'Time taken to mine a block: {time_difference}ms, Difficulty: {next_block_data["difficulty"]} average time: {avg}ms')

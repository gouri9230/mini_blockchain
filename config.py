from hash_generator import hash_function

GENESIS_BLOCK = {
    "block_no": 0,
    "timestamp": "19-09-2025",
    "data": [],
    "prev_hash": "0x0000", 
    "block_hash": hash_function([0,"19-09-2025",[],"0x0000"])
}
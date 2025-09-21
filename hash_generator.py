import hashlib

def hash_function(data):
    
    if isinstance(data, list):
        elements = ''.join(str(d) for d in data)
        hash_value = hashlib.sha256(elements.encode()).hexdigest()

    return hash_value

#hash = hash_function([0, 1000, [], "0x0000", 0, 3])
#hash = "215d414d990bce5259d6bc1697adbbd60869d60cfe713d2094f9821df48fcba0"
#bin_hash = bin(int(hash, 16))[2:].zfill(256)
#print(bin_hash)

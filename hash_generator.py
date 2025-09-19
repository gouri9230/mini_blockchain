import hashlib

def hash_function(data):
    
    if isinstance(data, list):
        elements = ''.join(str(d) for d in data)
        hash_value = hashlib.sha256(elements.encode()).hexdigest()
    else:
        hash_value = hashlib.sha256(data.encode()).hexdigest()

    return hash_value
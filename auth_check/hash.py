import hashlib

SALT = 'random_salt'

def hashing(original):
    hashed = hashlib.sha256((original + SALT).encode('utf-8')).hexdigest()
    return hashed

def verifying(stored, provided):
    hashed = hashing(provided)
    return hashed == stored
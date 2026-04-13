from hashlib import sha256

input_ = input('Enter something: ')
print(sha256(input_.encode('utf-8')).hexdigest())


def hash_message():
    print()

def verify_hash() :
    print() 
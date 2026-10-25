
import hmac
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16

# Gen key
def gen():
    return os.urandom(BLOCK_SIZE)

def xor_blocks(block1, block2):
    return bytes(a ^ b for a, b in zip(block1, block2))

# Check for valid block size
def mac(key, msg):
    if len(msg) == 0 or len(msg) % BLOCK_SIZE != 0:
        raise ValueError("Invalid Block Size")

    #encryption
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()


    chain = bytes(BLOCK_SIZE)
    #Process each block to get tag
    for i in range(0, len(msg), BLOCK_SIZE):
        block = msg[i:i + BLOCK_SIZE]

        block = xor_blocks(chain, block) # XOR the block with chain
        chain = encryptor.update(block)

    return chain


def verify(key, msg, tag):
    if len(msg) == 0 or len(msg) % BLOCK_SIZE != 0: #length check
        return False

    if len(tag) != BLOCK_SIZE:
        return False

    # Calculate + compare correct tag
    correct_tag = mac(key, msg)
    return hmac.compare_digest(correct_tag, tag)

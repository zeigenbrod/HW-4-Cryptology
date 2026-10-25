
from cbcmac import BLOCK_SIZE, gen, mac, verify, xor_blocks

class Oracle:
    def __init__(self):
        self.key = gen()
        self.queried_messages = []

#record message, return tag
    def query(self, msg):
        self.queried_messages.append(msg)
        return mac(self.key, msg)
#check tag
    def verify(self, msg, tag):
        return verify(self.key, msg, tag)

    def received(self, msg):
        return msg in self.queried_messages


def forge(query, target):
    # turn target into blocks
    blocks = []
    for i in range(0, len(target), BLOCK_SIZE):
        blocks.append(target[i:i + BLOCK_SIZE])

    # query 1 (Find first block tag)
    first_message = blocks[0]
    first_tag = query(first_message)

    # query 2 (modify second block w/ first tag)
    second_message = xor_blocks(blocks[1], first_tag)

    # Add remainder
    for block in blocks[2:]:
        second_message += block

    forged_tag = query(second_message)

    return forged_tag

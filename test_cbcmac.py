import unittest
from cbcmac import BLOCK_SIZE, mac, verify


KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")

MESSAGE = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a"
    "ae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52ef"
    "f69f2445df4f9b17ad2b417be66c3710"
)

TAGS = {
    1: "3ad77bb40d7a3660a89ecaf32466ef97",
    2: "b148c17f309ee692287ae57cf12add49",
    3: "c93d11bfaf08c5dc4d90b37b4dee002b",
    4: "a7356e1207bb406639e5e5ceb9a9ed93",
}

def flip_bit(data, bit):
    flipped = bytearray(data)
    flipped[bit // 8] ^= 1 << (bit % 8)
    return bytes(flipped)


class TestCBCMAC(unittest.TestCase):

    def test_correct_tags(self): #check if expected tags produced
        for number_of_blocks, tag_hex in TAGS.items():
            message = MESSAGE[:BLOCK_SIZE * number_of_blocks]
            tag = bytes.fromhex(tag_hex)
            self.assertEqual(mac(KEY, message), tag)

    def test_correct_tags_accepted(self): #test verify accepts correct inputs
        for number_of_blocks, tag_hex in TAGS.items():
            message = MESSAGE[:BLOCK_SIZE * number_of_blocks]
            tag = bytes.fromhex(tag_hex)
            self.assertTrue(verify(KEY, message, tag))

    def test_invalid_message_len(self):
        for message in [b"", bytes(17)]:
            with self.assertRaises(ValueError):
                mac(KEY, message)
            self.assertFalse(verify(KEY, message, bytes(BLOCK_SIZE)))

    def test_invalid_tag_len(self):
        message = MESSAGE[:BLOCK_SIZE]
        correct_tag = bytes.fromhex(TAGS[1])
        invalid_tags = [
            b"",
            correct_tag[:15],
            correct_tag + b"\x00"
        ]
        for tag in invalid_tags:
            self.assertFalse(verify(KEY, message, tag))

#flipping bits test
    def test_changed_message_rejected(self):
        for number_of_blocks, tag_hex in TAGS.items():
            message = MESSAGE[:BLOCK_SIZE * number_of_blocks]
            tag = bytes.fromhex(tag_hex)
            self.assertFalse(verify(KEY, flip_bit(message, 0), tag))

    def test_changed_tag_rejected(self):
        for number_of_blocks, tag_hex in TAGS.items():
            message = MESSAGE[:BLOCK_SIZE * number_of_blocks]
            tag = bytes.fromhex(tag_hex)
            self.assertFalse(verify(KEY, message, flip_bit(tag, 0)))


if __name__ == "__main__":
    unittest.main()
from cbcmac import BLOCK_SIZE
from forgery import Oracle, forge


class FixedLengthOracle(Oracle):
    def __init__(self, blocks):
        super().__init__()
        self.blocks = blocks

    def query(self, msg):
        if len(msg) != self.blocks * BLOCK_SIZE: #check required block size
            raise ValueError(
                f"oracle rejected a {len(msg) // BLOCK_SIZE}-block message "
                f"(accepts only {self.blocks} blocks)"
            )
        return super().query(msg)

    def verify(self, msg, tag):
        if len(msg) != self.blocks * BLOCK_SIZE: #check required block size
            return False
        return super().verify(msg, tag)


def main():
    oracle = FixedLengthOracle(3) #3 block message oracle
    target = b"from=alice&to=mallory&amount=1000000&note=rent!!"

    queries = []

    def query(msg):
        queries.append(msg)
        return oracle.query(msg)

    # test 2 query forgery
    try:
        forge(query, target)
        print("2 query forgery accepted.")
    except ValueError as error:
        print(f"2 query forgery fails at query {len(queries)}: {error}")


if __name__ == "__main__":
    main()
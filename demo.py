
from forgery import Oracle, forge

target = b"from=alice&to=mallory&amount=1000000&note=rent!!"

runs = 100
successes = 0

print("Target message:", target.decode())
print("Target hex:", target.hex())

for run in range(1, runs + 1):
    oracle = Oracle()
    queries = []

    def query(message):
        tag = oracle.query(message)
        queries.append((message, tag))
        return tag

    # forged tag
    forged_tag = forge(query, target)

    #is forged accepted
    target_was_queried = oracle.received(target)
    accepted = oracle.verify(target, forged_tag)

    success = (accepted and not target_was_queried)

    if success:
        successes += 1

    if run:
        print("\nrun", run)

        for number, (message, tag) in enumerate(queries, start=1):
            print("query", number, "message:", message.hex())
            print("query", number, "tag:", tag.hex())

        print("forged tag:", forged_tag.hex())
        print("oracle received target:", target_was_queried)
        print("accepted:", accepted)
        print("successful forgery:", success)

print("\nsuccessful forgeries:", successes, "out of", runs)

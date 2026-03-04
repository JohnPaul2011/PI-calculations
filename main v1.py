import os
import gzip
import json

DIR = "Divisions"
os.makedirs(DIR, exist_ok=True)

a = 22
b = 7

STATE_FILE = DIR + "/state.json"
DATA_FILE = DIR + "/pi_digits.txt.gz"

# Load state if exists
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as s:
        state = json.load(s)
        c = state["c"]
        total_digits = state["digits"]
else:
    c = a
    total_digits = 0

CHUNK_SIZE = 1_000_000

print("Continuing from digit:", total_digits)

try:
    with gzip.open(DATA_FILE, "ab", compresslevel=9) as f:
        buffer = bytearray()

        while True:
            g = c // b
            c = (c - g * b) * 10

            buffer.append(48 + g)

            if len(buffer) >= CHUNK_SIZE:
                print("Added")
                f.write(buffer)
                total_digits += len(buffer)
                buffer.clear()

except KeyboardInterrupt:
    print("\nStopped at:", total_digits + len(buffer))

    # Save remaining buffer
    with gzip.open(DATA_FILE, "ab", compresslevel=9) as f:
        if buffer:
            f.write(buffer)

    # Save state
    with open(STATE_FILE, "w") as s:
        json.dump({
            "c": c,
            "digits": total_digits + len(buffer)
        }, s)

    print("State saved.")

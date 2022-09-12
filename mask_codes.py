from hashlib import sha224
import json

with open("mask_codes.json", "r") as f:
    full = json.load(f)

hashes = [sha224(c.encode()).hexdigest() for c in full]

hashes = list(sorted(hashes))

with open("organizations/mask_identifiers.json", "w") as f:
    json.dump(hashes, f, indent=4)

print("hashes", len(hashes))

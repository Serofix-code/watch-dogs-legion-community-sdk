import collections
import sys

from common import load_records

records = load_records()
ids = collections.Counter(record["id"] for record in records)
names = collections.Counter((record["kind"], record["name"].casefold()) for record in records)
errors = [f"duplicate id: {key}" for key, count in ids.items() if count > 1]
errors += [f"duplicate {key[0]} name: {key[1]}" for key, count in names.items() if count > 1]
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"No duplicate symbols in {len(records)} records.")

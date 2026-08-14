import sys

from common import ROOT, load_records

records = load_records()
ids = {record["id"] for record in records}
errors = []
for record in records:
    errors += [f"{record['id']}: unknown related id {related}" for related in record.get("related", []) if related not in ids]
    for evidence in record.get("evidence", []):
        reference = evidence["reference"]
        if not (ROOT / reference).is_file():
            errors.append(f"{record['id']}: missing evidence file {reference}")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"All references resolve across {len(records)} records.")

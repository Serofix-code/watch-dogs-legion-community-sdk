import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdk" / "python"))
from wdl_sdk import ResearchDatabase  # noqa: E402

parser = argparse.ArgumentParser(description="Search the WDL community SDK database")
parser.add_argument("query", nargs="+")
args = parser.parse_args()
matches = ResearchDatabase.open_repository(ROOT).search(" ".join(args.query))
for record in matches:
    print(f"[{record.confidence.upper()}] {record.id}\n  {record.name}\n  {record.summary}")
if not matches:
    print("No matches.")

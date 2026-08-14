from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdk" / "python"))

from wdl_sdk import ResearchDatabase  # noqa: E402

database = ResearchDatabase.open_repository(ROOT)
for record in database.search("operative roster"):
    print(f"[{record.confidence.upper()}] {record.id}: {record.summary}")

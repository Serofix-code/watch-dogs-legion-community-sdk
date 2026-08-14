import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdk" / "python"))

from wdl_sdk import ResearchDatabase  # noqa: E402


class ResearchDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.database = ResearchDatabase.open_repository(ROOT)

    def test_loads_initial_records(self):
        self.assertGreaterEqual(len(self.database.records), 4)

    def test_get_by_stable_id(self):
        self.assertEqual(self.database.get("system.operative.roster").confidence, "confirmed")

    def test_search_is_case_insensitive(self):
        self.assertTrue(any(record.id == "system.camera.freecam" for record in self.database.search("CAMERA")))


if __name__ == "__main__":
    unittest.main()

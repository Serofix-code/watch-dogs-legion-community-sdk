from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("inspect_fat5_entry", ROOT / "tools" / "inspect_fat5_entry.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Fat5InspectorTests(unittest.TestCase):
    def test_known_photo_camera_config_hash(self) -> None:
        self.assertEqual(
            MODULE.compute_name_hash(
                r"generated\databases\generic\photocameraconfig_40469731.obj"
            ),
            0xA27499A333E8AA3E,
        )

    def test_hash_is_case_insensitive(self) -> None:
        self.assertEqual(MODULE.compute_name_hash("Example/Path"), MODULE.compute_name_hash("example/path"))


if __name__ == "__main__":
    unittest.main()

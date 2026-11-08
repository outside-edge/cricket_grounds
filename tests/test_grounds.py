import csv
import unittest
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


class GroundDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "grounds.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            cls.columns = reader.fieldnames
            cls.rows = list(reader)

    def test_schema_and_values(self):
        self.assertEqual(self.columns, [
            "ground_profile_id", "ground_label", "country", "valid_from",
            "valid_until", "source", "method", "reference_match_id", "reference_ground",
        ])
        self.assertTrue(self.rows)
        methods = {"legacy_match_link", "audited_jurisdiction", "verified_location"}
        for row in self.rows:
            with self.subTest(ground=row["ground_profile_id"]):
                self.assertGreater(int(row["ground_profile_id"]), 0)
                self.assertGreater(int(row["reference_match_id"]), 0)
                for key in set(self.columns) - {"reference_ground"}:
                    self.assertTrue(row[key].strip(), key)
                    self.assertEqual(row[key], row[key].strip())
                self.assertIn(row["method"], methods)
                parsed = urlparse(row["source"])
                self.assertEqual(parsed.scheme, "https")
                self.assertTrue(parsed.netloc)
                self.assertLess(date.fromisoformat(row["valid_from"]),
                                date.fromisoformat(row["valid_until"]))
                if row["method"] == "legacy_match_link":
                    self.assertTrue(row["reference_ground"])

    def test_keys_and_intervals(self):
        groups = defaultdict(list)
        keys = set()
        for row in self.rows:
            key = (row["ground_profile_id"], row["valid_from"], row["valid_until"])
            self.assertNotIn(key, keys)
            keys.add(key)
            groups[row["ground_profile_id"]].append(row)
        for ground, rows in groups.items():
            ordered = sorted(rows, key=lambda row: row["valid_from"])
            for earlier, later in zip(ordered, ordered[1:]):
                with self.subTest(ground=ground):
                    self.assertLessEqual(earlier["valid_until"], later["valid_from"])


if __name__ == "__main__":
    unittest.main()

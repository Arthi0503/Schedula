"""Unit tests for API layer endpoints in Schedula."""
import unittest
from app.main import health_check, root
from app.api.endpoints import (
    get_sample_timetable,
    detect_conflicts,
    resolve_conflicts,
    download_timetable_template
)
from app.models.schemas import ScheduleSlot

class TestApiEndpoints(unittest.TestCase):
    def test_health_check(self):
        res = health_check()
        self.assertEqual(res.get("status"), "healthy")
        self.assertEqual(res.get("service"), "Schedula Timetable API")

    def test_root_endpoint(self):
        res = root()
        self.assertEqual(res.get("name"), "Schedula Timetable API")
        self.assertIn("docs_url", res)

    def test_sample_timetable_endpoint(self):
        slots = get_sample_timetable()
        self.assertIsInstance(slots, list)
        self.assertGreater(len(slots), 5)
        self.assertEqual(slots[0].course_code, "CS101")

    def test_detect_conflicts_endpoint(self):
        slots = get_sample_timetable()
        report = detect_conflicts(slots)
        self.assertGreater(report.total_slots, 0)
        self.assertGreater(report.total_conflicts, 0)
        self.assertIn("CS-Year-1", [c.affected_entities[0] for c in report.conflicts if c.affected_entities])

    def test_resolve_conflicts_endpoint(self):
        slots = get_sample_timetable()
        res = resolve_conflicts(slots)
        self.assertGreater(res.resolved_count, 0)
        self.assertGreater(len(res.resolutions), 0)

    def test_template_download_endpoint(self):
        res = download_timetable_template()
        self.assertEqual(res.media_type, "text/csv")
        self.assertIn(b"Course Code", res.body)

if __name__ == "__main__":
    unittest.main()

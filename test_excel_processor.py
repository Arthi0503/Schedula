"""Unit tests for Excel and CSV processing in Schedula."""
import unittest
from app.services.excel_processor import ExcelProcessor, CANONICAL_HEADERS, SAMPLE_TIMETABLE_ROWS
from app.services.conflict_detector import ConflictDetector

class TestExcelProcessor(unittest.TestCase):
    def test_canonical_headers_matching(self):
        headers = ["Course Code", "Subject Name", "Professor", "Hall", "Day", "From", "To", "Batch", "Strength", "Max Capacity", "Type"]
        col_map = ExcelProcessor.match_column_indices(headers)
        self.assertEqual(col_map.get("course_code"), 0)
        self.assertEqual(col_map.get("course_name"), 1)
        self.assertEqual(col_map.get("instructor"), 2)
        self.assertEqual(col_map.get("room"), 3)
        self.assertEqual(col_map.get("day"), 4)
        self.assertEqual(col_map.get("start_time"), 5)
        self.assertEqual(col_map.get("end_time"), 6)
        self.assertEqual(col_map.get("student_group"), 7)

    def test_csv_template_generation_and_parsing(self):
        csv_text = ExcelProcessor.generate_csv_template()
        self.assertIn("Course Code", csv_text)
        self.assertIn("CS101", csv_text)

        slots = ExcelProcessor.parse_csv_content(csv_text)
        self.assertEqual(len(slots), len(SAMPLE_TIMETABLE_ROWS))
        
        # Verify first slot values
        first = slots[0]
        self.assertEqual(first.course_code, "CS101")
        self.assertEqual(first.instructor_name, "Dr. Alan Turing")
        self.assertEqual(first.room_id, "Hall-A")
        self.assertEqual(first.day_of_week, "Monday")
        self.assertEqual(first.start_time, "08:30")
        self.assertEqual(first.end_time, "10:00")
        self.assertEqual(first.enrollment, 95)
        self.assertEqual(first.room_capacity, 120)

    def test_curated_sample_detects_conflicts(self):
        csv_text = ExcelProcessor.generate_csv_template()
        slots = ExcelProcessor.parse_csv_content(csv_text)
        detector = ConflictDetector()
        report = detector.detect_conflicts(slots)

        # The sample has deliberate room clash, instructor clash, group clash, and capacity overflow
        self.assertGreater(report.total_conflicts, 0)
        self.assertGreater(report.critical_count, 0)
        self.assertGreater(report.warning_count, 0)

    def test_excel_export_returns_valid_bytes(self):
        csv_text = ExcelProcessor.generate_csv_template()
        slots = ExcelProcessor.parse_csv_content(csv_text)
        detector = ConflictDetector()
        report = detector.detect_conflicts(slots)

        workbook_bytes = ExcelProcessor.generate_excel_workbook(slots, report)
        self.assertIsInstance(workbook_bytes, bytes)
        self.assertGreater(len(workbook_bytes), 100)

if __name__ == "__main__":
    unittest.main()

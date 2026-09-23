"""Unit tests for Timetable Conflict Detection Engine."""
import unittest
from app.models.schemas import ScheduleSlot, ConflictType, ConflictSeverity
from app.services.conflict_detector import ConflictDetector, is_overlapping, time_to_minutes, minutes_to_time

class TestConflictDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ConflictDetector()

    def test_time_conversions(self):
        self.assertEqual(time_to_minutes("00:00"), 0)
        self.assertEqual(time_to_minutes("08:30"), 510)
        self.assertEqual(time_to_minutes("14:45"), 885)
        self.assertEqual(minutes_to_time(510), "08:30")
        self.assertEqual(minutes_to_time(885), "14:45")

    def test_interval_overlaps(self):
        # Back to back: 09:00-10:00 and 10:00-11:00 -> NOT overlapping
        self.assertFalse(is_overlapping(540, 600, 600, 660))
        # Completely disjoint
        self.assertFalse(is_overlapping(500, 550, 600, 700))
        # Partial overlap: 09:00-10:30 and 10:00-11:00 -> Overlaps
        self.assertTrue(is_overlapping(540, 630, 600, 660))
        # Subset: 09:00-11:00 and 09:30-10:30 -> Overlaps
        self.assertTrue(is_overlapping(540, 660, 570, 630))
        # Identical
        self.assertTrue(is_overlapping(540, 600, 540, 600))

    def test_room_clash_detection(self):
        slot1 = ScheduleSlot(
            id="slot-1",
            course_code="CS101",
            course_name="Programming I",
            instructor_name="Dr. Smith",
            room_id="Hall-A",
            day_of_week="Monday",
            start_time="09:00",
            end_time="10:30",
            student_group="CS-Batch-1",
            enrollment=50,
            room_capacity=100
        )
        slot2 = ScheduleSlot(
            id="slot-2",
            course_code="MATH101",
            course_name="Calculus",
            instructor_name="Dr. Jones",
            room_id="Hall-A",  # Same room!
            day_of_week="Monday",  # Same day!
            start_time="10:00",  # Overlapping time: 10:00 to 11:30
            end_time="11:30",
            student_group="MATH-Batch-1",
            enrollment=40,
            room_capacity=100
        )

        report = self.detector.detect_conflicts([slot1, slot2])
        self.assertEqual(report.total_conflicts, 1)
        self.assertEqual(report.critical_count, 1)
        self.assertEqual(report.conflicts[0].conflict_type, ConflictType.ROOM_CLASH.value)
        self.assertIn("slot-1", report.conflicted_slot_ids)
        self.assertIn("slot-2", report.conflicted_slot_ids)

    def test_instructor_clash_detection(self):
        slot1 = ScheduleSlot(
            id="slot-3",
            course_code="CS201",
            course_name="Algorithms",
            instructor_name="Prof. Turing",
            room_id="Room-101",
            day_of_week="Tuesday",
            start_time="14:00",
            end_time="15:30",
            student_group="CS-Batch-A",
            enrollment=30,
            room_capacity=50
        )
        slot2 = ScheduleSlot(
            id="slot-4",
            course_code="CS301",
            course_name="Advanced Theory",
            instructor_name="Prof. Turing",  # Same instructor!
            room_id="Room-102",  # Different room
            day_of_week="Tuesday",
            start_time="14:30",  # Overlaps 14:30 to 16:00
            end_time="16:00",
            student_group="CS-Batch-B",
            enrollment=25,
            room_capacity=50
        )

        report = self.detector.detect_conflicts([slot1, slot2])
        self.assertEqual(report.total_conflicts, 1)
        self.assertEqual(report.conflicts[0].conflict_type, ConflictType.INSTRUCTOR_CLASH.value)

    def test_student_group_clash_detection(self):
        slot1 = ScheduleSlot(
            id="slot-5",
            course_code="ENG101",
            course_name="English",
            instructor_name="Dr. Angelou",
            room_id="Room-201",
            day_of_week="Wednesday",
            start_time="11:00",
            end_time="12:30",
            student_group="Year-1-Common",
            enrollment=40,
            room_capacity=60
        )
        slot2 = ScheduleSlot(
            id="slot-6",
            course_code="HIST101",
            course_name="History",
            instructor_name="Prof. Durant",
            room_id="Room-202",
            day_of_week="Wednesday",
            start_time="11:30",
            end_time="13:00",
            student_group="Year-1-Common",  # Same cohort!
            enrollment=40,
            room_capacity=60
        )

        report = self.detector.detect_conflicts([slot1, slot2])
        self.assertEqual(report.total_conflicts, 1)
        self.assertEqual(report.conflicts[0].conflict_type, ConflictType.GROUP_CLASH.value)

    def test_capacity_overflow_warning(self):
        slot = ScheduleSlot(
            id="slot-7",
            course_code="BIO101",
            course_name="Biology",
            instructor_name="Dr. Darwin",
            room_id="Lab-A",
            day_of_week="Thursday",
            start_time="09:00",
            end_time="10:30",
            student_group="Bio-Year-1",
            enrollment=85,  # Exceeds capacity!
            room_capacity=50
        )

        report = self.detector.detect_conflicts([slot])
        self.assertEqual(report.total_conflicts, 1)
        self.assertEqual(report.warning_count, 1)
        self.assertEqual(report.critical_count, 0)
        self.assertEqual(report.conflicts[0].conflict_type, ConflictType.CAPACITY_OVERFLOW.value)

    def test_no_conflict_clean_schedule(self):
        # Back-to-back classes in same room
        slot1 = ScheduleSlot(
            id="slot-8",
            course_code="CS101",
            course_name="CS 1",
            instructor_name="Teacher A",
            room_id="Room-1",
            day_of_week="Friday",
            start_time="09:00",
            end_time="10:00",
            student_group="Group-A",
            enrollment=30,
            room_capacity=50
        )
        slot2 = ScheduleSlot(
            id="slot-9",
            course_code="CS102",
            course_name="CS 2",
            instructor_name="Teacher B",
            room_id="Room-1",
            day_of_week="Friday",
            start_time="10:00",  # Starts right after slot1 ends
            end_time="11:00",
            student_group="Group-B",
            enrollment=30,
            room_capacity=50
        )

        report = self.detector.detect_conflicts([slot1, slot2])
        self.assertEqual(report.total_conflicts, 0)
        self.assertEqual(report.health_score, 100)

    def test_conflict_resolution_suggestions(self):
        # Room clash
        slot1 = ScheduleSlot(
            id="slot-10",
            course_code="CS101",
            course_name="CS 1",
            instructor_name="Teacher A",
            room_id="Room-201",
            day_of_week="Monday",
            start_time="09:00",
            end_time="10:30",
            student_group="Group-A",
            enrollment=30,
            room_capacity=60
        )
        slot2 = ScheduleSlot(
            id="slot-11",
            course_code="CS102",
            course_name="CS 2",
            instructor_name="Teacher B",
            room_id="Room-201",
            day_of_week="Monday",
            start_time="09:00",
            end_time="10:30",
            student_group="Group-B",
            enrollment=30,
            room_capacity=60
        )

        resolutions = self.detector.resolve_conflicts([slot1, slot2])
        self.assertGreaterEqual(resolutions.resolved_count, 1)
        res = resolutions.resolutions[0]
        self.assertIsNotNone(res.suggested_room)

if __name__ == "__main__":
    unittest.main()

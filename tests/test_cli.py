from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
INIT_SEMESTER = REPO / "scripts" / "init_semester.py"
INIT_COURSE = REPO / "scripts" / "init_course.py"
VALIDATE = REPO / "scripts" / "validate_vault.py"


class IndexContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "TEST27"

    def run_cli(self, script: Path, *arguments: object) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(script), *(str(argument) for argument in arguments)],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )

    def initialize_semester(self) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            INIT_SEMESTER,
            "--root", self.root,
            "--term", "TEST27",
            "--timezone", "America/Chicago",
        )

    def initialize_course(self) -> subprocess.CompletedProcess[str]:
        return self.run_cli(
            INIT_COURSE,
            "--semester-root", self.root,
            "--course-id", "TEST101",
            "--title", "Distributed Example",
        )

    def test_every_scope_has_an_index_and_initialization_is_idempotent(self) -> None:
        self.assertEqual(self.initialize_semester().returncode, 0)
        self.assertEqual(self.initialize_course().returncode, 0)
        course_index = self.root / "Courses" / "TEST101" / "Index.md"
        course_index.write_text("USER INDEX\n", encoding="utf-8")
        self.assertEqual(self.initialize_semester().returncode, 0)
        self.assertEqual(self.initialize_course().returncode, 0)
        self.assertTrue((self.root / "Index.md").is_file())
        self.assertTrue((self.root / "Overview" / "Index.md").is_file())
        self.assertTrue((self.root / "Courses" / "TEST101" / "learning" / "deadlines").is_dir())
        self.assertTrue((self.root / "Courses" / "TEST101" / "templates" / "Deadline.md").is_file())
        self.assertEqual(course_index.read_text(encoding="utf-8"), "USER INDEX\n")

    def test_validator_rejects_a_missing_index(self) -> None:
        self.assertEqual(self.initialize_semester().returncode, 0)
        self.assertEqual(self.initialize_course().returncode, 0)
        (self.root / "Overview" / "Index.md").unlink()
        result = self.run_cli(VALIDATE, "--semester-root", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing-root-item", result.stdout)
        self.assertIn("Overview/Index.md", result.stdout)

    def test_initialized_workspace_validates_cleanly(self) -> None:
        self.assertEqual(self.initialize_semester().returncode, 0)
        self.assertEqual(self.initialize_course().returncode, 0)
        result = self.run_cli(VALIDATE, "--semester-root", self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("errors=0 warnings=0", result.stdout)

    def test_verified_deadline_with_evidence_validates_cleanly(self) -> None:
        self.assertEqual(self.initialize_semester().returncode, 0)
        self.assertEqual(self.initialize_course().returncode, 0)
        deadline = self.root / "Courses" / "TEST101" / "learning" / "deadlines" / "HW1.md"
        deadline.write_text(
            "---\n"
            "type: deadline\n"
            "course: TEST101\n"
            "deadline_id: TEST101/deadline/hw1\n"
            "title: HW1\n"
            "deadline_kind: homework\n"
            "date_status: exact\n"
            "due_date: 2027-09-20\n"
            'due_time: "23:59"\n'
            "timezone: America/Chicago\n"
            "status: pending\n"
            "verification_status: verified\n"
            "source_path: Course.md\n"
            'source_locator: "Assessments > HW1"\n'
            "verified_at: 2027-08-25\n"
            "---\n",
            encoding="utf-8",
        )
        result = self.run_cli(VALIDATE, "--semester-root", self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_rejects_unsupported_or_malformed_deadline(self) -> None:
        self.assertEqual(self.initialize_semester().returncode, 0)
        self.assertEqual(self.initialize_course().returncode, 0)
        deadline = self.root / "Courses" / "TEST101" / "learning" / "deadlines" / "Bad.md"
        deadline.write_text(
            "---\n"
            "type: deadline\n"
            "course: TEST101\n"
            "deadline_id: TEST101/deadline/bad\n"
            "title: Bad deadline\n"
            "deadline_kind: homework\n"
            "date_status: exact\n"
            "due_date: 09/20/2027\n"
            'due_time: "8am"\n'
            "status: pending\n"
            "verification_status: verified\n"
            "---\n",
            encoding="utf-8",
        )
        result = self.run_cli(VALIDATE, "--semester-root", self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("deadline-date", result.stdout)
        self.assertIn("deadline-time", result.stdout)
        self.assertIn("deadline-timezone", result.stdout)
        self.assertIn("deadline-evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()

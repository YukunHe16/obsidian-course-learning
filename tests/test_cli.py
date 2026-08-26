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


if __name__ == "__main__":
    unittest.main()

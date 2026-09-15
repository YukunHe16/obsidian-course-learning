from __future__ import annotations
import datetime as dt
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from vault_model import frontmatter, resolve_link, sha256, course_fingerprint
from rebuild_overview import build_summary, write_summary
from validate_vault import validate_reading, resolve_links, validate_course


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name) / "TEST101"
        self.vault.mkdir()
        self.note("Course", "type: course\ncourse_id: TEST101\nschema_version: 2\nexam_dates:\n  []")
        self.note("wiki/index", "type: knowledge-index", "[[wiki/lectures/L1|开始]]")
        self.note("learning/Progress", "type: learning-progress\nresume_link:\nupdated_at:",
                  "## 待澄清问题\n\n暂无记录。\n")
        raw = self.vault / "raw/slides.pdf"
        raw.parent.mkdir(parents=True)
        raw.write_bytes(b"SYNTHETIC SOURCE FIXTURE")
        self.note("wiki/lectures/L1",
                  f"type: lecture\ncourse: TEST101\nlecture_no: 1\nreading_role: primary\nstatus: active\nchecked_at: 2027-01-02\nsource_pdf: raw/slides.pdf\nsource_hash: {sha256(raw)}",
                  "# L1\n\n## 数据流\n\nSource: [[raw/slides.pdf#page=1|Slide 1]]\n")

    def note(self, name, properties, body=""):
        path = self.vault / (name + ".md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + properties + "\n---\n\n" + body + "\n", encoding="utf-8")
        return path

    def test_empty_progress_is_not_learning_evidence(self):
        issues = []
        validate_reading(self.vault, issues)
        self.assertEqual(issues, [])
        summary = build_summary(self.vault, "America/Chicago", dt.datetime(2027, 1, 2))
        self.assertIn("open_question_count: 0", summary)
        self.assertIn("last_studied: \n", summary)
        self.assertNotIn("average_mastery", summary)

    def test_real_misconception_and_resolution_keep_session_evidence(self):
        self.note("learning/sessions/s1",
                  'type: study-session\ncourse: TEST101\ndate: 2027-01-02\nsource_lecture: "[[wiki/lectures/L1]]"\nevidence_summary: Confused record and partition',
                  "## Q1\n\nSynthetic test response.")
        p = self.note("learning/Progress",
                      'type: learning-progress\nresume_link: "[[wiki/lectures/L1#数据流]]"\nupdated_at: 2027-01-02',
                      "## 待澄清问题\n\n- [ ] TEST101/M001 · 分组混淆 [[learning/sessions/s1#Q1|证据]]\n")
        issues = []
        validate_reading(self.vault, issues)
        self.assertEqual(issues, [])
        self.assertIn("open_question_count: 1", build_summary(self.vault, "America/Chicago"))
        p.write_text(p.read_text().replace("- [ ]", "- [x]"))
        self.assertIn("open_question_count: 0", build_summary(self.vault, "America/Chicago"))
        self.assertTrue((self.vault / "learning/sessions/s1.md").exists())

    def test_bad_bookmark_and_fabricated_session_are_rejected(self):
        self.note("learning/Progress",
                  'type: learning-progress\nresume_link: "[[wiki/lectures/L1#不存在]]"\nupdated_at: 2027-01-02',
                  "## 待澄清问题\n\n- [ ] TEST101/M001 无证据\n")
        self.note("learning/sessions/empty", "type: study-session\ndate: 2027-01-02")
        issues = []
        validate_reading(self.vault, issues)
        codes = {i["code"] for i in issues}
        self.assertTrue({"progress-link", "progress-evidence", "session-evidence", "session-lecture"} <= codes)

    def test_checked_notes_need_sources_and_valid_return_links(self):
        p = self.note("wiki/concepts/Grouping",
                      "type: concept\nconcept_id: TEST101/grouping\nstatus: active\nchecked_at: 2027-01-02",
                      "# 分组")
        issues = []
        validate_reading(self.vault, issues)
        self.assertTrue({"checked-source", "missing-return-link"} <= {i["code"] for i in issues})
        self.note("wiki/concepts/Grouping",
                  'type: concept\nconcept_id: TEST101/grouping\nstatus: active\nchecked_at: 2027-01-02\nreturn_to:\n  - "[[wiki/lectures/L1#数据流]]"',
                  "Source: [[raw/slides.pdf#page=1|Slide 1]]")
        issues = []
        validate_reading(self.vault, issues)
        self.assertEqual(issues, [])

    def test_section_table_alias_and_question_links(self):
        p = self.note("learning/questions/Q", "type: question-set",
                      "## Q1 · 分组\n\n| 参考 |\n| --- |\n| [[wiki/lectures/L1#数据流\\|中文]] |\n")
        self.assertIsNone(resolve_link(self.vault, p, "wiki/lectures/L1#数据流")[1])
        self.assertIsNone(resolve_link(self.vault, p, "#Q1 · 分组")[1])
        self.assertEqual(resolve_link(self.vault, p, "#Q2")[1], "broken-fragment")
        issues = []
        resolve_links(self.vault, issues)
        self.assertEqual(issues, [])

    def test_summary_is_idempotent_and_does_not_mutate_course(self):
        before = course_fingerprint(self.vault)
        path = Path(self.tmp.name) / "Overview/courses/TEST101.md"
        first = build_summary(self.vault, "America/Chicago", dt.datetime(2027, 1, 2, 10))
        self.assertTrue(write_summary(path, first))
        stat = path.stat().st_mtime_ns
        later = build_summary(self.vault, "America/Chicago", dt.datetime(2027, 1, 2, 15))
        self.assertFalse(write_summary(path, later))
        self.assertEqual(path.stat().st_mtime_ns, stat)
        self.assertEqual(course_fingerprint(self.vault), before)
        self.assertTrue(write_summary(path, build_summary(self.vault, "America/Chicago", dt.datetime(2027, 1, 3))))

    def test_deadlines_do_not_invent_dates_for_recurring_work(self):
        self.note("learning/deadlines/hw", "type: deadline\nstatus: pending\ndate_status: exact\ndue_date: 2027-01-05\ntitle: Homework")
        self.note("learning/deadlines/video", "type: deadline\nstatus: pending\ndate_status: unpublished\ntitle: Video")
        self.note("learning/deadlines/lab", "type: deadline\nstatus: pending\ndate_status: recurring\ndue_date: 2027-01-04\ntitle: Lab")
        summary = build_summary(self.vault, "America/Chicago", dt.datetime(2027, 1, 2))
        self.assertIn("upcoming_deadline_count: 1", summary)
        self.assertIn('next_deadline: "2027-01-05"', summary)

    def test_existing_optional_scores_and_new_unscored_concepts(self):
        for extra, expected in [("", False), ("\nmastery: 2\nreview_stage: 1", False), ("\nmastery: 9", True)]:
            self.note("wiki/concepts/C", "type: concept\ncourse: TEST101\nconcept_id: TEST101/c\nstatus: draft" + extra)
            issues = []
            validate_course(self.vault, issues, {}, {})
            self.assertEqual(any(i["code"] == "mastery-range" for i in issues), expected)


if __name__ == "__main__":
    unittest.main()

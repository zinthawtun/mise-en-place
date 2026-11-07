#!/usr/bin/env python3
"""Tests for generate_register.py and check_links.py, using examples/shortlink as the fixture.

Run: python3 skills/mise-en-place/scripts/test_scripts.py
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLE = HERE.parents[2] / "examples" / "shortlink"
REGISTER = HERE / "generate_register.py"
LINKS = HERE / "check_links.py"


def run(script, *args, cwd):
    p = subprocess.run([sys.executable, str(script), *args], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class RegisterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(EXAMPLE, self.tmp / "p")
        self.root = self.tmp / "p"
        self.bp = self.root / "blueprint"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, rel, old, new):
        f = self.bp / rel
        text = f.read_text(encoding="utf-8")
        self.assertIn(old, text)
        f.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_example_passes_and_check_is_idempotent(self):
        code, out = run(REGISTER, "--scan", "tests", cwd=self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("withdrawn: 1", out)
        code, out = run(REGISTER, "--check", cwd=self.root)
        self.assertEqual(code, 0, out)

    def test_check_fails_when_register_is_stale(self):
        run(REGISTER, cwd=self.root)
        self.edit("02-specs/spec-links.md", "| S | P2 | §2 b6 |", "| C | P2 | §2 b6 |")
        code, out = run(REGISTER, "--check", cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("out of date", out)

    def test_budget_fails_only_when_live_count_exceeds_it(self):
        code, out = run(REGISTER, "--budget", "1", cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("requirement budget exceeded", out)
        code, out = run(REGISTER, "--budget", "100", cwd=self.root)
        self.assertEqual(code, 0, out)

    def test_duplicate_id_fails(self):
        self.edit("02-specs/spec-links.md", "| FR-LNK-004 |", "| FR-LNK-003 |")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("duplicate ID FR-LNK-003", out)

    def test_gated_must_without_ac_fails_but_later_phase_is_allowed(self):
        self.edit("02-specs/spec-links.md", "- **AC-LNK-003.1**", "- **Removed**")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("Must without AC: FR-LNK-003", out)
        self.assertNotIn("Must without AC: FR-RED-003", out)
        code, out = run(REGISTER, "--ac-phases", "", cwd=self.root)
        self.assertEqual(code, 0, out)

    def test_nfr_takes_phase_from_spec_front_matter(self):
        self.edit("02-specs/spec-redirect.md", "- **AC-NFR-RED-001.1**", "- **Removed**")
        code, out = run(REGISTER, cwd=self.root)
        self.assertIn("Must without AC: NFR-RED-001 (P1", out)

    def test_backlog_phase_mismatch_and_unknown_id_fail(self):
        self.edit("04-plan/backlog.md", "| FR-SEC-001, FR-SEC-002 |", "| FR-SEC-001, FR-SEC-002, FR-RED-003, FR-XYZ-999 |")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("SL-1-03 (P1) satisfies FR-RED-003 scheduled for P2", out)
        self.assertIn("SL-1-03 references unknown FR-XYZ-999", out)

    def test_ac_needing_later_phase_requirement_fails(self):
        self.edit("02-specs/spec-links.md", "- **AC-LNK-003.1**", "- **AC-LNK-003.1** Needs: FR-RED-003.")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("AC of FR-LNK-003 (P1) needs FR-RED-003 scheduled for P2", out)

    def test_gated_must_missing_from_backlog_warns(self):
        self.edit("04-plan/backlog.md", "| FR-SEC-001, FR-SEC-002 |", "| FR-SEC-002 |")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("WARN  gated Must not in backlog: FR-SEC-001", out)

    def test_scan_detects_unknown_withdrawn_and_ac_named_tests(self):
        code, out = run(REGISTER, "--scan", "tests", cwd=self.root)
        self.assertNotIn("no AC-named test: FR-RED-001", out)
        self.assertIn("no AC-named test: FR-LNK-001", out)
        (self.root / "tests" / "test_bad.py").write_text(
            "def test_AC_ZZZ_001_1_x(): ...\n# satisfies FR-SEC-003\n", encoding="utf-8")
        code, out = run(REGISTER, "--scan", "tests", cwd=self.root)
        self.assertEqual(code, 1, out)
        self.assertIn("unknown FR-ZZZ-001", out)
        self.assertIn("Withdrawn FR-SEC-003", out)

    def test_audit_only_before_traceability_exists(self):
        (self.bp / "traceability.md").unlink()
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("audit only", out)
        self.assertFalse((self.bp / "traceability.md").exists())
        self.edit("02-specs/spec-links.md", "- **AC-LNK-003.1**", "- **Removed**")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 1, out)
        code, out = run(REGISTER, "--check", cwd=self.root)
        self.assertIn("does not exist", out)

    def test_status_column_drives_register_and_withdrawal(self):
        run(REGISTER, cwd=self.root)
        reg = (self.bp / "traceability.md").read_text(encoding="utf-8")
        self.assertIn("| FR-LNK-004 | S | P2 | Draft |", reg)
        self.assertIn("| FR-SEC-003 | M | P1 | Withdrawn |", reg)
        self.edit("02-specs/spec-links.md", "| M | P1 | §2 b1 | Agreed |", "| M | P1 | §2 b1 | Withdrawn |")
        self.edit("02-specs/spec-links.md", "- **AC-LNK-001.1**", "- **Removed**")
        code, out = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 0, out)

    def test_missing_marker_is_usage_error(self):
        self.edit("traceability.md", "## 3. Requirement register", "## 3. Register")
        code, _ = run(REGISTER, cwd=self.root)
        self.assertEqual(code, 2)


class LinkTests(unittest.TestCase):
    def test_example_has_no_broken_links(self):
        code, out = run(LINKS, str(EXAMPLE), cwd=HERE)
        self.assertEqual(code, 0, out)

    def test_detects_broken_link_and_ignores_code(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "a b.md").write_text("x", encoding="utf-8")
            Path(d, "doc.md").write_text(
                "[ok](./a%20b.md) [ok2](<./a b.md>) [web](https://x.y) [anchor](#top)\n"
                "`[skip](./nope1.md)`\n```\n[skip](./nope2.md)\n```\n[bad](./missing.md)\n",
                encoding="utf-8")
            code, out = run(LINKS, d, cwd=d)
            self.assertEqual(code, 1, out)
            self.assertIn("missing.md", out)
            self.assertNotIn("nope", out)
            self.assertIn("Broken links: 1", out)

    def test_help(self):
        code, out = run(LINKS, "--help", cwd=HERE)
        self.assertEqual(code, 0)
        self.assertIn("usage", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)

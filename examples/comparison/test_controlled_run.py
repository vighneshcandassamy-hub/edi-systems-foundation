"""Launch gate and mechanical reporting checks; no world or provider imported."""
from pathlib import Path
import tempfile
import unittest
from offline_runner import BoundaryError
from responses_adapter import SpendPolicy
from controlled_run import run, validate_launch, write_comparison

class DriverChecks(unittest.TestCase):
    def test_default_run_cannot_create_a_world_or_call_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"not-created"
            with self.assertRaises(BoundaryError):run(Path(tmp),target,post=lambda *_:self.fail("network called"))
            self.assertFalse(target.exists())
    def test_enabled_flag_alone_is_insufficient_authorization(self):
        with self.assertRaises(BoundaryError):validate_launch(SpendPolicy(approved_by_user=True),{},lambda *_:None)
    def test_report_keeps_incomplete_arm_visible_without_fabricating_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=write_comparison(tmp,{"terminal":{"baseline":"yielded","edi":"completed"},
                "outcome":{"baseline":{"years_elapsed":1},"edi":{"years_elapsed":5,"final_report":{"conclusion":"Fixture explanation only"}}}}, {})
            report=(Path(tmp)/"comparison.md").read_text()
            self.assertIn("No accepted final report",report)
            self.assertIn("Fixture explanation only",report)
            self.assertFalse((Path(tmp)/"baseline-participant-report.md").exists())
            self.assertEqual(result["limits"]["replications"],1)

if __name__=="__main__":unittest.main(verbosity=2)

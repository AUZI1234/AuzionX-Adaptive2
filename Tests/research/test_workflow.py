"""Workflow contract tests; fixtures are not market evidence."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from datetime import datetime, timezone
from Research.data.validate_ticks import Tick, validate_ticks

class WorkflowTests(unittest.TestCase):
    def test_malformed_csv_is_reported_not_raised_by_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); source=root/'bad.csv'; report=root/'report.json'
            source.write_text('wrong\nvalue\n', encoding='utf-8')
            result=subprocess.run([sys.executable, 'Research/data/validate_ticks.py', str(source), '--report', str(report)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(json.loads(report.read_text())['valid'])

    def test_abnormal_spread_and_zero_movement_are_reported(self):
        base=datetime(2024,1,1,tzinfo=timezone.utc)
        ticks=[Tick(base, 1, 2), Tick(base.replace(second=1), 1, 5)]
        report=validate_ticks(ticks, max_spread=2)
        self.assertEqual(report['zero_movement_ticks'], 0)
        self.assertEqual(report['abnormal_spreads'], 1)

if __name__ == '__main__': unittest.main()

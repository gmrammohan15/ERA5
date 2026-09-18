import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zero_simulator import (  # noqa: E402
    STAGES,
    VirtualCluster,
    correctness_check,
    memory_report,
    shard_sizes,
)


class ZeroSimulatorTests(unittest.TestCase):
    def test_virtual_cluster_has_32_ranks(self):
        cluster = VirtualCluster(101, 32)
        self.assertEqual(len(cluster.ranks), 32)
        self.assertEqual(sum(shard_sizes(101, 32)), 101)

    def test_memory_decreases_with_each_stage(self):
        values = [memory_report(1_000_000, 32, stage).model_state_bytes_per_rank for stage in STAGES]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_zero3_adds_parameter_communication(self):
        from zero_simulator import communication_report

        zero2 = communication_report(1_000_000, 32, "zero2")
        zero3 = communication_report(1_000_000, 32, "zero3")
        self.assertGreater(zero3.total_bytes_per_rank, zero2.total_bytes_per_rank)

    def test_reference_update_is_equivalent(self):
        result = correctness_check()
        self.assertTrue(result["all_close"])


if __name__ == "__main__":
    unittest.main()

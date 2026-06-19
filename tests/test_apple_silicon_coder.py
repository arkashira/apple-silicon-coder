import pytest
from apple_silicon_coder import optimize_for_apple_silicon, OptimizationResult, validate_optimization_result

def test_optimize_for_apple_silicon_happy_path():
    hardware_config = {"clock_speed": 2, "num_cores": 100}
    result = optimize_for_apple_silicon(hardware_config)
    assert result.throughput == 200
    assert result.reasoning_capabilities

def test_optimize_for_apple_silicon_edge_case():
    hardware_config = {"clock_speed": 1, "num_cores": 100}
    result = optimize_for_apple_silicon(hardware_config)
    assert result.throughput == 100
    assert not result.reasoning_capabilities

def test_validate_optimization_result_happy_path():
    result = OptimizationResult(200, True)
    assert validate_optimization_result(result)

def test_validate_optimization_result_edge_case():
    result = OptimizationResult(100, False)
    assert not validate_optimization_result(result)

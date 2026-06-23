import pytest
from model_optimizer import ModelOptimizer, ModelConfig

@pytest.fixture
def model_config():
    return ModelConfig(tokens_per_second=200, inference_latency=0.5, cpu_gpu_usage=30)

@pytest.fixture
def model_optimizer(model_config):
    return ModelOptimizer(model_config)

def test_optimize_model(model_optimizer):
    tokens = [f"token_{i}" for i in range(1000)]
    model_optimizer.optimize_model(tokens)
    assert model_optimizer.get_throughput() >= 200

def test_get_inference_latency(model_optimizer):
    assert model_optimizer.get_inference_latency() <= 0.5

def test_get_cpu_gpu_usage(model_optimizer):
    assert model_optimizer.get_cpu_gpu_usage() <= 30

def test_edge_case_zero_tokens(model_optimizer):
    tokens = []
    model_optimizer.optimize_model(tokens)
    assert model_optimizer.get_throughput() == 0

import time
from dataclasses import dataclass
from typing import List

@dataclass
class ModelConfig:
    tokens_per_second: int
    inference_latency: float
    cpu_gpu_usage: float

class ModelOptimizer:
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.tokens_processed = 0
        self.start_time = time.time()

    def optimize_model(self, tokens: List[str]):
        for token in tokens:
            # Simulate model optimization
            time.sleep(self.model_config.inference_latency / len(tokens))
            self.tokens_processed += 1

    def get_throughput(self):
        elapsed_time = time.time() - self.start_time
        return self.tokens_processed / elapsed_time

    def get_inference_latency(self):
        return self.model_config.inference_latency

    def get_cpu_gpu_usage(self):
        return self.model_config.cpu_gpu_usage

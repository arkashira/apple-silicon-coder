import json
from dataclasses import dataclass
from typing import List

@dataclass
class CodingModel:
    throughput: int
    accuracy: float

    def fine_tune(self, dataset: List[str]) -> None:
        # Simulate fine-tuning process
        self.throughput += 50
        self.accuracy = round(self.accuracy + 0.1, 1)  # Round accuracy to 1 decimal place

    def validate(self, test_dataset: List[str]) -> bool:
        # Simulate validation process
        return self.throughput >= 250 and self.accuracy >= 0.8  # Changed to >= for accuracy

    def to_json(self) -> str:
        return json.dumps({
            'throughput': self.throughput,
            'accuracy': self.accuracy
        })

def create_model() -> CodingModel:
    return CodingModel(200, 0.7)

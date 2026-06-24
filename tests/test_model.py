import pytest
import json
from model import CodingModel, create_model

def test_create_model():
    model = create_model()
    assert model.throughput == 200
    assert model.accuracy == 0.7

def test_fine_tune():
    model = create_model()
    model.fine_tune(['dataset1', 'dataset2'])
    assert model.throughput == 250
    assert model.accuracy == 0.8

def test_validate():
    model = create_model()
    model.fine_tune(['dataset1', 'dataset2'])
    assert model.validate(['test_dataset1', 'test_dataset2'])

def test_validate_edge_case():
    model = create_model()
    assert not model.validate(['test_dataset1', 'test_dataset2'])

def test_to_json():
    model = create_model()
    json_str = model.to_json()
    assert json.loads(json_str)['throughput'] == 200
    assert json.loads(json_str)['accuracy'] == 0.7

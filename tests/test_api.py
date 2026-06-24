import time
import pytest
from api_server import process_request

def test_process_request_valid():
    tokens = [f"token{i}" for i in range(10)]
    data = {'tokens': tokens}
    result = process_request(data)
    assert 'response' in result
    assert result['response'] == list(reversed(tokens))

def test_process_request_empty():
    data = {'tokens': []}
    result = process_request(data)
    assert result['response'] == []

def test_process_request_invalid_type():
    data = {'tokens': 'not a list'}
    with pytest.raises(ValueError):
        process_request(data)

def test_process_request_too_many_tokens():
    data = {'tokens': ['t'] * 101}
    with pytest.raises(ValueError):
        process_request(data)

def test_process_request_non_string_token():
    data = {'tokens': ['a', 1, 'b']}
    with pytest.raises(ValueError):
        process_request(data)

def test_process_request_missing_tokens():
    data = {'foo': 'bar'}
    with pytest.raises(ValueError):
        process_request(data)

def test_process_request_performance():
    tokens = [f"token{i}" for i in range(100)]
    data = {'tokens': tokens}
    start = time.time()
    result = process_request(data)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 50, f"Processing took {elapsed_ms:.2f} ms, expected < 50 ms"
    assert result['response'] == list(reversed(tokens))

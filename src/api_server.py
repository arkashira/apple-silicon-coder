import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List

def process_request(data: Dict) -> Dict:
    """
    Process a JSON payload containing a list of tokens.

    Parameters
    ----------
    data : dict
        JSON object with a single key 'tokens' mapping to a list of strings.

    Returns
    -------
    dict
        JSON object with a single key 'response' mapping to the reversed list of tokens.

    Raises
    ------
    ValueError
        If the payload is invalid or violates constraints.
    """
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")
    if 'tokens' not in data:
        raise ValueError("Missing 'tokens' key")
    tokens = data['tokens']
    if not isinstance(tokens, list):
        raise ValueError("'tokens' must be a list")
    if len(tokens) > 100:
        raise ValueError("Maximum 100 tokens allowed")
    for t in tokens:
        if not isinstance(t, str):
            raise ValueError("All tokens must be strings")
    # Simulate a lightweight processing: reverse the list
    response_tokens = list(reversed(tokens))
    return {'response': response_tokens}

class SimpleHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler that accepts POST requests to /predict with JSON payloads.
    """
    def do_POST(self):
        if self.path != '/predict':
            self.send_error(404, "Not Found")
            return
        content_type = self.headers.get('Content-Type')
        if content_type != 'application/json':
            self.send_error(400, "Content-Type must be application/json")
            return
        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            self.send_error(400, "Invalid Content-Length")
            return
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        try:
            result = process_request(data)
        except ValueError as e:
            self.send_error(400, str(e))
            return
        response_body = json.dumps(result).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

def run_server(host: str = '127.0.0.1', port: int = 8000):
    """
    Start the HTTP server on the specified host and port.
    """
    server = HTTPServer((host, port), SimpleHandler)
    print(f"Serving on {host}:{port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server()

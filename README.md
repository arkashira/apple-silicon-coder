# apple-silicon-coder

A lightweight, local REST API that accepts JSON payloads containing a list of tokens and returns the tokens reversed. Designed to run on macOS as a background daemon.

## Features

- **Fast**: Processes a 100‑token request in under 50 ms.
- **JSON‑only**: Accepts only `application/json` payloads.
- **Daemon**: Can be started in the background (`python -m src.api_server &`).

## Usage

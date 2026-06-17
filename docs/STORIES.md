# STORIES.md  

## Project: apple-silicon-coder  
**Goal:** Deliver a coding LLM that runs natively on Apple Silicon (M1/M2/M3) with ≥ 200 tokens / second sustained throughput, low latency, and strong reasoning for code generation, debugging, and refactoring. The MVP will be a self‑contained CLI tool and VS Code extension that developers can install locally, without cloud dependencies.

---  

## Epics & Backlog  

| Epic | Description | Priority (MVP) |
|------|-------------|----------------|
| **E1 – Core Model Runtime** | Build the inference engine optimized for Apple Silicon, integrate with vLLM/SGLang, and expose a simple Python/CLI API. | ★★★★★ |
| **E2 – Model Packaging & Distribution** | Containerize the model, create Homebrew & pip installers, and generate signed macOS binaries. | ★★★★ |
| **E3 – Developer Interface (CLI)** | Provide a command‑line tool for code generation, completion, and debugging. | ★★★★ |
| **E4 – VS Code Extension** | Seamless editor integration: inline completions, doc‑string generation, and quick‑fix suggestions. | ★★★ |
| **E5 – Prompt & Context Management** | Implement prompt templates, token budgeting, and multi‑file context handling. | ★★★ |
| **E6 – Security & Sandbox** | Ensure generated code runs in a sandboxed environment; prevent leakage of proprietary prompts. | ★★★ |
| **E7 – Monitoring & Telemetry (opt‑in)** | Collect anonymous usage metrics to validate performance & pain‑point coverage. | ★★ |
| **E8 – Documentation & Samples** | Write quick‑start guides, API docs, and example notebooks. | ★★ |

---  

## User Stories  

### Epic E1 – Core Model Runtime  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E1‑01** | **As a** performance engineer, **I want** the model to achieve ≥ 200 tokens / second on an M2 Pro (8‑core) CPU, **so that** developers experience near‑real‑time code generation. | • Benchmark script reports ≥ 200 t/s on Apple Silicon (M1‑Pro, M2, M3). <br>• 95 %‑tile latency ≤ 150 ms for a 64‑token request. <br>• No memory‑thrashing (> 2 GB RAM) on a 16 GB MacBook. |
| **E1‑02** | **As a** devops lead, **I want** the runtime to use the Apple Metal GPU backend when available, **so that** we can double throughput on GPU‑enabled Macs. | • Detect Metal GPU at startup and fallback to CPU. <br>• GPU path yields ≥ 1.8× speedup vs CPU on benchmark. <br>• Graceful fallback if GPU driver missing. |
| **E1‑03** | **As a** security auditor, **I want** the runtime to run inference in a sandboxed process with limited file‑system access, **so that** user code cannot exfiltrate data. | • Inference runs in a separate `sandboxd` process with `nosuid`, `noexec` flags. <br>• Attempts to read/write outside `/tmp` are denied and logged. |
| **E1‑04** | **As a** product manager, **I want** the runtime to expose a Python API `generate(prompt: str, max_tokens: int) -> str`, **so that** downstream tools can call it easily. | • `apple_silicon_coder.generate()` returns a string. <br>• Raises `ValueError` for > max‑token budget. <br>• Includes optional `temperature` and `top_p` args. |

### Epic E2 – Model Packaging & Distribution  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E2‑01** | **As a** Mac user, **I want** to install the model via Homebrew (`brew install apple-silicon-coder`), **so that** setup is one command. | • Formula publishes latest version, verifies SHA‑256. <br>• Post‑install `apple-silicon-coder --version` prints semantic version. |
| **E2‑02** | **As a** Python developer, **I want** a `pip install apple-silicon-coder` wheel that bundles the model weights, **so that** I can use it in virtual environments. | • Wheel size ≤ 2 GB (weights compressed). <br>• Installation succeeds on Python 3.10‑3.12 on macOS 13+. |
| **E2‑03** | **As a** CI engineer, **I want** a Docker image (`ghcr.io/axentx/apple-silicon-coder:latest`) that runs on Apple‑silicon runners, **so that** we can run integration tests. | • Image builds on `--platform linux/arm64/v8`. <br>• `docker run … apple-silicon-coder --help` works. |

### Epic E3 – Developer Interface (CLI)  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E3‑01** | **As a** backend developer, **I want** a CLI command `asc generate -p "<prompt>" -t 128` that returns generated code, **so that** I can script code generation. | • Command prints JSON `{prompt, completion, tokens, latency}`. <br>• Exit code 0 on success, 1 on error. |
| **E3‑02** | **As a** tester, **I want** a `--dry-run` flag that validates prompt length and token budget without invoking the model, **so that** I can catch errors early. | • Returns warning if prompt > max tokens. <br>• No GPU/CPU usage logged. |
| **E3‑03** | **As a** developer, **I want** the CLI to support a `--file <path>` option that reads a source file, adds a context window, and returns a diff patch, **so that** I can get automated refactors. | • Outputs a unified diff that applies cleanly with `git apply`. <br>• Diff size ≤ max tokens. |
| **E3‑04** | **As a** DevOps engineer, **I want** the CLI to emit structured logs (JSON) to stdout when `--json` is set, **so that** we can pipe to monitoring tools. | • Logs contain timestamp, request_id, tokens, latency, error (if any). |

### Epic E4 – VS Code Extension  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E4‑01** | **As a** front‑end developer, **I want** inline completions triggered by `Ctrl+Space` that show suggestions from the local model, **so that** I stay in my editor. | • Completion appears within 200 ms after trigger. <br>• Up to 5 suggestions shown, each ≤ 64 tokens. |
| **E4‑02** | **As a** Pythonista, **I want** a “Generate docstring” command that inserts a docstring based on the function signature, **so that** documentation is consistent. | • Docstring follows PEP‑257, includes type hints. <br>• No more than 2 seconds latency. |
| **E4‑03** | **As a** security‑conscious user, **I want** the extension to run the model in a separate process and never send code to the internet, **so that** my proprietary code stays local. | • Network traffic captured by `lsof` shows none. <br>• Extension shows a lock icon when sandbox active. |
| **E4‑04** | **As a** power user, **I want** a settings UI to adjust temperature, top‑p, and max tokens, **so that** I can tune creativity vs. determinism. | • Changes take effect without restarting VS Code. <br>• Settings persisted in `settings.json`. |

### Epic E5 – Prompt & Context Management  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E5‑01** | **As a** senior engineer, **I want** the system to automatically chunk multi‑file projects into a sliding‑window context (max 2048 tokens), **so that** the model sees relevant code without exceeding limits. | • `asc context --project <dir>` produces a JSON with ordered chunks. <br>• Overlap between chunks is 20 %. |
| **E5‑02** | **As a** developer, **I want** built‑in prompt templates for “unit test generation”, “bug fix”, and “refactor”, **so that** I don’t have to craft prompts manually. | • `asc generate --template test` produces a valid test file that passes `pytest` 80 % of the time on benchmark suite. |
| **E5‑03** | **As a** product analyst, **I want** token‑usage reporting per request, **so that** we can monitor cost and enforce limits. | • CLI returns `tokens_used` field; VS Code status bar shows current usage. |

### Epic E6 – Security & Sandbox  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E6‑01** | **As a** compliance officer, **I want** the model weights to be signed with our internal code‑signing key, **so that** customers can verify integrity. | • `codesign -dv` on binary shows our certificate. <br>• Verification script fails on tampered files. |
| **E6‑02** | **As a** user, **I want** an opt‑out flag `--no-telemetry` that disables all anonymous reporting, **so that** I control data flow. | • When set, no `*.log` files are written to `~/.apple-silicon-coder/telemetry`. |

### Epic E7 – Monitoring & Telemetry (opt‑in)  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E7‑01** | **As a** product manager, **I want** aggregated, anonymized metrics (throughput, error rate) sent weekly to our endpoint, **so that** we can validate the “200 t/s” claim. | • Metrics payload includes only hashes, no PII. <br>• Endpoint returns 200 OK; retry logic on failure. |
| **E7‑02** | **As a** support engineer, **I want** a `asc healthcheck` command that reports GPU availability, model load time, and current version, **so that** I can diagnose user issues quickly. | • Returns JSON with fields `gpu: true/false`, `load_ms`, `version`. |

### Epic E8 – Documentation & Samples  

| # | Story | Acceptance Criteria |
|---|-------|----------------------|
| **E8‑01** | **As a** new user, **I want** a “Quick‑Start” markdown guide that gets me from installation to first code generation in < 5 minutes, **so that** onboarding is frictionless. | • Guide includes Homebrew install, `asc generate` example, and VS Code extension activation. |
| **E8‑02** | **As a** educator, **I want** a Jupyter notebook demonstrating prompt engineering and token budgeting, **so that** I can teach students. | • Notebook runs end‑to‑end on a fresh macOS VM without additional dependencies. |
| **E8‑03** | **As a** developer, **I want** API reference generated with `mkdocs` and hosted on `docs.axentx.com/apple-silicon-coder`, **so that** I can look up options offline. | • Docs build passes CI, includes code samples for each CLI flag. |

---  

## MVP Scope (Stories to ship in Release 1.0)

1. **E1‑01**, **E1‑02**, **E1‑04** – Core runtime with performance guarantees and Python API.  
2. **E2‑01**, **E2‑02** – Homebrew & pip distribution.  
3. **E3‑01**, **E3‑02**, **E3‑03** – Fully functional CLI with generation, dry‑run, and diff output.  
4. **E4‑01**, **E4‑02**, **E4‑03** – VS Code inline completions, docstring generation, and sandbox enforcement.  
5. **E5‑01**, **E5‑02** – Prompt templates and automatic context chunking.  
6. **E6‑01**, **E6‑02** – Signed binaries and telemetry opt‑out.  
7. **E8‑01** – Quick‑Start guide.

All other stories are planned for subsequent minor releases (1.1‑1.3).  

---  

*Prepared by the Apple Silicon Coder product team – 2026‑06‑17*

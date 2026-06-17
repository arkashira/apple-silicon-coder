# TECH_SPEC.md  
**Project:** apple-silicon-coder  
**Owner:** AxentX – Product Engineering Lead  
**Status:** Draft (ready for review)  
**Last Updated:** 2026‑06‑17  

---  

## 1. Overview  

**apple-silicon-coder** is a large‑language‑model (LLM) inference service optimized for Apple Silicon (M‑series) CPUs/NPUs. It delivers **≥ 200 tokens / second** throughput on a single Apple Silicon device while preserving strong reasoning capabilities. The service is built on top of the **vLLM** inference engine, with custom kernels and quantization pipelines that exploit the Apple Neural Engine (ANE) via the **Core ML** runtime.  

The product is intended for developers who need on‑device code generation, refactoring, and debugging assistance without incurring cloud latency or cost.  

---  

## 2. Architecture Overview  

```
+-------------------+        +-------------------+        +-------------------+
|   Client SDKs     | <----> |   API Gateway     | <----> |   Inference Node  |
| (Python, Swift,  | HTTP   | (FastAPI + Auth) | gRPC   | (vLLM + CoreML)  |
|  VSCode, CLI)    |        |                   |        |                   |
+-------------------+        +-------------------+        +-------------------+
                                   |                         |
                                   |                         |
                                   v                         v
                           +-------------------+   +-------------------+
                           |   Model Store     |   |   Metrics/Logs    |
                           | (Apple‑MLModel)   |   | (Prometheus,     |
                           +-------------------+   |  Loki)            |
```

* **Client SDKs** – thin wrappers that handle authentication, request serialization, streaming responses, and optional local fallback.  
* **API Gateway** – FastAPI service exposing REST & WebSocket endpoints, performing rate‑limiting, JWT validation, and request routing.  
* **Inference Node** – Stateless worker process running on Apple Silicon hardware. It loads the model via Core ML, executes inference through vLLM’s scheduler, and returns token streams.  
* **Model Store** – Apple‑MLModel bundle (`.mlmodelc`) stored in an S3‑compatible bucket; nodes pull on start‑up or on‑demand.  
* **Observability** – Prometheus metrics (throughput, latency, GPU/CPU utilisation) and Loki logs are scraped by the central monitoring stack.  

---  

## 3. Core Components  

| Component | Responsibility | Implementation Details |
|-----------|----------------|------------------------|
| **vLLM Engine** | High‑throughput token generation, KV‑cache management | Forked from `vllm-project/vllm` (v0.4). Added Apple‑Silicon scheduler hooks and custom `DeviceManager` that selects `mlcompute` backend. |
| **Core ML Backend** | Executes quantized model on ANE/CPU | Model exported to `mlmodelc` with 8‑bit integer quantization (per‑channel). Uses `MLComputeDevice` with `MLComputeDeviceType::ANE` fallback to `CPU`. |
| **Quantization Pipeline** | Convert original FP16 checkpoint → INT8 Core ML model | Python script (`quantize.py`) uses `torch.quantization` + `coremltools` conversion. Stores calibration dataset (10 k code snippets) in the repo. |
| **API Gateway** | HTTP/WS entry point, auth, throttling | FastAPI + `uvicorn[standard]`. JWT validated against AxentX IAM. Rate limit 30 req/min per token. |
| **Client SDKs** | Language‑specific wrappers | - **Python** (`apple_silicon_coder`) – pip package, async API. <br> - **Swift** (`AppleSiliconCoder`) – Swift Package Manager, Combine‑based streaming. <br> - **VSCode Extension** – uses the Python SDK under the hood. |
| **Metrics Exporter** | Prometheus exposition | `/metrics` endpoint on each node; counters for `tokens_generated`, `requests_total`, histograms for latency. |
| **Model Store Sync** | Pull latest model version | Simple S3 sync using `awscli` with `--no-sign-request` (public bucket). Versioned by semantic tag (`v1.2.0`). |

---  

## 4. Data Model  

### 4.1 Request Payload  

```json
{
  "model": "apple-silicon-coder",
  "messages": [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function to compute Fibonacci numbers."}
  ],
  "max_tokens": 256,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": true
}
```

* `messages` follows the OpenAI chat format.  
* `stream` = `true` returns Server‑Sent Events (SSE) or WebSocket frames with incremental tokens.  

### 4.2 Response (Streaming)  

```
data: {"token":"def"}
data: {"token":" "}
data: {"token":"fib"}
...
data: {"finish_reason":"stop"}
```

When `stream=false`, a single JSON object with `choices[0].message.content` is returned.  

---  

## 5. Key APIs / Interfaces  

| Method | Path | Description | Auth | Streaming |
|--------|------|-------------|------|-----------|
| `POST /v1/chat/completions` | `/v1/chat/completions` | Generate code/completion from chat history. | JWT (Bearer) | SSE / WebSocket (if `stream=true`) |
| `GET /v1/models` | `/v1/models` | List available model versions. | JWT | N/A |
| `GET /healthz` | `/healthz` | Liveness/Readiness probe. | None | N/A |
| `GET /metrics` | `/metrics` | Prometheus metrics. | None | N/A |

**Authentication** – Clients must include `Authorization: Bearer <jwt>` header. Tokens are issued by AxentX IAM with scopes `coder:invoke`.  

---  

## 6. Technology Stack  

| Layer | Technology | Version | Rationale |
|-------|-------------|---------|-----------|
| **Inference Engine** | vLLM (fork) | 0.4.2‑apple | Proven high‑throughput scheduler; easy to extend for Core ML. |
| **Model Runtime** | Core ML (mlcompute) | macOS 14+ | Direct access to ANE, low‑latency int8 execution. |
| **Quantization** | torch, coremltools | 2.3, 7.2 | Enables 8‑bit inference with < 2 % accuracy loss on coding benchmarks. |
| **API** | FastAPI + uvicorn | 0.115, 0.30 | Async, auto‑docs, easy deployment. |
| **Containerisation** | Docker (Apple Silicon base) | 24.0 | Guarantees reproducible environment on M1/M2 chips. |
| **Observability** | Prometheus, Loki, Grafana | 2.53, 2.9, 10.4 | Standard monitoring stack. |
| **CI/CD** | GitHub Actions (self‑hosted runners on M1) | – | Builds model bundle, runs integration tests, pushes Docker image. |
| **Client SDKs** | Python 3.11, Swift 5.9, VSCode Extension (TypeScript) | – | Native developer experience. |

---  

## 7. Dependencies  

- **System**: macOS 14+ (Apple Silicon), Docker Engine for Apple Silicon.  
- **Python**: `torch>=2.3`, `vllm>=0.4.2‑apple`, `fastapi`, `uvicorn[standard]`, `python‑jwt`, `httpx`.  
- **Swift**: `AppleMLCompute`, `Combine`.  
- **Core ML Model**: `apple-silicon-coder-1.2.0.mlmodelc` (≈ 2.8 GB).  
- **External Services**: S3 bucket `axentx-models`, AxentX IAM (OAuth2).  

All third‑party libraries are MIT/Apache‑2.0 compatible; licensing verified in `LICENSES/THIRD_PARTY.csv`.  

---  

## 8. Deployment Architecture  

### 8.1 Container Image  

```
FROM ghcr.io/arkashira/apple-silicon-base:latest   # Apple Silicon base with Python 3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
ENV MODEL_VERSION=1.2.0
CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "8080"]
```

Image size ≈ 1.9 GB.  

### 8.2 Kubernetes (optional)  

* **Node pool**: macOS‑based nodes (e.g., `kind-mac` or custom `k3s` on M1).  
* **Deployment**: `replicas: 3` (horizontal scaling).  
* **Pod spec**:  
  ```yaml
  resources:
    limits:
      cpu: "8"
      memory: "16Gi"
    requests:
      cpu: "4"
      memory: "8Gi"
  ```  
* **Service**: LoadBalancer exposing port 443 with TLS termination (cert‑manager).  

### 8.3 Scaling Strategy  

* **Throughput target**: 200 t/s per pod.  
* **Auto‑scale**: HorizontalPodAutoscaler based on `tokens_generated_per_second` metric.  
* **Cold‑start mitigation**: Warm‑up job loads model into memory on pod start.  

---  

## 9. Security & Compliance  

| Concern | Mitigation |
|---------|------------|
| **Data leakage** | No request payload is persisted; logs redact `messages.*.content`. |
| **Auth** | JWT signed with RSA‑2048; short‑lived (15 min) access tokens. |
| **Model IP** | Model bundle stored in private S3 bucket; access via signed URLs for internal nodes only. |
| **Compliance** | All third‑party libs are OSS with permissive licenses; no user data stored long‑term. |
| **Runtime sandbox** | Inference runs in an unprivileged container; no network egress except to model store. |

---  

## 10. Testing & Validation  

| Test Type | Tooling | Coverage |
|-----------|---------|----------|
| Unit | `pytest` (Python), `XCTest` (Swift) | 92 % |
| Integration | Postman collection + `httpx` scripts | 100 % of API surface |
| Performance | Custom load‑generator (`locust`) targeting 250 t/s per node | Meets ≥ 200 t/s |
| Regression (reasoning) | Code generation benchmark suite (HumanEval‑C) | ≤ 2 % drop vs baseline FP16 model |
| Security | OWASP ZAP scan on gateway | No critical findings |

All CI jobs run on Apple Silicon self‑hosted runners; failures block merges.  

---  

## 11. Roadmap (post‑launch)  

| Milestone | Target | Description |
|-----------|--------|-------------|
| **v1.3.0** | Q3 2026 | Add support for Apple Vision Pro (GPU‑accelerated) for multi‑modal code‑image generation. |
| **v1.4.0** | Q4 2026 | Introduce LoRA adapters for domain‑specific coding (e.g., SwiftUI, Rust). |
| **v2.0** | H1 2027 | Full offline SDK with on‑device model updates via delta patches (≤ 200 MB). |

---  

## 12. Glossary  

| Term | Definition |
|------|------------|
| **ANE** | Apple Neural Engine – hardware accelerator for ML on Apple Silicon. |
| **Core ML** | Apple’s on‑device ML runtime, exposing `MLComputeDevice` APIs. |
| **vLLM** | High‑throughput LLM inference engine with KV‑cache scheduling. |
| **SSE** | Server‑Sent Events – streaming protocol used when `stream=true`. |
| **LoRA** | Low‑Rank Adaptation – technique for efficient fine‑tuning. |

---  

*Prepared by the Apple‑Silicon‑Coder engineering team. For questions, contact `engineer-lead@axentx.com`.*

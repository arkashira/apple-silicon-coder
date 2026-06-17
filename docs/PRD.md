# PRD – Apple Silicon Coder

**Product:** `apple-silicon-coder`  
**Owner:** Senior Product Lead – Axentx  
**Date:** 2026‑06‑17  
**Version:** 1.0  

---  

## 1. Problem Statement  

Developers building applications for macOS, iOS, iPadOS, visionOS, and other Apple‑Silicon platforms need a locally‑runnable LLM that can:

* Generate high‑quality code snippets, refactorings, and documentation **in real time**.  
* Exploit the performance characteristics of Apple Silicon (M‑series CPUs, Neural Engine, and unified memory) to achieve **≥ 200 tokens / second** throughput on a single device.  
* Remain affordable for individual developers and small teams (no cloud‑API fees, low power consumption).  

Existing solutions either:

| Solution | Latency / Throughput | Cost | Apple‑Silicon Optimization |
|----------|----------------------|------|----------------------------|
| OpenAI / Claude APIs | 30‑60 t/s (network bound) | $ per token | None (cloud) |
| Generic LLMs (e.g., LLaMA‑2, Mistral) run via CPU | 10‑30 t/s | Free but high CPU load | No hardware‑specific kernels |
| Apple‑provided CoreML models (e.g., CodeLlama‑CoreML) | 80‑120 t/s | Free | Limited to inference, no fine‑tuning, lower reasoning depth |

**Result:** Developers either pay per‑token for cloud APIs, suffer high latency on generic CPU models, or lack a model that balances speed, cost, and reasoning depth on‑device.

---

## 2. Target Users  

| Segment | Persona | Primary Pain Point |
|---------|---------|--------------------|
| **Individual macOS/iOS developers** | “Solo Sam” – builds apps, scripts, and utilities on a MacBook Pro (M2‑Pro). | Needs instant code assistance without leaving the IDE or paying per‑token. |
| **Small dev teams / startups** | “Team Tina” – 3‑5 engineers sharing a single Apple‑Silicon workstation. | Must keep tooling costs low while maintaining fast iteration cycles. |
| **Enterprise Apple‑Silicon labs** | “Lab Leo” – R&D groups with high‑end Mac Studio (M2‑Ultra). | Requires high‑throughput batch generation for code‑base analysis and migration tasks. |
| **Education / bootcamps** | “Instructor Ivy” – teaches Swift/Objective‑C on campus Macs. | Needs an affordable, offline model that can run on student laptops. |

---

## 3. Goals & Success Metrics  

| Goal | Metric | Target (12 mo) |
|------|--------|----------------|
| **Performance** | Throughput on M2‑Pro (single core) | ≥ 200 tokens / s (baseline) |
| | Latency for 256‑token completion | ≤ 0.8 s |
| **Affordability** | Average cost per developer per month | <$5 (electricity + maintenance) |
| **Quality** | Pass@1 on HumanEval‑Swift benchmark | ≥ 0.45 |
| | User‑rated relevance (5‑point Likert) | ≥ 4.2 |
| **Adoption** | Active installations (unique Apple‑Silicon devices) | 12 k |
| | Retention (30‑day active users) | 78 % |
| **Safety** | Toxicity/PII false‑positive rate | < 0.5 % |

---

## 4. Scope  

### 4.1 In‑Scope (Must‑Have)

1. **Model Architecture**  
   * 7B‑parameter transformer fine‑tuned on code (Swift, Objective‑C, Python, JavaScript).  
   * Quantized to 4‑bit (GPTQ) for memory‑efficiency, with optional 8‑bit fallback.

2. **Apple‑Silicon Optimized Runtime**  
   * Leverages **vLLM** for batched inference and **SGLang** for structured generation.  
   * Uses **Metal** kernels for attention/FFN and Apple Neural Engine (ANE) for matrix multiplications where available.  
   * Auto‑detects device (M1‑M2‑M2‑Pro/Ultra) and selects optimal kernel path.

3. **CLI & IDE Plugins**  
   * `asc` command‑line tool (generate, refactor, explain).  
   * VS Code & Xcode extensions (inline suggestions, doc generation).  

4. **Packaging & Distribution**  
   * Homebrew formula & Apple Silicon‑only .pkg installer.  
   * Automatic background updates (signed, notarized).  

5. **Safety Filters**  
   * Integrated content filter (OpenAI‑compatible toxicity model).  
   * Prompt‑level “no‑PII” guardrails.

6. **Telemetry (opt‑in)**  
   * Anonymous usage stats (throughput, error rates).  
   * Feedback button in IDE plugins.

### 4.2 Out‑of‑Scope (Will Not Be Delivered in v1)

| Item | Reason |
|------|--------|
| Multi‑GPU / distributed inference across multiple Macs | Focus on single‑device performance first. |
| Full fine‑tuning UI for end‑users | Requires server‑side infrastructure; planned for v2. |
| Support for non‑Apple‑Silicon Linux/Windows | Separate product line (cross‑platform coder). |
| Integrated test‑generation engine | Future roadmap after core generation stabilizes. |
| Commercial licensing for enterprise (on‑prem) | Initial release targets individual & SMB market. |

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Apple‑Silicon Optimized Inference Engine** | Custom runtime built on vLLM + Metal + ANE kernels. | - 200 t/s on M2‑Pro (single core) <br> - Passes unit‑tests for kernel fallback. |
| **P1** | **CLI (`asc`)** | Simple command line for generation, refactoring, explanation. | - `asc generate "func add(a:Int,b:Int)->Int"` returns valid Swift code within 1 s. |
| **P1** | **VS Code & Xcode Extensions** | Inline suggestions, docstring generation, quick‑fix actions. | - 90 % of suggestions accepted in user study. |
| **P2** | **4‑bit Quantized Model** | Reduces memory to ~6 GB, fits on M1‑Max. | - Model loads in ≤ 5 s, uses ≤ 8 GB RAM. |
| **P2** | **Safety & Content Filtering** | Blocks toxic or PII‑leaking outputs. | - False‑positive < 0.5 %, false‑negative < 1 %. |
| **P3** | **Telemetry Dashboard** | Opt‑in usage collection, performance graphs. | - Dashboard shows real‑time throughput per device. |
| **P3** | **Automatic Update System** | Secure, notarized updates via Homebrew or .pkg. | - 95 % of active installs receive latest version within 24 h of release. |

---

## 6. Milestones & Timeline  

| Milestone | Deliverable | Owner | Target Date |
|-----------|-------------|-------|-------------|
| **M1 – Foundations** | Repo scaffold, CI/CD pipeline, vLLM integration | Engineering Lead | 2026‑07‑15 |
| **M2 – Model Training** | 7B code‑fine‑tuned model, 4‑bit quantization | ML Team | 2026‑08‑30 |
| **M3 – Apple‑Silicon Runtime** | Metal + ANE kernels, benchmark ≥ 200 t/s | Runtime Engineers | 2026‑09‑20 |
| **M4 – CLI & Packaging** | `asc` tool, Homebrew formula, .pkg installer | DevOps | 2026‑10‑05 |
| **M5 – IDE Plugins** | VS Code & Xcode extensions (beta) | Product Engineering | 2026‑10‑25 |
| **M6 – Safety Filters** | Integrated toxicity/PII guardrails | Safety Lead | 2026‑11‑10 |
| **M7 – Beta Launch** | Private beta to 200 users, telemetry enabled | PM | 2026‑11‑30 |
| **M8 – GA Release** | Public launch, documentation, support portal | PM/Marketing | 2026‑12‑20 |
| **M9 – Post‑Launch Review** | Success metrics report, roadmap refinement | PM | 2027‑01‑31 |

---

## 7. Risks & Mitigations  

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Kernel performance variance** across M1‑M2‑Ultra | Missed throughput target | Medium | Early profiling on device matrix; fallback to vLLM CPU path. |
| **Quantization quality loss** affecting code correctness | Lower Pass@1 score | Low | Run extensive regression suite; keep 8‑bit fallback. |
| **Apple policy changes** on ANE usage for third‑party models | Runtime breakage | Low | Design abstraction layer to swap to Metal‑only if needed. |
| **User adoption** slower than forecast | Revenue delay | Medium | Partner with Swift.org and Xcode community for co‑marketing. |
| **Safety filter false positives** degrade UX | User frustration | Low | Provide easy “override” toggle in IDE plugins. |

---

## 8. Open Questions  

1. Should we ship a **small 1.5B variant** for older M1 devices as a separate package?  
2. What is the optimal licensing model (free‑core + paid‑pro features) for sustained revenue?  
3. Will Apple’s upcoming **ML Compute** APIs (2027 Q1) supersede our custom kernels?  

*Action:* Schedule a cross‑functional workshop (PM, ML, Runtime, Legal) by 2026‑07‑01 to resolve.  

---  

## 9. Approval  

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner |  |  |  |
| Engineering Lead |  |  |  |
| ML Lead |  |  |  |
| Safety Lead |  |  |  |
| Marketing Lead |  |  |  |

---  

*Prepared by:* Senior Product/Engineering Lead, Axentx  
*Document ID:* PRD‑ASC‑2026‑01

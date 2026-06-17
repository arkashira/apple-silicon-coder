# ROADMAP.md – apple‑silicon‑coder

## Vision
Deliver a high‑throughput, low‑latency LLM‑powered coding assistant that runs **natively on Apple Silicon (M‑series)**.  
Target performance: **≥ 200 tokens / second** per core with full reasoning capabilities, enabling developers to code faster on macOS laptops and desktops without cloud dependency.

---

## Milestones Overview

| Milestone | Target Date | Description | MVP‑Critical? |
|-----------|-------------|-------------|---------------|
| **MVP – “Local Code‑Assist”** | **2026‑08‑15** | First ship‑able product that runs entirely on‑device, provides autocomplete & inline suggestions for Python, JavaScript, and Swift. | ✅ |
| **v1 – “Full‑Stack IDE Integration”** | 2026‑12‑01 | Plug‑ins for VS Code, Xcode, JetBrains; multi‑language support (Go, Rust, C++); project‑wide context & refactoring. | – |
| **v2 – “Enterprise & Collaboration”** | 2027‑04‑15 | Team‑wide code‑review bots, CI/CD linting, secure on‑prem deployment, API for custom tooling. | – |

---

## MVP – “Local Code‑Assist” (Launch)

| Feature | Acceptance Criteria | Owner |
|---------|----------------------|-------|
| **Apple‑Silicon Optimized Runtime** | • Built on **vLLM** + **SGLang** with Metal kernels.<br>• Sustains **≥ 200 t/s** on M2‑Pro (8‑core) under typical coding workload. | Runtime Engineer |
| **Core Coding Model** | • 7B‑parameter transformer fine‑tuned on `system‑user‑assistant` & `instr‑resp` datasets (≈ 1.5 B tokens).<br>• Benchmarked > 90 % on HumanEval‑C. | ML Engineer |
| **CLI Tool (`asc`)** | • `asc suggest <file> [--line N]` returns top‑3 completions.<br>• Works offline, < 100 ms latency per request. | DevOps |
| **Python / JavaScript / Swift Autocomplete** | • Integrated with `readline` and `sourcekitd` for context.<br>• 95 % acceptance in internal user study. | Front‑end |
| **Safety Filters** | • Toxicity & security filter (Open‑source `toxicity‑filter` lib).<br>• Zero false‑positives on a curated 500‑snippet test set. | QA |
| **Installer & Update System** | • Homebrew tap + signed notarized pkg.<br>• Auto‑update via Sparkle framework. | Release Engineer |
| **Documentation & Quick‑Start** | • 5‑minute install guide, usage examples, FAQ. | Technical Writer |
| **Telemetry (opt‑in)** | • Collect usage counts, latency, error rates (privacy‑first). | Data Engineer |

**MVP Success Metric:** 5,000 active macOS users within 30 days, average latency < 120 ms, ≥ 200 t/s sustained throughput.

---

## v1 – “Full‑Stack IDE Integration”

| Theme | Key Deliverables | Target |
|-------|------------------|--------|
| **IDE Plug‑ins** | • VS Code extension (Web‑view UI).<br>• Xcode Source Editor Extension.<br>• JetBrains plugin (IntelliJ, CLion). | Q4 2026 |
| **Expanded Language Coverage** | Add Go, Rust, C++, TypeScript support (model fine‑tune + tokenizers). | Q4 2026 |
| **Project‑Wide Context** | Index whole workspace, provide cross‑file suggestions, refactorings. | Q4 2026 |
| **In‑IDE Chat & Explain** | Interactive chat window for “explain this code”, “write tests”, etc. | Q4 2026 |
| **Performance Scaling** | Multi‑core dispatch, dynamic batch sizing, maintain ≥ 200 t/s per core. | Q4 2026 |
| **User Feedback Loop** | Inline rating UI → data pipeline for continuous fine‑tuning. | Q4 2026 |

**KPIs:** 80 % of beta users adopt at least one IDE plug‑in; average suggestion acceptance > 60 %; latency ≤ 150 ms.

---

## v2 – “Enterprise & Collaboration”

| Theme | Deliverables | Target |
|-------|--------------|--------|
| **Team‑wide Code Review Bot** | Auto‑generate review comments, detect anti‑patterns, suggest improvements. | Q1 2027 |
| **CI/CD Integration** | GitHub Action / GitLab CI job that runs `asc lint` on PRs. | Q1 2027 |
| **Secure On‑Prem Deployment** | Docker/Helm chart for internal networks, encrypted model weights, RBAC. | Q1 2027 |
| **Public API & SDK** | REST & gRPC endpoints, Python/Swift SDKs for custom tooling. | Q1 2027 |
| **Compliance & Auditing** | GDPR/CCPA data handling, exportable logs for audit trails. | Q1 2027 |
| **Pricing & Licensing** | Tiered licensing (individual, team, enterprise) with usage‑based billing. | Q1 2027 |
| **Marketplace Extensions** | Allow third‑party plug‑ins (e.g., domain‑specific snippets). | Q2 2027 |

**KPIs:** 30 + enterprise contracts, 95 % uptime SLA, average CI lint time < 5 s per 1k LOC.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Metal kernel performance variance** | May miss 200 t/s target on older M‑series chips. | Early profiling on M1‑Mini, fallback to CPU‑optimized path. |
| **Model size vs. device memory** | 7B model ~ 14 GB VRAM; older Macs may OOM. | Quantize to 4‑bit (GPTQ) for low‑memory mode; auto‑detect. |
| **Safety filter false positives** | Could frustrate developers. | Continuous human‑in‑the‑loop evaluation; adjustable filter strength. |
| **Apple policy changes (notarization, sandbox)** | Distribution delays. | Maintain close liaison with Apple Developer Relations; use notarized universal binaries. |

---

## Release Process (MVP)

1. **Feature Freeze** – 2026‑07‑31  
2. **Internal QA Sprint** – 2026‑08‑01 → 2026‑08‑07 (automated tests + manual code‑assist sessions)  
3. **Beta Release to 100 internal users** – 2026‑08‑08 → 2026‑08‑12 (collect telemetry, fix critical bugs)  
4. **Public Launch** – 2026‑08‑15 (Homebrew tap, docs, marketing page)  
5. **Post‑Launch Monitoring** – 2026‑08‑16 → 2026‑09‑30 (SLI/SLO tracking, rapid hot‑fixes)

---

## Appendices

- **Dataset Sources**: `system-user-assistant` (1.4 M pairs), `instr-resp` (6.3 M pairs) – used for instruction fine‑tuning.  
- **Core Tech Stack**: vLLM (inference), SGLang (structured generation), Metal (GPU kernels), Sparkle (auto‑update), Open‑source safety filter.  
- **Repository Structure** (high‑level)  
  ```
  /src
    /runtime   – Metal kernels, vLLM wrapper
    /model     – checkpoint loading, quantization scripts
    /cli       – asc command line
    /plugins   – VSCode, Xcode, JetBrains stubs
  /docs
    README.md
    INSTALL.md
  /tests
    unit/
    integration/
  ```

--- 

*Prepared by the Apple‑Silicon‑Coder product/engineering lead, 2026‑06‑17.*

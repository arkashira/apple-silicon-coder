# Breakeven Analysis – apple‑silicon‑coder

| Item | Assumptions | Value |
|------|-------------|-------|
| **Compute cost per active user** | 200 t/s throughput → 0.5 s per request (average). 1 GPU‑A100 (≈$3 USD/hour) runs 200 t/s. 1 GPU serves 400 req/s → 0.0025 s per request. 0.5 s/req → 200 req/s per user. <br>Compute cost = 200 req/s × $0.0025 s × 3600 s = **$18 USD/month** | **$18** |
| **Storage cost per active user** | 1 GB of user data + 10 GB of model checkpoints. 1 GB on S3 = $0.023 USD/month. | **$0.25** |
| **Bandwidth cost per active user** | 200 req/s × 1 KB payload = 200 KB/s → 17 GB/month. 1 GB egress = $0.09 USD. | **$1.53** |
| **Total variable cost per active user** | Compute + Storage + Bandwidth | **$19.78** |
| **Fixed cost (ops, dev, infra, marketing)** | $50 k/month (incl. 3 devs, ops, marketing) | **$50 k** |

---

## Pricing Tiers

| Tier | Monthly Price | Core Features | Extra Features |
|------|---------------|---------------|----------------|
| **Starter** | $29 | 200 t/s, 1 GPU, 1 GB storage, 10 GB checkpoints, 5 k requests/month | None |
| **Pro** | $79 | 400 t/s, 2 GPUs, 5 GB storage, 20 GB checkpoints, 20 k requests/month | Priority support |
| **Enterprise** | $199 | 800 t/s, 4 GPUs, 20 GB storage, 50 GB checkpoints, 80 k requests/month | SLA 99.9 %, dedicated account |

---

## Customer Acquisition Cost (CAC)

| Channel | Avg CAC | % of total spend |
|---------|---------|------------------|
| Paid Search | $120 | 30 % |
| Content Marketing | $60 | 15 % |
| Partnerships | $200 | 50 % |
| **Total CAC** | **$140** | 100 % |

---

## Lifetime Value (LTV)

| Tier | Avg Monthly Revenue | Avg Churn | LTV |
|------|---------------------|-----------|-----|
| Starter | $29 | 12 % | $29 / 0.12 = **$241** |
| Pro | $79 | 8 % | $79 / 0.08 = **$988** |
| Enterprise | $199 | 4 % | $199 / 0.04 = **$4,975** |

---

## Break‑Even Analysis

| Tier | Monthly Revenue per User | Monthly Cost per User | Profit per User | Users to Break‑Even |
|------|--------------------------|-----------------------|-----------------|---------------------|
| Starter | $29 | $19.78 | $9.22 | 50,000 |
| Pro | $79 | $19.78 | $59.22 | 842 |
| Enterprise | $199 | $19.78 | $179.22 | 279 |

**Break‑Even Users (all tiers combined)**  
Assuming a 70/20/10 split (Starter/Pro/Enterprise):

- Starter: 35 k users → $1.02 M revenue, $693 k cost → $327 k profit  
- Pro: 20 k users → $1.58 M revenue, $395 k cost → $1.19 M profit  
- Enterprise: 10 k users → $1.99 M revenue, $197 k cost → $1.79 M profit  

Total profit ≈ **$3.30 M**.  
Thus, **break‑even** is reached with **≈ 55 k active users** (≈ 35 k Starter, 20 k Pro, 10 k Enterprise).

---

## Path to $10 k MRR

| Tier | Users Needed | Monthly Revenue |
|------|--------------|-----------------|
| Starter | 345 | $10,005 |
| Pro | 127 | $10,033 |
| Enterprise | 51 | $10,149 |

**Recommended ramp**  
1. **Month 1–3**: Acquire 50 Starter users → $1.45 k MRR  
2. **Month 4–6**: Convert 30 % of Starter to Pro → +$2.37 k MRR  
3. **Month 7–9**: Add 20 Pro users → +$1.58 k MRR  
4. **Month 10–12**: Upsell 10 Pro to Enterprise → +$1.99 k MRR  

By month 12, total MRR ≈ **$10 k**.  

---

### Key Takeaways

- **Compute dominates cost**; optimize GPU utilization to keep per‑user cost ≤ $20.  
- **Pro tier** offers the highest margin; focus sales on this tier.  
- **Enterprise** drives LTV; nurture high‑value accounts with dedicated support.  
- **Break‑even** at ~55 k users; aim for 70 k to cushion churn.  
- **$10 k MRR** achievable in ~12 months with aggressive Pro upsell strategy.
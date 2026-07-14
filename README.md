# TCM-TopoGraph: Real-Time Topological and Geometric Clinical Decision Support System (CDSS)

Official implementation and simulation environment for the dissertation topic: **"Topological Data Analysis in Heterogeneous and Non-Euclidean Biological Networks: Unified Geometric Representations for High-Order Synergy Prediction"**.


---

## 📌 Project Overview

**TCM-TopoGraph** is a cloud-native, real-time Clinical Decision Support System (CDSS) that leverages Topological Data Analysis (TDA) and Hyperbolic Graph Neural Networks to predict high-order herbal synergy and prevent Adverse Drug Reactions (ADRs). 

To make this complex mathematics viable on low-cost clinical hardware, the project implements a **"Maximize Mathematics, Minimize Hardware"** philosophy. This repository contains both the core computational pipeline and a trace-driven population emulation suite.
### 🔬 Separation of Concerns (Evaluation Methodology)
To validate the system under rigorous academic and engineering standards, the evaluation is partitioned into two distinct phases:
1. **Domain-Specific Algorithmic Validation (TCM Logic):** Evaluated using our **DoTatLoi-714 Benchmark** , which aligns 361 indigenous acupoints to 714 pharmacological modalities via the **Probabilistic Multi-Evidence Alignment (PMEA) protocol**  (achieving a SOTA synergy prediction accuracy of **90.51%** and **0.77** cross-domain correlation on Stanford BIOSNAP .
2. **System-Level Performance Validation (Software Engineering):** Evaluated using a **Population-Scale Trace-Driven Simulation** utilizing raw physiological signals from the open-source **PhysioNet MIT-BIH Database**. This simulates a clinical ward with dozens of concurrent patients streaming chaotic, non-linear signals at 10Hz, verifying that our event-driven microservice architecture handles intensive topological calculations without thread-blocking or packet drop.

---

## ⚡ Empirical Performance Benchmarks

### 1. Micro-Benchmark: Topological Execution Time (Internal Filter)
Tested on the core persistent homology filter using `gudhi` across varying sliding window sizes ($N \in [10, 500]$).
* **$N=10$**: Average = `0.024 ms` | Max = `0.773 ms`
* **$N=50$ (Optimal Window)**: **Average = `0.032 ms`** | Max = `0.095 ms`
* **$N=100$**: Average = `0.057 ms` | Max = `0.133 ms`
* **$N=200$**: Average = `0.104 ms` | Max = `0.181 ms`
* **$N=500$**: Average = `0.264 ms` | Max = `0.903 ms`

*Conclusion:* Given a native 10Hz sampling rate (100 ms time budget per frame), an execution footprint of only **0.032 ms** for our optimal window size proves that the topological filter introduces negligible computational overhead.

### 2. Macro-Benchmark: End-to-End Latency & Scalability (Network RTT)
Stress-tested using the asynchronous FastAPI server and nested event-loop clients over WebSockets at a native 10Hz transmission rate.
* **1 Client:** Average RTT = `1.07 ms` | P95 Latency = `1.60 ms` | Max RTT = `2.15 ms`
* **10 Clients:** Average RTT = `1.98 ms` | P95 Latency = `3.53 ms` | Max RTT = `4.28 ms`
* **50 Clients (Heavy Ward Stress):** **Average RTT = `3.46 ms`** | **P95 Latency = `9.35 ms`** | Max RTT = `21.26 ms`

*Conclusion:* Even under a heavy load of 50 concurrent clinical devices processing 2,500 continuous data packets, the 95th Percentile (P95) latency remains well below **10 ms**, comfortably fitting within the 100 ms real-time transmission budget.

---

## 🚀 Getting Started

To explore this research framework, we provide both a standalone interactive browser-based simulation and a real-time programmatic testing suite.

### Option A: Standalone Interactive Demo (Recommended)
You can test the system's real-time filtering, normalization, and telemetry response directly in your browser.

1. Download the `index.html` file from this repository.
2. Double-click to open it in Google Chrome, Microsoft Edge, or Safari.
3. Use the **View Selector** to switch between homogeneous and heterogeneous patient streams (simulating baseline drifts and motion artifacts).
4. Drag the **Time Slider** to observe real-time cloud metric telemetry (CPU Load, active streams, and Round-Trip Time) adjusting instantaneously.

---

### Option B: Python Real-Time Emulation Suite
To replicate our micro- and macro-latency benchmarks, you can execute the Python simulation pipeline.

#### 1. Install Dependencies
```bash
pip install fastapi uvicorn websockets nest_asyncio wfdb numpy gudhi

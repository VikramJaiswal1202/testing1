# AutoSRE: AI-Driven Self-Healing CI/CD & Operations System

![AutoSRE Banner](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge) 
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python) 
![Next.js](https://img.shields.io/badge/Next.js-14.x-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.x-009688?style=for-the-badge&logo=fastapi)
![Prometheus & Grafana](https://img.shields.io/badge/Observability-Prometheus%2FGrafana-orange?style=for-the-badge&logo=prometheus)

AutoSRE is an innovative, fully automated Site Reliability Engineering (SRE) microservice that seamlessly embeds autonomous self-healing, root-cause analysis, and threat remediation into the CI/CD and application monitoring pipeline. Built for a Hackathon (`HackByte4`), it provides multi-tiered intelligence, bringing self-healing infrastructure to reality.

---

## 🎯 Aim and Objectives

The primary objective of AutoSRE is to remove human bottlenecks from incident response and CI/CD disruption. Traditional SRE relies on manually configured alerts, debugging, and patching. AutoSRE changes this paradigm by:

1. **Continuous Monitoring:** Integrating seamlessly with Prometheus and Grafana for real-time application telemetry.
2. **Predictive Analysis:** Intercepting problematic commits/Pull Requests and assessing architectural risk *before* deployment.
3. **Automated Root Cause Analysis (RCA):** Deeply analyzing performance degradation (like anomalous latency or error bursts).
4. **Autonomous Self-Healing:** Generating code/configuration fixes dynamically and executing remediation patches dynamically via an array of specialized AI agents.

---

## ⚙️ How It Works (Architecture & Workflow)

The project consists of three major components:
- **The Target Application:** A Next.js Frontend + FastAPI Backend exposing APIs (`/api/simulate`).
- **The Observability Stack:** Prometheus and Grafana containerized via Docker for monitoring backend latency and request counts.
- **AutoSRE Agentic Pipeline:** A multi-agent framework built in Python to supervise system health.

### The Agentic Workflow
When AutoSRE runs, it delegates responsibilities sequentially to its AI Swarm:

1. **Monitoring Agent:** Subscribes to telemetry from Prometheus. It detects anomalies such as error spikes (HTTP 500) or high latency.
2. **Incident Analysis Agent:** Once an incident is passed from monitoring, this agent gathers context (logs, traces, code context) to write a detailed Root Cause Analysis (RCA).
3. **Remediation Agent:** Using the generated RCA, it suggests robust operational actions or code fixes.
4. **Risk Scoring Agent:** Validates the remediation strategy against infrastructure safety to block destructive or risky actions.
5. **Execution Agent:** In safe boundaries, automatically executes the fix (e.g., reverting a bad commit, altering dynamic configuration, or scaling resources) and validates recovery.

A dynamic `load_generator.py` script is provided to simulate load, error spikes, and delays, proving the system's fault-detection in real time.

---

## 🚀 How to Use It On Your Own

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- Docker and Docker Compose
- API Keys configured in your environment (for the LLM powering the agents, e.g., OpenAI or Gemini).

### 1. Start the Environment & App
Spin up the main Next.js frontend, the FastAPI backend, Prometheus, and Grafana using Docker.

```bash
docker-compose up --build -d
```
* **Frontend UI:** `http://localhost:8080`
* **FastAPI Backend:** `http://localhost:8000`
* **Prometheus:** `http://localhost:9090`
* **Grafana:** `http://localhost:3000`

### 2. Configure AutoSRE Environment
Navigate to the `autosre/` directory and install the necessary dependencies:

```bash
cd autosre
pip install -r requirements.txt # (Ensure agents and dependencies are installed)
```
Ensure required environment variables are set. Example:
```bash
export LLM_API_KEY="your-api-key"
export SERVICES_CONFIG="my-backend,my-frontend"
```

### 3. Generate Load / Incidents
To trigger the agentic anomaly detection, you must simulate a live environment. We provide a load generator that pings the backend `/api/simulate` endpoint:

```bash
python load_generator.py
```
*Tip: You can modify `./backend/config.json` manually with a `delay_ms` value to intentionally spike latency and trigger AutoSRE.*

### 4. Run the AutoSRE Pipeline
Fire up the AutoSRE orchestrator. It will execute the full surveillance and self-healing loop:

```bash
python autosre/main.py
```
You will see the pipeline traverse through the agent swarm:
**`Monitor -> RCA -> Remediate -> Score Risk -> Execute Fix`**

### Validating Observability
Check Grafana at `http://localhost:3000` (Default login: `admin`/`admin`) to visually see the latency and request graphs captured by the Prometheus scrape configurations defined in `prometheus.yml`.

---
**Maintained exclusively for advanced AIOps research and hackathon demonstration.**

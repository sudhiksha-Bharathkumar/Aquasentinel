# 💧 AquaSentinel (NeerGap Vellore)
**Intermittent-Supply Risk Radar & Resource Triage System**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 The Problem
While long-term water infrastructure missions (like AMRUT pipelines and underground sewerage) are rolling out ward-by-ward, cities like Vellore face a dangerous "transition gap"[cite: 20]. 
* **Intermittent Supply:** Many wards receive piped water only once every 3 to 10 days for limited hours[cite: 18, 20].
* **Negative Pressure Ingress:** When pipes sit empty, they depressurize. Cracks near open drains and septic tanks suck in contaminated wastewater[cite: 20]. 
* **First-Flush Hazard:** When the supply abruptly restarts, accumulated pathogens and silt are pushed directly to household taps[cite: 20].
* **Unreliable Evidence:** Low-cost IoT sensors often drift, and field kits (like H2S vials) have limited accuracy, meaning a single "pass" or "alarm" is weak proof of safety[cite: 17, 18].

## 🚀 The Solution
AquaSentinel bridges this public health gap. It is an explainable early-warning and triage dashboard that tells municipal authorities **which wards are at the highest risk today** and **how to allocate scarce daily resources**[cite: 17, 20]. 

### Key Features
* **Risk Scoring Engine:** Calculates ward-level vulnerability using the transparent formula: `Risk = Pressure Loss Probability × Proximity to Sewage Source × Population Exposed`[cite: 20].
* **TruthTap Trust Layer:** Audits incoming sensor evidence using Isolation Forest algorithms to flag anomalies and drift, explicitly separating the "risk score" from the "evidence confidence score"[cite: 18, 20].
* **Greedy Resource Triage:** A knapsack optimizer that mathematically prioritizes where to send limited test kits, water tankers, and repair crews to maximize population-weighted risk reduction[cite: 20].
* **What-If Simulation:** An interactive slider that allows officials to simulate infrastructure upgrades (e.g., completing a sewer line in Ward X) and watch the localized risk drop[cite: 20].
* **Complaint NLP:** A multilingual (English/Tamil) TF-IDF text classifier that maps citizen complaints (e.g., yellow water, pressure drops) against the predictive risk map[cite: 20].

## 🛠️ Tech Stack
* **Core Data Science:** `pandas`, `numpy`, `scikit-learn`, `scipy` (for optimization)[cite: 20].
* **Geospatial & Visualization:** `geopandas`, `folium`, `plotly`[cite: 20].
* **Interactive Frontend:** `streamlit`[cite: 20].
* **Hardware Integration (Optional Bench-Scale):** ESP32 microcontrollers simulating/transmitting MQTT JSON payloads from pressure, turbidity, and free-residual chlorine sensors[cite: 17, 20].

## 📂 Repository Structure
```text
aquasentinel/
├── data/
│   ├── synthetic_ward_data.csv       # Simulated demographic and pipe-age data
│   └── weather_inputs.csv            # Rainfall parameters (Open-Meteo)
├── models/
│   ├── risk_calculator.py            # Baseline transparent risk formula
│   ├── truthtap_auditor.py           # Isolation Forest anomaly detection
│   └── text_classifier.py            # TF-IDF NLP for citizen complaints
├── optimization/
│   └── greedy_knapsack.py            # Resource allocation logic
├── app.py                            # Main Streamlit dashboard
├── requirements.txt
└── README.md

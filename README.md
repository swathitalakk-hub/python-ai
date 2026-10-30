# Student Performance Analytics & Predictive System 🎓📊

An AI-powered academic performance analytics, early warning detection, and interactive simulation system built with Python, scikit-learn, and a modern glassmorphic web dashboard.

---

## 🚀 Key Features

- **Executive Analytics Engine**: Calculates cohort statistics, grade distributions, pass rates, and inter-department metrics.
- **Machine Learning Predictor (Random Forest Regressor)**: Predicts final exam performance with **92.8% R² accuracy**.
- **Early Warning Risk Classifier**: Identifies at-risk students before final evaluations with automated remedial guidance.
- **Feature Importance Analysis**: Discloses key academic drivers (Midterm impact: 55%, Assignments: 28%, Study Hours: 13.1%).
- **Interactive Web Dashboard**:
  - Dark glassmorphic user interface.
  - Interactive Chart.js visualizations (Grade distribution, risk breakdown, department benchmarks).
  - Real-time "What-If" academic simulator to test interventions on study hours & attendance.
  - Searchable and filterable student roster.

---

## 📁 Repository Structure

```
├── generate_dataset.py      # Synthetic realistic academic dataset generator
├── analytics_engine.py      # Core statistical and ML models (sklearn, pandas)
├── main.py                  # CLI dashboard runner and demo pipeline
├── serve_dashboard.py       # Local web server for interactive dashboard
├── students_data.csv        # Cohort database of 250+ student records
├── analysis_results.json    # Exported statistical model and cohort summary
├── dashboard/
│   └── index.html           # Modern interactive web dashboard
├── requirements.txt         # Dependencies
├── .gitignore               # Ignored files
└── README.md                # Project documentation
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/student-performance-analytics.git
   cd student-performance-analytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Running the System

### 1. Run the CLI Analytics Pipeline
```bash
python main.py
```
Outputs complete executive metrics, top achievers, at-risk rosters, and ML validation.

### 2. Launch the Web Dashboard
```bash
python serve_dashboard.py
```
Or open [dashboard/index.html](file:///c:/Users/T.SWATHI/OneDrive/Documents/python.ai/dashboard/index.html) directly in any web browser.

---

## 📈 Model Performance Benchmark

| Model | Metric | Value |
|---|---|---|
| **RandomForestRegressor** | $R^2$ Score | **0.9276 (92.8%)** |
| **RandomForestRegressor** | RMSE | **±3.82 points** |
| **RandomForestClassifier** | Risk Accuracy | **100%** |
| **RandomForestClassifier** | F1-Score | **100%** |

---

## 📄 License
MIT License

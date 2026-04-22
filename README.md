---

# 📊 Workforce Productivity Analytics Dashboard

An interactive **Streamlit dashboard** for analyzing workforce productivity, comparing performance across work modes, and generating actionable insights through data visualization.

---

## 🔍 Overview

The dashboard evaluates key metrics such as:

* Efficiency
* Utilization Rate
* Task Completion

It helps identify trends, top performers, and underperforming segments for better decision-making.

---

## ⚙️ Features

* **Multi-page dashboard**

  * Overview
  * Descriptive Analysis
  * Trend Analysis
  * Comparative Analysis
  * KPI Dashboard
  * Conclusion

* **Interactive filters**

  * Department, Work Mode, Location, Gender, Age Group

* **Visualizations**

  * Bar, scatter, box, violin, and trend charts

* **Analytics**

  * Work mode comparison
  * Department performance
  * Employee-level insights
  * Risk identification

---

## 🛠️ Tech Stack

* Streamlit
* Pandas, NumPy
* Plotly
* Custom CSS

---

## 📁 Project Structure

```bash
├── app.py
├── data/
│   └── cleaned_data.csv
└── README.md
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install streamlit pandas numpy plotly
streamlit run app.py
```

---

## 📊 Data Requirements

Required columns:

* `employee_id`, `task_id`, `efficiency`, `utilization_rate`, `work_mode`

Optional:

* `department`, `location`, `gender`, `age`, `month`

---

## 📈 Key Insights

* Productivity varies across work modes
* Efficiency > task volume as a performance metric
* High utilization ≠ high efficiency
* Identifies top performers and at-risk employees

---

## 🔮 Future Scope

* Real-time data integration
* Drill-down analytics
* Exportable reports

---

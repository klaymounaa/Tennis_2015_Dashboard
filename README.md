# 🎾 ATP Tennis 2015 – Data Cleaning, Analysis & Interactive Dashboard

This project explores ATP Tennis matches from the 2015 season through **data cleaning, exploratory data analysis (EDA), and an interactive Streamlit dashboard**.  
The goal is to uncover performance patterns, player characteristics, and match dynamics using Python and modern data visualization tools.

🔗 **Live Dashboard:**  
👉 https://tennis2015dashboard-5andq4ww248gwxugmxzfiz.streamlit.app

---

## 📌 Project Overview

This repository contains the complete workflow for analyzing the ATP 2015 dataset:

- Data cleaning & preprocessing  
- Exploratory data analysis (univariate, bivariate, multivariate)  
- Insight generation  
- Interactive dashboard using Streamlit  
- Raw and cleaned datasets  
- One Jupyter Notebook containing the full analysis process  

The final dashboard provides an accessible way to explore match statistics, player performance, and tournament context.

---

## 📊 Key Insights

Here are some of the most important insights discovered from the dataset:

1. **Most active ATP players fall between their mid-20s and early-30s**, where tennis performance typically peaks.  
2. **Tournament structure strongly shapes match dynamics**, with Grand Slams showing clear differences due to best-of-5 formats.  
3. **Court surface significantly influences playing style and outcomes**, especially between hard, clay, and grass.  
4. **Serving strength is one of the clearest indicators of match control**, correlating with dominance and win probability.  
5. **Match length drives many performance indicators**, including serve accuracy, break points, and physical decline.  

---

## 🧠 Project Structure

final_project/
│
├── app.py
├── requirements.txt
│
├── data/
│ ├── atp_matches_2015.csv
│ └── atp_matches_2015_updated.csv
│
└── notebooks/
└── project23.ipynb

---

## 📂 Files Description

| File / Folder | Description |
|---------------|-------------|
| `app.py` | Streamlit dashboard application |
| `requirements.txt` | Python dependencies |
| `data/atp_matches_2015.csv` | Original dataset |
| `data/atp_matches_2015_updated.csv` | Cleaned dataset |
| `notebooks/project23.ipynb` | Full analysis, cleaning, EDA & insights |

---

## 🚀 Technologies Used

- Python  
- Pandas  
- Plotly  
- Streamlit  
- Jupyter Notebook  

---

## ▶️ How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/klaymounaa/Tennis_2015_Dashboard.git
cd Tennis_2015_Dashboard

Install dependencies:
pip install -r requirements.txt

Run the Streamlit app:
streamlit run app.py

📬 Contact
Khalid Laymouna
GitHub: https://github.com/klaymounaa

⭐ Acknowledgements
Dataset sourced from ATP match statistics.
Dashboard built using Streamlit and Plotly.
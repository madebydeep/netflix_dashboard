# 🎬 **Netflix Dashboard – Interactive Data Explorer**

Built with **Streamlit**, **Plotly**, and **Pandas**

---

## 📌 **Overview**

The **Netflix Dashboard** is an interactive web application that lets users explore the complete Netflix catalog using intuitive filters, charts, and insights.
It provides a visually rich and dynamic way to understand trends in Netflix content — including genres, actors, directors, release timelines, and content types.

This project transforms the raw Netflix dataset into an accessible and visually engaging analytics tool.

---

## 🚀 **Live Demo**

*(https://madebydeep-netflix-dashboard-app-atnqhb.streamlit.app/)*

---

## 📊 **Features**

### 🔎 **1. Smart Filtering & Search**

Filter and search Netflix content by:

* **Content Type** (Movie / TV Show)
* **Country**
* **Genre**
* **Title search**
* **Actor search**

All visualizations update instantly based on your filters.

---

### 📈 **2. Key Statistics (KPIs)**

A quick snapshot of your filtered selection:

* Total number of titles
* Number of movies
* Number of TV shows
* Countries represented
* Unique genre count

---

### 🍿 **3. Content Type Distribution**

A Netflix-themed pie chart showing the ratio of **Movies vs TV Shows** in your selection.

---

### 📅 **4. Releases Over the Years**

A clean bar chart showing how many titles were released each year (2000 onwards).
Helps you identify:

* Growth periods
* Release spikes
* Industry patterns

---

### 🎭 **5. Top 10 Genres**

Extracted automatically from multi-genre listings.
Shows which genres dominate the current filtered dataset.

---

### 🎬 **6. Top Directors**

Highlights the directors who appear most frequently in the selected data.

---

### ⭐ **7. Top Actors**

Shows the actors who appear across the largest number of Netflix titles.
Useful for identifying the most common faces on the platform.

---

### 📥 **8. Download Filtered Dataset**

Instantly export the filtered table as a **CSV** for further analysis.

---

## 🏗️ **Tech Stack**

| Layer               | Tools Used                      |
| ------------------- | ------------------------------- |
| **Frontend**        | Streamlit, Custom CSS           |
| **Backend / Logic** | Python, Pandas                  |
| **Visualizations**  | Plotly Express                  |
| **Hosting**         | Streamlit Cloud                 |
| **Dataset**         | Netflix Titles Dataset (Kaggle) |

---

## 📂 **Dataset Source**

The dataset is sourced from Kaggle:
👉 [https://www.kaggle.com/datasets/shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

It includes:

* Title
* Director
* Cast
* Country
* Release Year
* Content Type
* Description
* Genre (listed_in)

---

## 🛠️ **Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/YOUR-USERNAME/netflix_dashboard.git
cd netflix_dashboard
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Run the App**

```bash
streamlit run app.py
```

---

## 🎨 **Design Philosophy**

This dashboard uses:

* A **Netflix-inspired dark theme**
* Clean red/black styling
* Smooth charts with Plotly
* Minimal, helpful text explanations
* Clear visual hierarchy

The focus is on simplicity and usability while preserving visual richness.

---

## 📌 **Project Structure**

```
📁 netflix_dashboard
│── app.py               # Main Streamlit app
│── netflix_titles.csv   # Dataset (or upload separately on Streamlit Cloud)
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
└── .gitignore
```

---

## ✨ **Future Improvements**

Planned enhancements:

* Add clustering (K-Means) based on descriptions
* Add word-cloud visualization for movie summaries
* Introduce user ratings (if dataset supports it)
* Multi-year trend analysis
* Actor & director collaboration networks

---

## 👨‍💻 **Author**

**Deep Singh**
🔗 GitHub: [https://github.com/madebydeep](https://github.com/madebydeep)
💼 Portfolio: *Coming Soon*

If you like this project, consider starring ⭐ the repository!

---

## 📝 **License**

This project is licensed under the **MIT License** — free for personal and commercial use.


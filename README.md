# 🧠 Mental Health Data Analysis Web App

This project is an interactive **Streamlit** application aimed at analyzing various factors related to individuals' mental health. Through the app, users can visually explore possible relationships between **destructive thoughts** and variables such as age, job satisfaction, sleep duration, financial stress, and more.

<img width="1918" height="1015" alt="4" src="https://github.com/user-attachments/assets/be88b57a-5f27-48ff-a5c2-3601e3a18caa" />

---

##  App Features

- General information about the dataset
- Distribution by gender, age, city, and profession
- Analysis of factors related to destructive thoughts:
  - Job satisfaction
  - Sleep duration
  - Work/study hours
  - Financial stress
- Comprehensive visualizations:
  - Pie chart
  - Bar plot
  - Boxplot
  - Correlation heatmap
- Markdown summary explanations with each chart

---

## 📄 License

This dataset is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

- You must give appropriate credit to the dataset author.
- You may not use the material for commercial purposes.
- License details: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

**Dataset Author:** [adilshamim8 on Kaggle](https://www.kaggle.com/datasets/adilshamim8/exploring-mental-health-data/data)

---

## ⚙️ Installation Steps

### 1. Required Libraries

```bash
pip install pandas numpy matplotlib seaborn streamlit
```

##  Launching the App

```bash
streamlit run app.py
```
- Replace app.py with the name of your own .py file.

##  Kullanım Rehberi

Use the sidebar menu in the web interface to access the following analyses:

- **Dataset Info**: Structure, head rows, null check  
- **Gender Distribution**: Gender ratio (pie chart)  
- **Age Distribution**: Age histogram  
- **Work Type**: Student/worker ratio  
- **Top 10 Cities**: Cities with the highest number of participants  
- **Top 10 Professions**: Most common 10 professions  
- **Job Satisfaction**: Analysis of job satisfaction levels  
- **Work/Study Hours**: Analysis of daily work/study hours  
- **Financial Stress**: Analysis of financial stress levels  
- **Family Mental Illness**: Mental illness history in family  
- **Destructive Thoughts**: Distribution of destructive thoughts  
- **Group Analysis**: Boxplot of destructive thoughts by numerical features  
- **Correlation Matrix**: Heatmap of correlations between variables  

---

- ✅ Missing values have been cleaned and filled appropriately.  
- ⚠️ This application is for **analytical and educational purposes only**. It should **not** be used for diagnosis.

---

## ⚙️ Technical Details

-  Wide layout is supported  
-  Visuals are generated with high DPI  
-  Charts are displayed without data loss using `BytesIO`  
-  Explanations are presented in **Markdown** format  
-  Visualization libraries used: `matplotlib`, `seaborn`, `pandas`

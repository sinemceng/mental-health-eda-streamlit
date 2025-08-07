import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from io import BytesIO

st.set_page_config(layout="wide")
def load_data():
    df=pd.read_csv("veri.csv")  #you can add here your own dataset or the dataset in the discription.
    return df

def cleaning(df):
    df = df.copy()  #orijinal df bozulmasın diye
    df = df.drop(["id","Name","Academic Pressure","CGPA","Study Satisfaction"], axis=1)
    df["Profession"] = df["Profession"].replace([" ", "", "nan", "NaN", "None"], np.nan)
    df["Profession"] = df["Profession"].fillna("Unknown")
    df["Dietary Habits"] = df["Dietary Habits"].fillna(df["Dietary Habits"].mode()[0])
    df["Degree"] = df["Degree"].fillna(df["Degree"].mode()[0])
    df["Work Pressure"] = df["Work Pressure"].fillna(df["Work Pressure"].mean())
    df["Job Satisfaction"] = df["Job Satisfaction"].fillna(df["Job Satisfaction"].mean())
    df["Sleep Duration"] = df["Sleep Duration"].str.extract(r"(\d+)[^\d]+(\d+)?").astype(float).mean(axis=1)
    df["Sleep Duration"] = df["Sleep Duration"].fillna(df["Sleep Duration"].mean())
    return df

def plot_pie(df, col, title):
    st.subheader(title)
    counts = df[col].value_counts()
    fig, ax = plt.subplots(figsize=(3, 3))  # Bu sadece çizim boyutu
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140, shadow=True, colors=["blue", "red"])
    ax.set_title(title)

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=400, bbox_inches="tight")
    st.image(buf,width=350)  # ← Gerçek gösterim boyutu bu
    plt.close(fig)


def plot_box(df, col, target="Have you ever had suicidal thoughts ?"):
    st.subheader(f"{col} by Destructive Thoughts")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x=target, y=col, palette="Set2", ax=ax)
    ax.set_xlabel("Have you ever had destructive thoughts ?")
    st.pyplot(fig)

def plot_count(df, xcol, huecol, title):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x=xcol, hue=huecol, palette=["red","blue"], ax=ax)
    ax.set_title(title, fontweight="bold")
    ax.legend(title="Have you ever had destructive thoughts ?")
    st.pyplot(fig)

def correlation(df):
    st.subheader("Correlation Matrix")
    use_cols = ["Age", "Job Satisfaction", "Work/Study Hours", "Financial Stress"]
    corr = df[use_cols].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

st.title("Mental Health Data Analysis App")
df = load_data()
df = cleaning(df)

menu = st.sidebar.radio("Select Analysis", [
    "Dataset Info",
    "Gender Distribution",
    "Age Distribution",
    "Work Type",
    "Top 10 Cities",
    "Top 10 Professions",
    "Job Satisfaction",
    "Work/Study Hours",
    "Financial Stress",
    "Family Mental Illness",
    "Destructive Thoughts",
    "Group Analysis",
    "Correlation Matrix"
])

if menu == "Dataset Info":
    st.write("### First 5 Rows:")
    code = """
    st.dataframe(df.head())"""
    st.code(code)
    st.dataframe(df.head())
    st.markdown("""
    - This dataframe has 14 columns and 5 rows.
    """)

    st.write("### Column Types:")
    code = """
    st.write(df.dtypes)"""
    st.code(code)
    st.write(df.dtypes)
    st.markdown("""
    - It includes both categorical and numerical features.
    """)

    st.write("### Null Values:")
    code = """
    st.write(df.isnull().sum())"""
    st.code(code)
    st.write(df.isnull().sum())
    st.markdown("""
    - No missing values were found because all columns were cleaned.
    """)

elif menu == "Gender Distribution":
    col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
    with col1:
        plot_pie(df,"Gender","Gender Distribution")
    with col2:
        st.markdown("""
        #### Analysis Summary
        - This data shows gender distribution.
        - Females make up 45.3% of the sample.
        - Males make up 54.7% of the sample.
        """)

elif menu == "Age Distribution":
    st.subheader("Age Distribution")
    fig,ax =plt.subplots()
    ax.hist(df["Age"],bins=30,color="darkred",edgecolor="black", alpha=0.7)
    ax.set_xlabel("Age")
    ax.set_ylabel("Number of People")
    buf = BytesIO()
    fig.savefig(buf,format="png",dpi=500,bbox_inches="tight")
    st.image(buf, width=600)
    plt.close(fig)
elif menu == "Work Type":
    col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
    with col1:
        plot_count(df,"Working Professional or Student","Working Professional or Student","Work Type Distribution")
    with col2:
        st.markdown("""
            #### Analysis Summary
            - This data shows the distribution of respondents based on their work type.
            The majority of the respondents are working professionals, making up 
            approximately 80% of the sample. The remaining 20% of the respondents are students.
            This distribution could be a starting point for further analysis, potentially 
            examining the correlation between work type and the presence of destructive thoughts.
            """)

elif menu == "Top 10 Cities":
    st.subheader("Top 10 Most Populated Cities")
    city_counts = df["City"].value_counts().nlargest(10).reset_index()
    city_counts.columns = ["City","Count"]
    fig,ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=city_counts, x="City", y="Count", palette="pastel",ax=ax)
    for index, row in city_counts.iterrows():
        ax.text(x=index, y=row["Count"] + 3, s=f"{row['Count']}",ha='center',color='red',fontsize=10,fontweight="bold")
    st.pyplot(fig)

elif menu == "Top 10 Professions":
    st.subheader("Top 10 Most Populated Professions")
    prof_counts = df["Profession"].value_counts().nlargest(10).reset_index()
    prof_counts.columns = ["Profession", "Count"]
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=prof_counts,x="Profession",y="Count",palette="pastel", ax=ax)
    for index, row in prof_counts.iterrows():
        ax.text(x=index, y=row["Count"] + 3, s=f"{row['Count']}",ha='center',color='red',fontsize=10,fontweight="bold")
    st.pyplot(fig)

elif menu == "Job Satisfaction":
    col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
    with col1:
        plot_count(df, "Job Satisfaction","Have you ever had suicidal thoughts ?","Job Satisfaction")
    with col2:
        st.markdown("""
                #### Analysis Summary
                - The data generally suggests a negative correlation between job satisfaction and having destructive
                thoughts. In other words, as job satisfaction levels increase, the likelihood of having destructive
                thoughts appears to decrease. The number of people without destructive thoughts is generally higher
                in the more satisfied groups (3.0 and 5.0).
                """)

elif menu == "Work/Study Hours":
    col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
    with col1:
        plot_count(df,"Work/Study Hours","Have you ever had suicidal thoughts ?","Work/Study Hours")
    with col2:
        st.markdown("""
                #### Analysis Summary
                - The data suggests a positive correlation between very high work/study hours and the presence
                of destructive thoughts. While a typical 8-hour workday/study session does not show a strong link, 
                working or studying for 9 or more hours per day appears to be associated with an increased likelihood of 
                having destructive thoughts. This highlights the potential negative mental health impact of overwork.
                """)

elif menu == "Financial Stress":
    col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
    with col1:
        plot_count(df,"Financial Stress","Have you ever had suicidal thoughts ?","Financial Stress")
    with col2:
        st.markdown("""
                #### Analysis Summary
                - The data suggests a strong positive correlation between financial stress and having destructive thoughts.
                As the level of financial stress increases, the likelihood and number of individuals experiencing destructive 
                thoughts also significantly increase. The highest number of people with destructive thoughts is observed in the 
                group experiencing the most severe financial stress (level 5.0), while the lowest number is in the group with 
                the least financial stress (level 1.0). This highlights financial stress as a major contributing factor to poor 
                mental health.
                """)

elif menu == "Family Mental Illness":
    plot_pie(df,"Family History of Mental Illness","Family Mental Illness")

elif menu == "Destructive Thoughts":
    plot_pie(df,"Have you ever had suicidal thoughts ?","Destructive Thoughts Distribution")

elif menu == "Group Analysis":
    cols = ["Age", "Sleep Duration", "Work/Study Hours", "Financial Stress"]
    for col in cols:
        if col == "Age":
            col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
            with col1:
                plot_box(df, col)
            with col2:
                st.markdown("""
                            #### Analysis Summary
                            - The data suggests a slight negative correlation between age and destructive thoughts. 
                            The median age for the group that has had destructive thoughts ("Yes") is lower than 
                            the group that has not ("No"). This indicates that, based on this sample, destructive thoughts 
                            might be slightly more prevalent in younger adults. However, the overlap in the age ranges is 
                            significant, so this is a general trend rather than a definitive separation.
                            """)
        elif col == "Sleep Duration":
            col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
            with col1:
                plot_box(df, col)
            with col2:
                st.markdown("""
                            #### Analysis Summary
                            - The data suggests a negative correlation between sleep duration and destructive thoughts. 
                            The median sleep duration for the group that has had destructive thoughts ("Yes") is half 
                            an hour less than the group that has not ("No"). This indicates that, based on this sample, 
                            individuals who have experienced destructive thoughts tend to sleep slightly less. The wider 
                            spread and presence of more extreme outliers in the "Yes" group also suggest a less stable or 
                            more irregular sleep pattern for this group.
                            """)
        elif col == "Work/Study Hours":
            col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
            with col1:
                plot_box(df, col)
            with col2:
                st.markdown("""
                            #### Analysis Summary
                            - Based on the box plot analysis, the graph suggests a minor trend where individuals who have experienced 
                            destructive thoughts ("Yes") tend to have slightly longer work/study hours, as indicated by a higher median 
                            (around 7 hours vs. 6 hours) and a higher upper quartile. However, the overall data distribution shows a 
                            significant overlap between the two groups, with both exhibiting a wide range of hours (from 0 to 12), 
                            which indicates that having destructive thoughts is not a strong or singular determinant of work/study 
                            duration.
                            """)

        elif col == "Financial Stress":
            col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
            with col1:
                plot_box(df, col)
            with col2:
                st.markdown("""
                            #### Analysis Summary
                            - This box plot compares financial stress levels between individuals who have and have not had destructive 
                            thoughts. The analysis reveals that the median financial stress level for both groups is identical, at 
                            approximately 3.0. Furthermore, the interquartile range(IQR), which represents the middle 50% of the data, 
                            is also the same for both groups (ranging from 2.0 to 4.0), and the overall range of financial stress 
                            scores (from a minimum of 1.0 to a maximum of 5.0) is consistent across both categories. The striking 
                            similarity in the median, distribution, and range of financial stress levels suggests that, according to 
                            this data, there is no significant difference in financial stress between those who have had destructive 
                            thoughts and those who have not.
                            """)
elif menu == "Correlation Matrix":





    col1, col2 = st.columns([2, 1])  # col1 geniş, col2 daha dar
    with col1:
        correlation(df)
    with col2:
        st.markdown("""
                        #### 
                        Analysis Summary
                        - This heat map is a correlation matrix displaying the linear relationships between four variables: 
                        Age, Job Satisfaction, Work/Study Hours, and Financial Stress. The color intensity and value of each 
                        cell represent the correlation coefficient, with warmer colors indicating a positive correlation and 
                        cooler colors a negative one.
                        - The analysis of the matrix reveals the following:
                        - Diagonal values are all 1.00, as a variable is perfectly correlated with itself.
                        - Age has a very weak positive correlation with Job Satisfaction (0.02) and weak negative 
                        correlations with Work/Study Hours (-0.12) and Financial Stress (-0.08). These relationships 
                        are not strong.
                        - Job Satisfaction has negligible correlations with Work/Study Hours (-0.02) and Financial Stress (-0.03), 
                        indicating almost no linear relationship between these variables.
                        - Work/Study Hours shows a very weak positive correlation with Financial Stress (0.05), 
                        suggesting a minimal and likely insignificant link.
                        """)
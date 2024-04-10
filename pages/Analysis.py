import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv('jobs_in_data.csv')  # Adjust the file path
    return data

# Main function
def main():
    st.title("Job Analysis Dashboard")

    # Load the dataset
    data = load_data()

    # Show the first few rows of the dataset
    if st.checkbox("Show Dataset"):
        st.write(data.head())

    # Job Category Distribution (Pie Chart)
    st.header("Job Category Distribution")
    st.write(data['job_category'].value_counts())
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data['job_category'].value_counts(), labels=data['job_category'].value_counts().index, autopct='%1.1f%%')
    st.pyplot(fig)

    # Salary Distribution (Histogram)
    st.header("Salary Distribution")
    plt.figure(figsize=(10, 6))
    sns.histplot(data['salary_in_usd'], bins=20, color='skyblue')
    st.pyplot()

    # Employment Type Distribution (Bar Chart)
    st.header("Employment Type Distribution")
    employment_type_counts = data['employment_type'].value_counts()
    st.bar_chart(employment_type_counts)

    # Experience Level Distribution (Pie Chart)
    st.header("Experience Level Distribution")
    st.write(data['experience_level'].value_counts())
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data['experience_level'].value_counts(), labels=data['experience_level'].value_counts().index, autopct='%1.1f%%')
    st.pyplot(fig)

    # Work Setting Distribution (Bar Chart)
    st.header("Work Setting Distribution")
    work_setting_counts = data['work_setting'].value_counts()
    st.bar_chart(work_setting_counts)

    # Conclusion
    st.header("Conclusion")
    st.write("1. The most common job category is:", data['job_category'].mode().iloc[0])
    st.write("2. The average salary in USD is:", data['salary_in_usd'].mean())
    st.write("3. The most common employment type is:", employment_type_counts.idxmax())
    st.write("4. The most common experience level is:", data['experience_level'].mode().iloc[0])
    st.write("5. The most common work setting is:", work_setting_counts.idxmax())

if __name__ == "__main__":
    main()

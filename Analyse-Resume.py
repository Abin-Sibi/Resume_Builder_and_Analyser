import streamlit as st
from PyPDF2 import PdfReader
import spacy
from spacy.matcher import PhraseMatcher
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from textblob import TextBlob

# st.set_page_config(page_title="This is the Multipage Webapp")
# st.sidebar.success("Select any page from here")

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment

# Function to extract keywords using NLP
def extract_keywords(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(keywords)
    most_common_words = word_freq.most_common(10)
    return most_common_words

# Function to check eligibility based on job role, experience, and degree
def check_eligibility(resume_text, job_role, experience_years, highest_degree):
    nlp = spacy.load('en_core_web_sm')
    matcher = PhraseMatcher(nlp.vocab)
    job_role_keywords = nlp(job_role.lower())
    experience_keywords = nlp(experience_years.lower())
    degree_keywords = nlp(highest_degree.lower())
    
    matcher.add('JOB_ROLE', None, job_role_keywords)
    matcher.add('EXPERIENCE', None, experience_keywords)
    matcher.add('DEGREE', None, degree_keywords)
    
    doc = nlp(resume_text.lower())
    matches = matcher(doc)
    
    if matches:
        return True
    else:
        return False

# Streamlit app
def main():
    st.title("Resume Analyzer")
    
    # Input fields
    job_role = st.text_input("Enter the job role:")
    experience_years = st.text_input("Enter years of experience:")
    highest_degree = st.text_input("Enter the highest degree or qualification:")
    
    # File upload moved to main page
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

    if uploaded_file is not None:
        # Read and display contents
        resume_text = extract_text_from_pdf(uploaded_file)
        st.header("Resume Content:")
        st.write(resume_text)

        # Sentiment analysis
        st.header("Sentiment Analysis:")
        sentiment = analyze_sentiment(resume_text)
        st.write("Polarity:", sentiment.polarity)
        st.write("Subjectivity:", sentiment.subjectivity)

        # Keyword extraction
        st.header("Keywords Extraction:")
        keywords = extract_keywords(resume_text)
        st.write("Top 10 Keywords:")
        for keyword, freq in keywords:
            st.write(keyword, ":", freq)

        # Check eligibility
        if job_role and experience_years and highest_degree:
            is_eligible = check_eligibility(resume_text, job_role, experience_years, highest_degree)
            if is_eligible:
                st.header("Eligibility Check:")
                st.write("Congratulations! You are eligible for the job.")
                st.write("Skills, projects, and other relevant information can be found in the resume.")
            else:
                st.header("Eligibility Check:")
                st.write("You are not eligible for the job. Please try again with a different resume or input.")
    
if __name__ == '__main__':
    main()

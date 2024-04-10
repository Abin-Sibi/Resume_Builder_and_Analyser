import streamlit as st
from PyPDF2 import PdfReader
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter
from textblob import TextBlob

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment

def extract_keywords(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(keywords)
    most_common_words = word_freq.most_common(10)
    return most_common_words

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

    # Calculate percentage of matches
    total_inputs = 3
    unique_matches = set()  # To store unique matches
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == 'JOB_ROLE':
            unique_matches.add('JOB_ROLE')
        elif nlp.vocab.strings[match_id] == 'EXPERIENCE':
            unique_matches.add('EXPERIENCE')
        elif nlp.vocab.strings[match_id] == 'DEGREE':
            unique_matches.add('DEGREE')

    percentage_matched = (len(unique_matches) / total_inputs) * 100

    # Check eligibility based on percentage
    if percentage_matched >= 60:
        return True, percentage_matched
    else:
        return False, percentage_matched

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
            is_eligible, percentage_matched = check_eligibility(resume_text, job_role, experience_years, highest_degree)
            st.header("Eligibility Check:")
            if is_eligible:
                st.write(f"Congratulations! You are eligible for the job with {percentage_matched:.2f}% match.")
                st.write("Skills, projects, and other relevant information can be found in the resume.")
            else:
                st.write(f"You are not eligible for the job. Your match percentage is {percentage_matched:.2f}%, which is below 60%. Please try again with a different resume or input.")
    
if __name__ == '__main__':
    main()

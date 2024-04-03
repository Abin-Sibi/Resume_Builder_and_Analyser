import streamlit as st

def show_about_page():
    st.title('About - Resume Projects')

    st.header('Resume Analyzer')
    st.write('The Resume Analyzer project allows users to upload a resume and input details such as years of experience, job role, and qualifications. The model then crosschecks the resume with the provided inputs to determine if the user is eligible for the job. If there is a match, it displays a message indicating eligibility for the job; otherwise, it shows a message indicating non-eligibility.')
    st.write('Example: [Resume Analyzer App](https://github.com/example)')

    st.header('Resume Builder')
    st.write('The Resume Builder project enables users to create a neat and professional resume by providing necessary details in a form. After entering details such as name, contact information, education, experience, skills, etc., the app generates a PDF resume with proper alignment, borders, and separation. Users can download the generated resume.')
    st.write('Example: [Resume Builder App](https://github.com/example)')

    st.subheader('Resume Builder Demo')
    st.write('Coming soon...')  # Placeholder for demo
    
    # Add more content and demos for each project as needed

if __name__ == '__main__':
    show_about_page()

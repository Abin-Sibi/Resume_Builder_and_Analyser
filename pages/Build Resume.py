import streamlit as st
from fpdf import FPDF
import base64
import os

def generate_resume(name, job_title, about, email, phone, address, skills, experience, education, projects, declaration):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Name and Job Title
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt=name, ln=True, align="C")
    pdf.cell(200, 10, txt=job_title, ln=True, align="C")
    pdf.ln(5)  # Adjust spacing

    # About You
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=about, align="C")
    pdf.ln(5)  # Adjust spacing
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw separation line
    pdf.ln(3)

    # Personal Information
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Personal Information", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True, align="L")
    pdf.ln(3)  # Adjust spacing
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw separation line
    pdf.ln(3)

    # Skills and Projects
    col_width = pdf.w / 2.2
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Skills", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(col_width, 10, txt=skills, align="L")
    pdf.set_x(col_width + 10)
    pdf.ln(3)  # Adjust spacing
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw separation line
    pdf.ln(3)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Projects", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(col_width, 10, txt=projects, align="L")
    pdf.ln(3)  # Adjust spacing
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw separation line
    pdf.ln(3)

    # Experience
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Experience", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=experience, align="L")
    pdf.ln(3)  # Adjust spacing
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw separation line
    pdf.ln(3)

    # Education
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Education", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=education, align="L")
    pdf.ln(3)  # Adjust spacing
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw separation line
    pdf.ln(3)

    # Declaration
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Declaration", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=declaration, align="L")

    # Save PDF
    pdf_output_path = f"{name}_resume.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path


# Function to display the PDF demo
def display_demo(pdf_bytes):
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    return f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="800" type="application/pdf">'

# Streamlit app
def main():
    st.title("Resume Builder")

    # Input fields
    name = st.text_input("Name:")
    job_title = st.text_input("Job Title:")
    about = st.text_area("About You:")
    email = st.text_input("Email:")
    phone = st.text_input("Phone:")
    address = st.text_area("Address:")
    skills = st.text_area("Skills (comma-separated):")
    experience = st.text_area("Experience:")
    education = st.text_area("Education:")
    projects = st.text_area("Projects:")
    declaration = st.text_area("Declaration:")

    # Generate Resume button
    if st.button("Generate Resume"):
        if name and job_title and about and email and phone and address and skills and experience and education and projects and declaration:
            pdf_path = generate_resume(name, job_title, about, email, phone, address, skills, experience, education, projects, declaration)
            with open(pdf_path, "rb") as file:
                pdf_bytes = file.read()
            st.subheader("Resume Demo")
            st.markdown(display_demo(pdf_bytes), unsafe_allow_html=True)
            st.subheader("Download Resume")
            st.markdown(f'<a href="data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode()}" download="{os.path.basename(pdf_path)}">Click here to download the PDF</a>', unsafe_allow_html=True)
            os.remove(pdf_path)

if __name__ == "__main__":
    main()

import streamlit as st
from fpdf import FPDF
import os

# Set up quiz questions and answers
questions = {
    "What is the function of a CPU?": ("Process data", ["Store data", "Display output", "Process data", "Print data"]),
    "Which of the following is an input device?": ("Mouse", ["Monitor", "Speaker", "Mouse", "Printer"]),
    "What does RAM stand for?": ("Random Access Memory", ["Read And Modify", "Run Active Memory", "Random Access Memory", "Run Automated Memory"]),
    "Which file format is used for documents?": ("DOCX", ["MP3", "DOCX", "EXE", "PNG"]),
    "What is the internet?": ("A global network", ["A local software", "A printer", "A global network", "A web browser"])
}

st.title("🎓 Fundamentals Course Final Quiz")
st.markdown("Answer the questions below. You need 70% to pass and receive a certificate.")

name = st.text_input("Enter your full name")

score = 0
responses = {}

if name:
    for q, (correct, options) in questions.items():
        answer = st.radio(q, options, key=q)
        responses[q] = answer
        if answer == correct:
            score += 1

    if st.button("Submit Quiz"):
        total = len(questions)
        percentage = (score / total) * 100
        st.write(f"✅ **Your Score:** {score}/{total} ({percentage:.0f}%)")

        if percentage >= 70:
            st.success("Congratulations! You passed the quiz.")

            # Generate certificate
            pdf = FPDF(orientation='L')
            pdf.add_page()
            pdf.set_font("Arial", "B", 24)
            pdf.cell(0, 50, "Certificate of Completion", ln=True, align="C")
            pdf.set_font("Arial", "", 16)
            pdf.cell(0, 10, f"Awarded to: {name}", ln=True, align="C")
            pdf.cell(0, 10, f"For successfully passing the Fundamentals Course Quiz.", ln=True, align="C")

            cert_path = f"{name.replace(' ', '_')}_certificate.pdf"
            pdf.output(cert_path)

            with open(cert_path, "rb") as f:
                st.download_button("📄 Download Your Certificate", f, file_name="certificate.pdf")

            os.remove(cert_path)
        else:
            st.error("Sorry, you did not pass. Try again!")

else:
    st.info("Please enter your name to start the quiz.")


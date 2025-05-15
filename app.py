# skillvite_quiz_app.py
import os
from datetime import datetime
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
client = gspread.authorize(creds)

sheet = client.open_by_key("1AoQYzcuprY8qzp5P0NyhNZm249aRQ59V34U9zoL6slc").sheet1  # You can rename this sheet as needed

# ------------------ Quiz Questions ------------------
questions = [
    {"question": "What is the main function of a computer?", "options": ["Cooking", "Storing and processing data", "Playing music"], "answer": "Storing and processing data"},
    {"question": "Which of the following is an input device?", "options": ["Monitor", "Keyboard", "Speaker"], "answer": "Keyboard"},
    {"question": "Which port is commonly used to connect a keyboard?", "options": ["HDMI", "USB", "Ethernet"], "answer": "USB"},
    {"question": "Which generation of computers used microprocessors?", "options": ["First", "Third", "Fourth"], "answer": "Fourth"},
    {"question": "Which part of a computer is called the brain?", "options": ["Monitor", "CPU", "RAM"], "answer": "CPU"},
    {"question": "What is an Operating System?", "options": ["An antivirus program", "A software that manages hardware and software", "A game"], "answer": "A software that manages hardware and software"},
    {"question": "Which of these is an application software?", "options": ["Windows", "MS Word", "BIOS"], "answer": "MS Word"},
    {"question": "Which one is used to browse the internet?", "options": ["Google Chrome", "Excel", "Paint"], "answer": "Google Chrome"},
    {"question": "How do you protect a computer from viruses?", "options": ["Install antivirus", "Use internet a lot", "Open spam emails"], "answer": "Install antivirus"},
    {"question": "What is the full form of CPU?", "options": ["Central Process Unit", "Central Processing Unit", "Computer Processing Unit"], "answer": "Central Processing Unit"},
    {"question": "Which is faster: Laptop or Desktop (generally)?", "options": ["Laptop", "Desktop", "They are the same"], "answer": "Desktop"},
    {"question": "What is a cloud server used for?", "options": ["Making rain", "Storing files online", "Cooling computers"], "answer": "Storing files online"},
    {"question": "Which key is used to delete?", "options": ["Enter", "Del", "Esc"], "answer": "Del"},
    {"question": "Which device connects a computer to the internet?", "options": ["Scanner", "Router", "Printer"], "answer": "Router"},
    {"question": "What is phishing?", "options": ["A way to catch fish", "A scam to steal information", "A type of software"], "answer": "A scam to steal information"},
    {"question": "What does a search engine do?", "options": ["Stores data", "Finds information online", "Cleans your computer"], "answer": "Finds information online"},
    {"question": "What is Windows?", "options": ["A door", "An OS", "A folder"], "answer": "An OS"},
    {"question": "Which software is used to type documents?", "options": ["PowerPoint", "MS Word", "Excel"], "answer": "MS Word"},
    {"question": "How can you install a new program?", "options": ["Use install file", "Delete old files", "Restart PC"], "answer": "Use install file"},
    {"question": "What is spam?", "options": ["Useful email", "Unwanted email", "Normal email"], "answer": "Unwanted email"},
    {"question": "How do you uninstall software?", "options": ["Delete desktop icon", "Control Panel > Uninstall", "Turn off computer"], "answer": "Control Panel > Uninstall"},
    {"question": "What do you need to set up a desktop?", "options": ["Only monitor", "Monitor, CPU, Keyboard, Mouse", "TV"], "answer": "Monitor, CPU, Keyboard, Mouse"},
    {"question": "Which part stores long-term data?", "options": ["RAM", "Hard Drive", "Cache"], "answer": "Hard Drive"},
    {"question": "What is digital tracking?", "options": ["Finding your location online", "Opening files", "Using a mouse"], "answer": "Finding your location online"},
    {"question": "What might computers be like in the future?", "options": ["Slower", "Faster and smaller", "No change"], "answer": "Faster and smaller"}
]

# ------------------ Certificate Generator ------------------
def generate_certificate(name):
    template = Image.open("certificate_template.png")
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("arialbd.ttf", 45)
    draw.text((300, 450), name, font=font, fill="black")

    # ✅ Ensure the 'certificates' folder exists
    os.makedirs("certificates", exist_ok=True)

    cert_path = f"certificates/{name.replace(' ', '_')}_certificate.png"
    template.save(cert_path)
    return cert_path

# ------------------ App UI ------------------
st.set_page_config(page_title="Skillvite Quiz", layout="centered")
st.title("🖥️ Computer Fundamentals Final Quiz")

name = st.text_input("Enter your full name to begin:")

if name:
    score = 0
    selected_answers = {}
    questions_sample = questions[:25]

    for i, q in enumerate(questions_sample):
        st.subheader(f"Q{i+1}. {q['question']}")
        answer = st.radio("", q['options'], key=i)
        selected_answers[q['question']] = answer
        if answer == q['answer']:
            score += 1

    if st.button("Submit Quiz"):
        st.success(f"You scored {score}/25")

        # Store result in Google Sheet
        sheet.append_row([name, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        if score >= 20:
            cert_path = generate_certificate(name)
            st.success("🎉 Congratulations! You passed the quiz.")
            st.image(cert_path, caption="Your Certificate", use_container_width=True)
            with open(cert_path, "rb") as file:
                st.download_button("📥 Download Certificate", data=file, file_name=f"{name}_certificate.png")
        else:
            st.warning("You did not pass. Please try again.")

        st.subheader("📣 We value your feedback!")
feedback = st.text_area("Let us know what you think about this course:")
if st.button("Submit Feedback"):
    feedback_sheet = client.open_by_key("1AoQYzcuprY8qzp5P0NyhNZm249aRQ59V34U9zoL6slc").worksheet("Feedback")
    feedback_sheet.append_row([name, feedback, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    st.success("✅ Thank you for your feedback!")

    # Display count of participants
    all_records = sheet.get_all_records()
    student_count = len([row for row in all_records if isinstance(row.get("Score"), int)])
    st.info(f"📊 Total students who attempted the quiz: {student_count}")

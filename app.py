import streamlit as st
import pandas as pd
from AdFaceSelect import topsis
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(recipient_email, subject, body, attachment):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Add body and attachment
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(attachment)

    try:
        # SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False

st.title("Ad Face Select - TOPSIS")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
weights = st.text_input("Enter weights (comma separated)")
impacts = st.text_input("Enter impacts (+ or - separated by comma)")
email = st.text_input("Enter your email address")

if st.button("Submit"):
    if uploaded_file is not None and weights and impacts and email:
        df = pd.read_csv(uploaded_file)
        df.to_csv("input_file.csv", index=False)
        try:
            result = topsis("input_file.csv", weights, impacts, "output_file.csv")
            result_csv = result.to_csv(index=False)
            result_file = "output_file.csv"
            with open(result_file, "w") as f:
                f.write(result_csv)
            
            with open(result_file, "r") as f:
                attachment = MIMEText(f.read(), "base64")
                attachment.add_header("Content-Disposition", "attachment", filename=result_file)

            email_sent = send_email(
                recipient_email=email,
                subject="TOPSIS Results",
                body="Please find the attached TOPSIS results.",
                attachment=attachment
            )

            if email_sent:
                st.success("TOPSIS results sent successfully!")
            else:
                st.error("Failed to send TOPSIS results.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please fill all the fields correctly.")

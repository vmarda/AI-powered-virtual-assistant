import speech_recognition as sr
import pyttsx3
from datetime import datetime
import gpt_2_simple as gpt2
import smtplib
import webbrowser
import subprocess
import tensorflow as tf

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize the GPT-2 model
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to send an email via SMTP
def send_email(to, subject, body):
    # Configure your email settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(sender_email, to, message)
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        speak("Sorry, I couldn't send the email. Please try again later.")

# Function to perform a web search
def search(query):
    url = f'https://www.google.com/search?q={query}'
    webbrowser.open(url)

# Function to open an application
def open_app(app_name):
    try:
        subprocess.Popen(app_name)
        speak(f"Opening {app_name}")
    except Exception:
        speak(f"Sorry, I couldn't open {app_name}. Please check if it's installed.")

# Function to generate a response using GPT-2
def generate_response(prompt):
    response = gpt2.generate(sess, model_name='124M', prefix=prompt, length=100, temperature=0.7, return_as_list=True)[0]
    return response

# Main program loop
with sr.Microphone() as source:
    print("Listening...")
    while True:
        audio = recognizer.listen(source)

        # Convert speech to text
        command = recognizer.recognize_google(audio)
        print("You said:", command)

        # Process the command
        if 'Matilda' in command:
            speak("Hello! How can I assist you today?")
            while True:
                print("Listening...")
                audio = recognizer.listen(source)
                query = recognizer.recognize_google(audio)
                print("You said:", query)

                if 'exit' in query:
                    speak("Goodbye!")
                    break
                elif 'send email' in query:
                    speak("To whom would you like to send the email?")
                    audio = recognizer.listen(source)
                    recipient = recognizer.recognize_google(audio)
                    speak("What is the subject of the email?")
                    audio = recognizer.listen(source)
                    subject = recognizer.recognize_google(audio)
                    speak("What should the email say?")
                    audio = recognizer.listen(source)
                    body = recognizer.recognize_google(audio)
                    send_email(recipient, subject, body)
                elif 'search' in query:
                    search_query = query.replace('search', '', 1).strip()
                    search(search_query)
                elif 'open app' in query:
                    app_name = query.replace('open app', '', 1).strip()
                    open_app(app_name)
                else:
                    response = generate_response(query)
                    speak(response)
        else:
            speak("Sorry, I didn't catch that. Could you please call me as Matilda?")
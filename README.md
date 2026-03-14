MailPilot – Email Campaign Automation Tool

MailPilot is a desktop application built in Python that allows sending personalized email campaigns using a CSV contact list.

The application connects to an SMTP server (for example Gmail), loads contacts from a CSV file, and sends individualized messages to each recipient.

MailPilot is designed for:

recruitment outreach

lead generation

customer communication

automated follow-ups

email campaign testing

Each email is sent individually, which ensures that recipients cannot see other addresses.

Features

SMTP email sending

CSV contact import

Personalized email templates

Email validation

Attachments support

Delay between emails

Campaign start / stop control

Campaign save / load

Contact preview

Live logs during sending

Progress bar

Desktop GUI application

Executable build support

Email Personalization

MailPilot supports simple template variables.

Example template:

Hello {name},

This is a test message sent with MailPilot.

If the CSV file contains:

email,name
john@gmail.com,John
anna@gmail.com,Anna

The sent messages will automatically become:

Hello John
Hello Anna
Technologies Used

Python

Libraries:

CustomTkinter

Pandas

SMTP (smtplib)

JSON

Threading

Installation

Clone the repository

git clone https://github.com/czuameni/mail-pilot.git

Enter the project folder

cd mail-pilot

Install dependencies

pip install -r requirements.txt
Running the Application

Run the program

python main.py

The MailPilot GUI window will open.

CSV Contact Format

Contacts must be stored in CSV format.

Example:

email,name
john@gmail.com,John
anna@gmail.com,Anna
mike@gmail.com,Mike

Required columns:

email

name

Gmail Setup (App Password)

If you use Gmail, you must generate an App Password.

Steps:

Open your Google Account security settings

Enable 2-Step Verification

Go to App Passwords

Generate a password for Mail

Use that password in the MailPilot App Password field

Usage

Enter the sender email address

Enter the App Password

Write the email subject

Write the email body

Set delay between messages

(Optional) add attachment

Load contacts from CSV

Click Start Campaign

The application will start sending emails one by one.

You can stop the process anytime using Stop Campaign.

Campaign Management

MailPilot allows saving campaign settings.

Save campaign:

Save Campaign

Load campaign:

Load Campaign

Campaign settings are stored in JSON format.

Project Structure
main.py
gui.py
smtp_client.py
email_sender.py
contact_loader.py
template_engine.py
validator.py
logger.py

requirements.txt
README.md
INSTRUKCJA.txt

examples.csv
mailpilot.ico
Application Interface

Main components:

SMTP SETTINGS
Sender email and App Password

CAMPAIGN
Subject, message body, delay and attachments

CONTACTS
CSV import and contact preview

CONTROL
Start / Stop / Save / Load campaign

LOGS
Real-time campaign activity

Example Use Cases

recruitment outreach campaigns

lead generation emails

cold email testing

internal notification automation

marketing message distribution

License

This project is released under the MIT License.

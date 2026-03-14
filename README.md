# MailPilot

MailPilot is a desktop application for automated email campaigns built with Python and CustomTkinter.

The application allows sending personalized emails to multiple recipients using a CSV contact list.

Features:

• SMTP email sending
• Personalized messages using {name}
• CSV contact import
• Email validation
• Attachments support
• Delay between emails
• Campaign save/load
• Campaign stop control
• Live logs
• Contact preview

Technologies used:

Python  
CustomTkinter  
SMTP  
Pandas


## Installation

Install dependencies:

pip install -r requirements.txt


Run the application:

python main.py


## CSV Format

Contacts must be stored in CSV format:

email,name

Example:

john@gmail.com,John
anna@gmail.com,Anna
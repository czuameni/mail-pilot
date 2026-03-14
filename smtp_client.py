import smtplib


def connect_smtp(email, password, smtp_server="smtp.gmail.com", port=587):

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()

    server.login(email, password)

    return server
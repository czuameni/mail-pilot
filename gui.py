import customtkinter as ctk
from tkinter import filedialog
import time
import threading
import json

from smtp_client import connect_smtp
from contact_loader import load_contacts
from template_engine import render_template
from email_sender import send_email
from logger import log
from validator import is_valid_email


class MailPilotApp:

    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("MailPilot")
        self.root.geometry("750x650")

        self.contacts = []
        self.running = False
        self.attachment_path = None

        self.attachment_path = None

        self.main_frame = ctk.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):

        main = ctk.CTkFrame(self.main_frame)
        main.pack(fill="both", expand=True, padx=120, pady=20)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)


        left = ctk.CTkFrame(main)
        left.grid(row=0, column=0, padx=20, sticky="nw")

        right = ctk.CTkFrame(main)
        right.grid(row=0, column=1, padx=20, sticky="nw")

        left.configure(width=420)


        smtp_frame = ctk.CTkFrame(left)
        smtp_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(smtp_frame, text="SMTP SETTINGS").pack(pady=5)

        self.email_entry = ctk.CTkEntry(smtp_frame, placeholder_text="Sender email")
        self.email_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(smtp_frame, placeholder_text="App Password", show="*")
        self.password_entry.pack(pady=5)


        contacts_frame = ctk.CTkFrame(left)
        contacts_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(contacts_frame, text="CONTACTS").pack(pady=5)

        load_btn = ctk.CTkButton(contacts_frame, text="Load CSV", command=self.load_contacts)
        load_btn.pack(pady=5)

        self.contact_label = ctk.CTkLabel(contacts_frame, text="Contacts loaded: 0")
        self.contact_label.pack()

        self.preview_box = ctk.CTkTextbox(contacts_frame, height=120)
        self.preview_box.pack(fill="x", expand=True, pady=5)


        campaign_frame = ctk.CTkFrame(right)
        campaign_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(campaign_frame, text="CAMPAIGN").pack(pady=5)

        self.subject_entry = ctk.CTkEntry(campaign_frame, placeholder_text="Subject")
        self.subject_entry.pack(pady=5)

        self.body_box = ctk.CTkTextbox(campaign_frame, height=180)
        self.body_box.pack(pady=5)

        self.delay_entry = ctk.CTkEntry(campaign_frame, placeholder_text="Delay seconds")
        self.delay_entry.pack(pady=5)

        attach_btn = ctk.CTkButton(campaign_frame, text="Add Attachment", command=self.add_attachment)
        attach_btn.pack(pady=5)

        self.attachment_label = ctk.CTkLabel(campaign_frame, text="No attachment")
        self.attachment_label.pack()


        control_frame = ctk.CTkFrame(right)
        control_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(control_frame, text="CONTROL").pack(pady=5)

        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(pady=5)

        left_buttons = ctk.CTkFrame(button_frame)
        left_buttons.grid(row=0, column=0, padx=10)

        right_buttons = ctk.CTkFrame(button_frame)
        right_buttons.grid(row=0, column=1, padx=10)

        start_btn = ctk.CTkButton(left_buttons, text="Start Campaign", command=self.start_thread)
        start_btn.pack(pady=5)

        stop_btn = ctk.CTkButton(left_buttons, text="Stop Campaign", command=self.stop_campaign)
        stop_btn.pack(pady=5)

        save_btn = ctk.CTkButton(right_buttons, text="Save Campaign", command=self.save_campaign)
        save_btn.pack(pady=5)

        load_btn = ctk.CTkButton(right_buttons, text="Load Campaign", command=self.load_campaign)
        load_btn.pack(pady=5)


        self.progress = ctk.CTkProgressBar(self.main_frame)
        self.progress.pack(fill="x", padx=40, pady=10)
        self.progress.set(0)


        logs_frame = ctk.CTkFrame(self.main_frame)
        logs_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(logs_frame, text="LOGS").pack(pady=5)

        self.log_box = ctk.CTkTextbox(logs_frame, height=150)
        self.log_box.pack(fill="both", expand=True)

    def log_gui(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def load_contacts(self):

        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if path:
            self.contacts = load_contacts(path)
            self.contact_label.configure(text=f"Contacts loaded: {len(self.contacts)}")
            self.log_gui(f"Loaded {len(self.contacts)} contacts")

            self.preview_box.delete("1.0", "end")

            for contact in self.contacts[:20]:

                line = f"{contact['email']} | {contact['name']}"
                self.preview_box.insert("end", line + "\n")

    def add_attachment(self):

        path = filedialog.askopenfilename()

        if path:
            self.attachment_path = path
            self.attachment_label.configure(text=f"Attachment: {path.split('/')[-1]}")

    def start_thread(self):

        thread = threading.Thread(target=self.start_campaign)
        thread.start()

    def start_campaign(self):

        self.running = True

        email = self.email_entry.get()
        password = self.password_entry.get()
        subject = self.subject_entry.get()
        body_template = self.body_box.get("1.0", "end")
        delay = int(self.delay_entry.get())

        self.log_gui("Connecting to SMTP...")

        server = connect_smtp(email, password)

        total = len(self.contacts)
        sent = 0

        for contact in self.contacts:

            if not self.running:
                self.log_gui("Campaign stopped")
                break

            if not is_valid_email(contact["email"]):

                msg = f"Invalid email skipped: {contact['email']}"
                self.log_gui(msg)
                log(msg)

                continue

            try:

                body = render_template(body_template, contact)

                send_email(
                    server,
                    email,
                    contact["email"],
                    subject,
                    body,
                    self.attachment_path
                )

                sent += 1

                progress = sent / total
                self.progress.set(progress)

                msg = f"Sent: {contact['email']}"
                self.log_gui(msg)
                log(msg)

                time.sleep(delay)

            except Exception as e:

                error = f"Failed: {contact['email']} ({str(e)})"
                self.log_gui(error)
                log(error)

        self.log_gui("Campaign finished")

    def stop_campaign(self):

        self.running = False

    def save_campaign(self):

        data = {

            "subject": self.subject_entry.get(),
            "body": self.body_box.get("1.0", "end"),
            "delay": self.delay_entry.get(),
            "attachment": self.attachment_path

        }

        path = filedialog.asksaveasfilename(defaultextension=".json")

        if path:

            with open(path, "w") as f:
                json.dump(data, f)

            self.log_gui("Campaign saved")

    def load_campaign(self):

        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

        if path:

            with open(path) as f:
                data = json.load(f)

            self.subject_entry.delete(0, "end")
            self.subject_entry.insert(0, data["subject"])

            self.body_box.delete("1.0", "end")
            self.body_box.insert("1.0", data["body"])

            self.delay_entry.delete(0, "end")
            self.delay_entry.insert(0, data["delay"])

            self.attachment_path = data["attachment"]

            if self.attachment_path:
                self.attachment_label.configure(
                    text=f"Attachment: {self.attachment_path.split('/')[-1]}"
                )

            self.log_gui("Campaign loaded")        

    def run(self):
        self.root.mainloop()

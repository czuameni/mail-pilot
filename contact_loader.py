import pandas as pd


def load_contacts(csv_path):
    df = pd.read_csv(csv_path)

    contacts = []

    for _, row in df.iterrows():
        contacts.append({
            "email": row.get("email"),
            "name": row.get("name", "")
        })

    return contacts
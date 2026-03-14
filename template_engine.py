def render_template(template, contact):
    text = template

    for key, value in contact.items():
        placeholder = "{" + key + "}"
        text = text.replace(placeholder, str(value))

    return text
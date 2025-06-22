import gooeypie as gp
import string
import random
import pyperclip
import hashlib
import requests

# Load common passwords from file
List_of_passwords = []
with open('Pwdb_top-10000.txt', 'r') as file:
    for line in file:
        for word in line.split():
            List_of_passwords.append(word.strip().lower())

# Password checker function
def check_password(event):
    user_password = password_box.text
    lower_password = user_password.lower()

    password_feedback.text = "Length Check: ✅ Passed" if len(user_password) >= 8 else "Length Check: ❌ Too short"
    password_feedback_2.text = "Digit Check: ✅ Passed" if any(char.isdigit() for char in user_password) else "Digit Check: ❌ Must contain at least one number"
    password_feedback_3.text = "Special Char Check: ✅ Passed" if any(char in string.punctuation for char in user_password) else "Special Char Check: ❌ Must include a special character"
    password_feedback_4.text = "Common Password Check: ✅ Passed" if lower_password not in List_of_passwords else "Common Password Check: ❌ Too common!"

    sha1_pw = hashlib.sha1(user_password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_pw[:5]
    suffix = sha1_pw[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code == 200:
            hashes = response.text.splitlines()
            found = any(line.split(':')[0] == suffix for line in hashes)
            if found:
                password_feedback_5.text = "Password Breach Check: ❌ This password has appeared in a data breach!"
            else:
                password_feedback_5.text = "Password Breach Check: ✅ This password has not been found in breaches"
        else:
            password_feedback_5.text = "HIBP Breach Check: ⚠️ Error checking HIBP"
    except Exception:
        password_feedback_5.text = "HIBP Breach Check: ⚠️ Failed to connect"

def clear_generated_password():
    generated_password_box.text = ''
    generated_password_lbl.text = '🔒 Password cleared after 2 minutes.'

def copy_password(event):
    pw = generated_password_box.text
    if pw:
        pyperclip.copy(pw)
        generated_password_lbl.text = "📋 Password copied to clipboard!"
    else:
        generated_password_lbl.text = "❌ No password to copy."

def matrix_effect_and_generate(event):
    length = length_slider.value
    characters = string.ascii_lowercase
    if include_uppercase.checked:
        characters += string.ascii_uppercase
    if include_digits.checked:
        characters += string.digits
    if include_specials.checked:
        characters += string.punctuation

    if not characters:
        generated_password_lbl.text = "❌ Choose at least one character type"
        generated_password_box.text = ''
        return

    animation_steps = 20
    animation_delay = 50
    colors = ['green', 'lime', 'lightgreen', 'darkgreen']

    def show_random(step=0):
        if step < animation_steps:
            random_text = ''.join(random.choice(characters) for _ in range(length))
            generated_password_box.text = random_text
            generated_password_box.foreground = random.choice(colors)
            app.after(animation_delay, lambda: show_random(step + 1))
        else:
            password = ''.join(random.choice(characters) for _ in range(length))
            generated_password_box.text = password
            generated_password_box.foreground = 'black'
            generated_password_lbl.text = f"✅ Password generated! (Length: {length})"
            app.after(120000, clear_generated_password)

    show_random()

def open_help(event):
    help_app = gp.GooeyPieApp('Help')
    help_app.width = 500
    help_app.height = 400
    help_app.set_grid(10, 1)

    help_text = (
        "Locked Away was developed by Josh Kenny\n"
        "Released under GNU General Public License\n\n"
        "Features supported:\n"
        "- Password Length: Use longer passwords\n"
        "- Password Complexity: Mix letters, numbers, symbols\n"
        "- Save to clipboard: Copy your password\n"
        "- Checks common passwords and known breaches\n"
    )
    help_label = gp.Label(help_app, help_text)
    help_label.wrap = True
    help_app.add(help_label, 1, 1)
    help_app.run()

def update_length_value_label(event):
    length_value_lbl.text = str(length_slider.value)

show_password = True
def toggle_password_visibility(event):
    global show_password
    show_password = not show_password
    password_box.secret = not show_password
    toggle_password_btn.text = 'Hide' if show_password else 'Show'

app = gp.GooeyPieApp('Locked Away')
app.width = 750
app.height = 600
app.set_grid(30, 3)  # Increased rows to 30

app.set_column_weights(0, 1, 1)

title_lbl = gp.Label(app, '🔐 Locked Away')
title_lbl.font = ('Arial', 20, 'bold')
app.add(title_lbl, 1, 1, colspan=2)

help_button = gp.Button(app, 'Help', open_help)
help_button.font = ('Arial', 10)
app.add(help_button, 1, 3)

# -------- Password Checker --------
checker_container = gp.Container(app)
checker_container.set_grid(9, 3)

checker_title = gp.Label(checker_container, 'Password Strength Checker')
checker_title.font = ('Arial', 14, 'bold')
checker_container.add(checker_title, 1, 1, colspan=3)

password_lbl = gp.Label(checker_container, 'Enter your password:')
password_box = gp.Textbox(checker_container, 35)
password_box.secret = True

submit = gp.Button(checker_container, 'Check Password', check_password)
toggle_password_btn = gp.Button(checker_container, 'Show', toggle_password_visibility)

password_feedback = gp.Label(checker_container, "Length Check: ")
password_feedback_2 = gp.Label(checker_container, "Digit Check: ")
password_feedback_3 = gp.Label(checker_container, "Special Char Check: ")
password_feedback_4 = gp.Label(checker_container, "Common Password Check: ")
password_feedback_5 = gp.Label(checker_container, "HIBP Breach Check: ")

checker_container.add(password_lbl, 2, 1)
checker_container.add(password_box, 2, 2)
checker_container.add(toggle_password_btn, 2, 3)
checker_container.add(submit, 3, 2)

checker_container.add(password_feedback, 4, 1, colspan=3)
checker_container.add(password_feedback_2, 5, 1, colspan=3)
checker_container.add(password_feedback_3, 6, 1, colspan=3)
checker_container.add(password_feedback_4, 7, 1, colspan=3)
checker_container.add(password_feedback_5, 8, 1, colspan=3)

app.add(checker_container, 2, 1, colspan=1)

# -------- Password Generator --------
generator = gp.Container(app)
generator.set_grid(10, 2)

generator_title = gp.Label(generator, 'Password Generator')
generator_title.font = ('Arial', 18, 'bold')
generator.add(generator_title, 1, 1, colspan=1)

length_lbl = gp.Label(generator, 'Length:')
length_slider = gp.Slider(generator, 4, 32, orientation='horizontal')
length_value_lbl = gp.Label(generator, str(length_slider.value))

include_uppercase = gp.Checkbox(generator, 'Include Uppercase Letters')
include_digits = gp.Checkbox(generator, 'Include Numbers')
include_specials = gp.Checkbox(generator, 'Include Special Characters')

generate_button = gp.Button(generator, 'Generate Password', matrix_effect_and_generate)
copy_button = gp.Button(generator, 'Copy Password', copy_password)

generated_password_lbl = gp.Label(generator, '')
generated_password_box = gp.Textbox(generator, 30)
generated_password_box.readonly = True

generator.add(length_lbl, 2, 1)
generator.add(length_slider, 2, 2)
generator.add(length_value_lbl, 3, 2)

generator.add(include_uppercase, 4, 1)
generator.add(include_digits, 5, 1)
generator.add(include_specials, 6, 1)

generator.add(generate_button, 7, 1)
generator.add(copy_button, 7, 2)
generator.add(generated_password_lbl, 8, 1, colspan=2)
generator.add(generated_password_box, 9, 1, colspan=2)

app.add(generator, 10, 1, colspan=3)

length_slider.add_event_listener('change', update_length_value_label)

app.run()

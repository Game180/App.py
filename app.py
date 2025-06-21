import gooeypie as gp
import string
import random
import pyperclip  # For clipboard copy (install with pip if needed)

# Load common passwords from file (lowercase and stripped)
List_of_passwords = []
with open('Pwdb_top-10000.txt', 'r') as file:
    for line in file:
        for word in line.split():
            List_of_passwords.append(word.strip().lower())

# Password check function
def check_password(event):
    user_password = password_box.text
    lower_password = user_password.lower()

    # Length check
    if len(user_password) < 8:
        password_feedback.text = "Length Check: ❌ Too short"
    else:
        password_feedback.text = "Length Check: ✅ Passed"

    # Digit check
    if not any(char.isdigit() for char in user_password):
        password_feedback_2.text = "Digit Check: ❌ Must contain at least one number"
    else:
        password_feedback_2.text = "Digit Check: ✅ Passed"

    # Special character check
    if any(char in string.punctuation for char in user_password):
        password_feedback_3.text = "Special Character Check: ✅ Passed"
    else:
        password_feedback_3.text = "Special Character Check: ❌ Must include a special character"

    # Common password check
    if lower_password in List_of_passwords:
        password_feedback_4.text = "Common Password Check: ❌ Too common! Choose a stronger password."
    else:
        password_feedback_4.text = "Common Password Check: ✅ Passed"

# Clear generated password after 2 minutes
def clear_generated_password():
    generated_password_box.text = ''
    generated_password_lbl.text = '🔒 Password cleared after 2 minutes.'

# Copy password to clipboard
def copy_password(event):
    pw = generated_password_box.text
    if pw:
        pyperclip.copy(pw)
        generated_password_lbl.text = "📋 Password copied to clipboard!"
    else:
        generated_password_lbl.text = "❌ No password to copy."

# Password generator with Matrix effect animation
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
    animation_delay = 50  # milliseconds

    def show_random(step=0):
        if step < animation_steps:
            random_text = ''.join(random.choice(characters) for _ in range(length))
            generated_password_box.text = random_text
            app.after(animation_delay, lambda: show_random(step + 1))
        else:
            password = ''.join(random.choice(characters) for _ in range(length))
            generated_password_box.text = password
            generated_password_lbl.text = f"✅ Password generated! (Length: {length})"
            # Start timer to clear password after 2 minutes
            app.after(120000, clear_generated_password)

    show_random()

# Open Help window
def open_help(event):
    help_app = gp.GooeyPieApp('Help')
    help_app.width = 500
    help_app.height = 400
    help_app.set_grid(10, 1)

    help_text = (
        "Locked Away was developed by Josh Kenny\n"
        "Released under GNU General Public License\n\n"
        "Features supported:\n"
        "- Password Length: Use longer passwords for strength\n"
        "- Password Complexity: Mix letters, numbers, symbols\n"
        "- Save to clipboard: Copy your generated password\n"
        "  Note: Password clears after 2 minutes\n"
    )
    help_label = gp.Label(help_app, help_text)
    help_label.wrap = True
    help_app.add(help_label, 1, 1)
    help_app.run()

# Update slider label
def update_length_value_label(event):
    length_value_lbl.text = str(length_slider.value)

# Create main app window
app = gp.GooeyPieApp('Locked Away')
app.width = 700
app.height = 550
app.set_grid(15, 3)
app.set_column_weights(0, 1, 1)

# Title and Help label (styled as button)
title_lbl = gp.Label(app, '🔐 Locked Away')
title_lbl.font = ('Arial', 24, 'bold')
app.add(title_lbl, 1, 1, colspan=2)

help_button = gp.Button(app, 'Help', open_help)
help_button.background = 'blue'
help_button.foreground = 'white'
help_button.font = ('Arial', 12, 'bold')
help_button.padding = 5
app.add(help_button, 1, 3)
help_button.add_event_listener('press', open_help)

# -------- Password Checker Container --------
checker_container = gp.Container(app)
checker_container.set_grid(7, 2)

checker_title = gp.Label(checker_container, 'Password Strength Checker')
checker_title.font = ('Arial', 16, 'bold')
checker_container.add(checker_title, 1, 1, colspan=2)

password_lbl = gp.Label(checker_container, 'Enter your password:')
password_box = gp.Textbox(checker_container, 35, 1)

submit = gp.Button(checker_container, 'Check Password', check_password)

password_feedback = gp.Label(checker_container, "Length Check: ")
password_feedback_2 = gp.Label(checker_container, "Digit Check: ")
password_feedback_3 = gp.Label(checker_container, "Special Char Check: ")
password_feedback_4 = gp.Label(checker_container, "Common Password Check: ")

checker_container.add(password_lbl, 2, 1)
checker_container.add(password_box, 2, 2)
checker_container.add(submit, 3, 2)
checker_container.add(password_feedback, 4, 1, colspan=2)
checker_container.add(password_feedback_2, 5, 1, colspan=2)
checker_container.add(password_feedback_3, 6, 1, colspan=2)
checker_container.add(password_feedback_4, 7, 1, colspan=2)

app.add(checker_container, 2, 1, colspan=2)

# -------- Password Generator Container --------
generator_container = gp.Container(app)
generator_container.set_grid(8, 2)

generator_title = gp.Label(generator_container, 'Password Generator')
generator_title.font = ('Arial', 16, 'bold')
generator_container.add(generator_title, 1, 1, colspan=2)

length_lbl = gp.Label(generator_container, 'Length:')
length_slider = gp.Slider(generator_container, 4, 32, orientation='horizontal')
length_value_lbl = gp.Label(generator_container, str(length_slider.value))

include_uppercase = gp.Checkbox(generator_container, 'Include Uppercase Letters')
include_digits = gp.Checkbox(generator_container, 'Include Numbers')
include_specials = gp.Checkbox(generator_container, 'Include Special Characters')

generate_button = gp.Button(generator_container, 'Generate Password', matrix_effect_and_generate)
copy_button = gp.Button(generator_container, 'Copy Password', copy_password)

generated_password_lbl = gp.Label(generator_container, '')
generated_password_box = gp.Textbox(generator_container, 30)
generated_password_box.readonly = True

generator_container.add(length_lbl, 2, 1)
generator_container.add(length_slider, 2, 2)
generator_container.add(length_value_lbl, 1, 2)
generator_container.add(include_uppercase, 3, 1)
generator_container.add(include_digits, 4, 1)
generator_container.add(include_specials, 5, 1)
generator_container.add(generate_button, 6, 1)
generator_container.add(copy_button, 6, 2)
generator_container.add(generated_password_lbl, 7, 1, colspan=2)
generator_container.add(generated_password_box, 8, 1, colspan=2)

app.add(generator_container, 9, 1, colspan=2)

# Events
length_slider.add_event_listener('change', update_length_value_label)

# Run app
app.run()

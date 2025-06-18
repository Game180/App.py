import gooeypie as gp
import string
import random

# Create the list of passwords
List_of_passwords = []

# Opening the text file and reading each line
with open('Pwdb_top-10000.txt', 'r') as file:
    for line in file:
        for word in line.split():
            print(word)
            List_of_passwords.append(word)

# Password check function
def check_password(event):
    user_password = password_box.text

    # Greeting check
    if user_password == "Josh Kenny":
        print("Hi Josh")
    else:
        print("Hi")

    # Length check
    if len(user_password) < 8:
        password_feedback.text = "Length Check: ❌ Too short"
    else:
        password_feedback.text = "Length Check: ✅ Passed"

    # Digit check
    if not any(char.isdigit() for char in user_password):
        password_feedback_2.text = "Digit Check: ❌ Password must contain at least one number"
    else:
        password_feedback_2.text = "Digit Check: ✅ Passed"

    # Special character check
    if any(char in string.punctuation for char in user_password):
        password_feedback_3.text = "Special Character Check: ✅ Passed"
    else:
        password_feedback_3.text = "Special Character Check: ❌ Must include a special character"

    # Common password check
    if user_password in List_of_passwords:
        password_feedback_4.text = "Common Password Check: ❌ Too common! Choose a stronger password."
    else:
        password_feedback_4.text = "Common Password Check: ✅ Passed"

# Password generator function
def generate_password(event):
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
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    generated_password_box.text = password
    generated_password_lbl.text = f"✅ Password generated! (Length: {length})"

# Create the app
app = gp.GooeyPieApp('Locked Away')
app.width = 600 

# Create widgets
name_lbl = gp.Label(app, 'Locked Away')
# passsword checker widgets
password_lbl = gp.Label(app, 'Enter Password:')
password_box = gp.Textbox(app, 20, 1)
password_feedback = gp.Label(app, "Length Check: ")
password_feedback_2 = gp.Label(app, "Digit Check: ")
password_feedback_3 = gp.Label(app, "Special Char Check: ")
password_feedback_4 = gp.Label(app, "Common Password Check: ")


submit_cont = gp.Container(app)
submit = gp.Button(submit_cont, 'Submit', check_password)
submit_cont.set_grid(1, 3)
submit_cont.add(submit, 1, 3)


# password generator widgets
generator_lbl = gp.Label(app, 'Password Generator')
length_lbl = gp.Label(app, 'Length:')
length_slider = gp.Slider(app, 4, 32, orientation='horizontal')
length_value_lbl = gp.Label(app, str(length_slider.value))

include_uppercase = gp.Checkbox(app, 'Include Uppercase Letters')
include_digits = gp.Checkbox(app, 'Include Numbers')
include_specials = gp.Checkbox(app, 'Include Special Characters')

generate_button = gp.Button(app, 'Generate Password', generate_password)

generated_password_lbl = gp.Label(app, '')
generated_password_box = gp.Textbox(app, 30)
generated_password_box.readonly = True

# Add widgets to app layout
app.set_grid(17, 2)
app.set_column_weights(0, 1)

app.add(name_lbl, 1, 1)

# password strength checker section
app.add(password_lbl, 2, 1)
app.add(password_box, 2, 2, fill=True)
app.add(submit_cont, 3, 2)
app.add(password_feedback, 4, 1, fill=True)
app.add(password_feedback_2, 5, 1, fill=True)
app.add(password_feedback_3, 6, 1, fill=True)
app.add(password_feedback_4, 7, 1, fill=True)

# password generator section
app.add(generator_lbl, 9, 1)
app.add(length_lbl, 10, 1)
app.add(length_slider, 10, 2)
app.add(length_value_lbl, 9, 2)
app.add(include_uppercase, 12, 1)
app.add(include_digits, 13, 1)
app.add(include_specials, 14, 1)
app.add(generate_button, 15, 1)
app.add(generated_password_lbl, 16, 1)
app.add(generated_password_box, 17, 1, colspan=2, fill=True)


def update_length_value_label(event):
    length_value_lbl.text = str(length_slider.value)

length_slider.add_event_listener('change', update_length_value_label)
# Run the app
app.run()
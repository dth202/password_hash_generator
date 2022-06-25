from flask import Flask, request
from processing import do_passwdsalt, do_validate_password

import os

app = Flask(__name__)

@app.route(os.environ.get('URI_BASE', '/'), methods=["GET", "POST"])


def adder_page():
    message = ""
    result_box_style = ""
    errors = ""
    result = ""
    password = ""
    password_confirmation = ""
    showpass = ""
    
    # Check password on POST
    if request.method == "POST":
        password = request.form["passwd1"]
        password_confirmation = request.form["passwd2"]
        
        # Make sure passwords are not empty and they match
        if not password:
            errors += "<li>Password is missing.</li>"
        if not password_confirmation:
            errors += "<li>Password Confirmation is missing.</li>"
        if password != password_confirmation:
            errors += "<li>Passwords do not match.</li>"
        # Verify Password requirments (if needed)
        if os.environ.get("VALIDATE_PASSWORD", False):
            errors += do_validate_password(password)
        # Show Password?
        # Display string if showpass is checked
        if 'showpass' in request.form and request.form["showpass"] == 'checked':
            message += "<p>Password entered: <font style='font-family:monospace'>{password}</font></p>".format(password=password)

        # Generate Hash if no errors, otherwise display errors
        if errors == "":
            try:
                result = do_passwdsalt(password)
                result_box_style = "display:inline-block;font-family:monospace;background:#eeeeee;border: 2px solid #777777;padding: 14px;border-radius: 4px;color:Black;"
                message += "<p>&#9989;&nbsp;Success!</p>"

            except:
                message += "&#10060;&nbsp;An error has occured: "
                errors += "<li>do_passwdsalt failed to generate hash</li>"

        else:
            message += "&#10060;&nbsp;An error has occured:"

    return '''
        <html>
            <body>
                <h1>Password Hash Generator</h1>
                <subtitle><i>created by Dallas Harris</i></subtitle>
                <p>This utility returns a SHA512 hash for the string
                you enter below. 
                <p> uses:
                <ul>
                  <li>Create a password hash for linux accounts where passwords are managed via puppet, salt, chef, etc</li>
                  <li>To create a password hash for your Systems administrator to add to a Linux server without providing your plain text password</li>
                  </ul>
                </p>
                <p>Note: A Strong Password Should contain:
                <ul>
                    <li>At least 8 characters in length</li>
                    <li>At least 1 number</li>
                    <li>At least 1 symbol</li>
                    <li>At least 1 uppercase letter</li>
                    <li>At least 1 lowercase letter</li>
                </ul></p>
                <form method="post" action=".">
                    <label for="passwd1">Password:</label><br>
                    <input id="passwd1" type="password" name="passwd1" value="{passwd1}" /><br>
                    <label for="passwd2">Confirm Password:</label><br>
                    <input id="passwd2" type="password" name="passwd2" value="{passwd2}" /><br>
                    <input type="checkbox" id="showpass" name="showpass" value="checked" {checked}>
                    <label for="showpass"> Show password with results</label><br>
                    <input type="submit" value="Submit" />
                </form>
                <div style="color:Black;">{message}</div>
                <div style="{result_box_style}">{result}</div>
                <div style="color:Black;"><ul>{errors}</ul></div>

            </body>
        </html>
    '''.format(message=message,result=result,result_box_style=result_box_style,errors=errors,passwd1=password,passwd2=password_confirmation,checked=showpass)


if __name__ == '__main__':
    app.run(debug=os.environ.get("DEBUG", False),host=os.environ.get('HOST', '0.0.0.0'),port=os.environ.get('PORT', 5000))



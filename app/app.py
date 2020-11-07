from flask import Flask, request
from processing import do_passwdsalt, validate_password

app = Flask(__name__)


@app.route("/genhash", methods=["GET", "POST"])


def adder_page():
    message = ""
    result_box_style = ""
    errors = ""
    result = ""
    password = ""
    password_confirmation = ""
    showpass = ""
    if request.method == "POST":
        password = request.form["passwd1"]
        password_confirmation = request.form["passwd2"]
        if 'showpass' in request.form:
            showpass = request.form["showpass"]

        # Make sure passwords are not empty and they match
        if not password:
            errors += "<li>Password is missing.</li>"
        if not password_confirmation:
            errors += "<li>Password Confirmation is missing.</li>"
        if password != password_confirmation:
            errors += "<li>Passwords do not match.</li>"

        # Verify Password requirments
        errors += do_validate_password(password)

        # Show Password?
        if showpass == 'checked':
            message += "<p>Password entered: <font style='font-family:monospace'>{password}</font></p>".format(password=password)

        # Gen Hash if no errors, otherwise display errors
        if errors == "":
            try:
                result = do_passwdsalt(password)
                result_box_style = "display:inline-block;font-family:monospace;background:#eeeeee;border: 2px solid #777777;padding: 14px;border-radius: 4px;color:Black;"
                message += "<p>&#9989;&nbsp;Success!</p><a href='mailto:campusahosting@utah.gov?subject=Hash%20Generated&body=Username%3A%20%5BUsername%5D%0D%0A{result}%0D%0A'>Please click here to send generated hash to Campus A Hosting</a>".format(result=result)

            except:
                message += "&#10060;&nbsp;An error has occured: "
                errors += "<li>do_passwdsalt failed to generate hash</li>"

        else:
            message += "&#10060;&nbsp;An error has occured:"

    return '''
        <html>
            <body>
                <h1>Password Hash Generator</h1>
                <subtitle><i>Provided by Campus A Hosting</i></subtitle>
                <p>This utility creates a hash for the password
                you enter below. This does not automatically update your
                password so make sure to send the hash to hosting!</p>
                <p>Note: Password Requirments:
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
    app.run(debug=True,host='0.0.0.0')



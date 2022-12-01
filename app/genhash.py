from flask import Flask, request
from waitress import serve
from processing import get_requirements, do_passwdsalt, do_validate_password

import os

DEBUG = os.environ.get("DEBUG", False)
URI_BASE = os.environ.get('URI_BASE', '/')
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = os.environ.get('PORT', 5000)

app = Flask(__name__)

@app.route(URI_BASE, methods=["GET", "POST"])

def adder_page():
    message = ""
    result_box_style = ""
    errors = ""
    result = ""
    password = ""
    password_confirmation = ""
    showpass = ""

    # Populate Requirements List
    requirements = get_requirements()

    
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
                <h1><a href="{REPO_URL}" target="_blank" >{TITLE}</a></h1>
                <subtitle>{SUBTITLE}</subtitle>
                <p>{BANNER}</p> 
                
                <!-- Requirements Box -->
                <div class="requirements">
                <p>Password Requirements:
                <ul>{requirements}</ul></p>
                </div> 

                <!-- Password Form -->
                <form method="post" action=".">
                    <label for="passwd1">Password:</label><br>
                    <input id="passwd1" type="password" name="passwd1" value="{passwd1}" /><br>
                    <label for="passwd2">Confirm Password:</label><br>
                    <input id="passwd2" type="password" name="passwd2" value="{passwd2}" /><br>
                    <input type="checkbox" id="showpass" name="showpass" value="checked" {checked}>
                    <label for="showpass"> Show password with results</label><br>
                    <input type="submit" value="Submit" />
                </form>

                <!-- Feedback, Errors, or Result -->
                <div style="color:Black;">{message}</div>
                <div style="{result_box_style}">{result}</div>
                <div style="color:Black;"><ul>{errors}</ul></div>
                
            </body>
        </html>
    '''.format(
            TITLE=os.environ['TITLE_STR'],
            SUBTITLE=os.environ['SUBTITLE_STR'],
            BANNER=os.environ['BANNER'],
            REPO_URL=os.environ['PROJECT_REPO'],
            requirements=requirements,
            message=message,
            result=result,
            result_box_style=result_box_style,
            errors=errors,
            passwd1=password,
            passwd2=password_confirmation,
            checked=showpass)


#if __name__ == '__main__':
#    app.run(debug=DEBUG,host=HOST,port=PORT)

serve(app, host=HOST, port=PORT)

from flask import request
from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
# https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            #return redirect(url_for('home'))
            print("YES")
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1900, use_reloader=False, threaded=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = firebaseConfig = {
  "apiKey": "AIzaSyA1p75Fvh8Yo45sDSkk-JYE9ixwUVSNCVc",
  "authDomain": "fir-e5575.firebaseapp.com",
  "projectId": "fir-e5575",
  "storageBucket": "fir-e5575.appspot.com",
  "messagingSenderId": "865543612227",
  "appId": "1:865543612227:web:4bfd59b7b8641d8667f1f6",
  "measurementId": "G-B2VWN8FX6V",
  "databaseURL": "https://fir-e5575-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"

    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name":request.form['full_name'], "password":request.form['password'], "username": request.form['username'], "bio":request.form['bio']}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        Title = request.form['title']
        Text = request.form['text']
        try:
            tweet = {"Title":request.form['title'], "Text":request.form['text'], "uid":'user'}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "Authentication failed"

    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)
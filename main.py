from flask import Flask, redirect, render_template

app = Flask(__name__)

# Render the homepage with buttons
@app.route('/')
def index():
    return render_template('index.html')

# Redirect to post_app
@app.route('/redirect-7000')
def redirect_7000():
    return redirect('http://post-app:7000')

# Redirect to music_app
@app.route('/redirect-8000')
def redirect_8000():
    return redirect('http://music-app:8000')

# Redirect to documents_app
@app.route('/redirect-9000')
def redirect_9000():
    return redirect('http://documents-app:9000')

if __name__ == '__main__':
    # If running with Gunicorn, you can start the app using Gunicorn like this:
    # gunicorn main:app -b 0.0.0.0:8080
    app.run(port=8080)

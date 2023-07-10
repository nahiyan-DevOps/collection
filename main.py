from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

# Render the homepage with buttons
@app.route('/')
def index():
    return render_template('index.html')

# Redirect to port 7000
@app.route('/redirect-7000')
def redirect_7000():
    return redirect('http://localhost:7000')

# Redirect to port 8000
@app.route('/redirect-8000')
def redirect_8000():
    return redirect('http://localhost:8000')

# Redirect to port 9000
@app.route('/redirect-9000')
def redirect_9000():
    return redirect('http://localhost:9000')

if __name__ == '__main__':
    app.run(port=8080)

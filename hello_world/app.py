from flask import Flask
app = Flask(__name__)

@app.route('/') #home or root of the site
def index():
    return '<html><head><title>Hello, World!</title></head><body><h1>Hello, World!</h1><p>Welcome to the home page. Developed by Horacio Duran.</p></body></html>' #what to show when the user visits the home page

@app.route('/about') #info page about the site
def about():
    return '<html><head><title>About</title></head><body><h1>About</h1><p>This is the about page. Developed by Horacio Duran.</p></body></html>' #what to show when the user visits the about page

if __name__ == '__main__':
    app.run(debug=True)
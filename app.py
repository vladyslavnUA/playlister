from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """return homepage."""
    #return 'Hellow, world!'
    return render_template('home.html', msg='flask is cool!!')


#if __name__ == '__main__':
#    app.run(debug=True)

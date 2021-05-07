#import Flask Framework
from flask import *

#Initialize Flask app
app = Flask(__name__)

#Root Route
@app.route('/')
def home():
    return render_template('index.html')

#Run Flask app when the python file is ran
if __name__ == "__main__":
    app.run(debug=True)
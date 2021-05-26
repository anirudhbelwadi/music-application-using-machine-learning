#import Flask Framework
from flask import *
from detect_cnn import *
from datetime import datetime
import sqlite3
import tensorflow.keras as keras

#Initialize Flask app
app = Flask(__name__)

#Root Route


@app.route('/')
def home():
    return render_template('index.html')

#Team Route


@app.route('/team')
def team():
    return render_template('team.html')

#Contact Route
@app.route('/contact', methods=['POST','GET'])
def contact():
    if 'message' in request.args:
        message = request.args.get('message')
        return render_template('contact.html', message=message)
    return render_template('contact.html')


@app.route('/submitcontact', methods=['POST'])
def submit_contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        #Make a connection
        myconnection = sqlite3.connect('soundlogy_database.db')
        #Make a cursor which will perform certain actions
        mycursor = myconnection.cursor()
        #Execute Given action
        mycursor.execute("INSERT INTO contact VALUES (:timestamp,:name,:email,:message)", {
                         'timestamp': dt_string, 'name': name, 'email': email, 'message': message})
        #Take acknowledgement
        myconnection.commit()
        #Close Connection
        myconnection.close()
        return redirect(url_for('contact',message="Thank you for submitting your query! We will get back to you soon."))


@app.route('/detect', methods=['POST'])
def detect():
    name = request.form['name']
    #File Input
    user_input = request.files['song']
    #stuff you do with the file goes here
    f_name = 'test/input/'+user_input.filename
    uploadedIMG = os.path.join(f_name)
    user_input.save(uploadedIMG)
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    genre = detect_genre_cnn()
    #Make a connection
    myconnection = sqlite3.connect('soundlogy_database.db')
    #Make a cursor which will perform certain actions
    mycursor = myconnection.cursor()
    #Execute Given action
    mycursor.execute("INSERT INTO detection VALUES (:timestamp,:name,:filename,:genre)", {
                    'timestamp': dt_string, 'name': name, 'filename': user_input.filename, 'genre': genre})
    #Take acknowledgement
    myconnection.commit()
    #Close Connection
    myconnection.close()
    return render_template('detect.html', genre=genre)


@app.route('/summary')
def summary():
    cnn_model = keras.models.load_model('saved_model/my_CNN_model')
    rnn_model = keras.models.load_model('saved_model/my_RNN_model')
    mlp_model = keras.models.load_model('saved_model/my_MLP_model')
    print("\n\nCNN MODEL SUMMARY")
    cnn_model.summary()
    print("RNN MODEL SUMMARY")
    rnn_model.summary()
    print("MLP MODEL SUMMARY")
    mlp_model.summary()
    return render_template('summary.html')


#Run Flask app when the python file is ran
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
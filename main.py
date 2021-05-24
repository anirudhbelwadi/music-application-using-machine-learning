#import Flask Framework
from flask import *
from detect_cnn import *


#Initialize Flask app
app = Flask(__name__)

#Root Route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    #File Input
    user_input = request.files['song']
    #stuff you do with the file goes here
    f_name = 'test/input/'+user_input.filename
    uploadedIMG = os.path.join(f_name)
    user_input.save(uploadedIMG)
    
    genre = detect_genre_cnn()
    print(genre)
    return genre

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
    app.run(debug=True)

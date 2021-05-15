#import Flask Framework
from flask import *
from cnn import *

#Initialize Flask app
app = Flask(__name__)

#Root Route


@app.route('/')
def home():
    return render_template('index.html')

#Genre Detection route
@app.route('/detectgenre', methods=['POST'])
def detect():
    # get train, validation, test splits
    X_train, X_validation, X_test, y_train, y_validation, y_test = prepare_datasets(
        0.25, 0.2, DATA_PATH)

    # create network
    input_shape = (X_train.shape[1], X_train.shape[2], 1)
    model = build_model(input_shape)

    # compile model
    optimiser = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimiser,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # train model
    history = model.fit(X_train, y_train, validation_data=(
        X_validation, y_validation), batch_size=32, epochs=30)

    # plot accuracy/error for training and validation
    plot_history(history)

    # evaluate model on test set
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
    print('\nTest accuracy:', test_acc)
    
    #File Input
    user_input = request.files['song']
    #stuff you do with the file goes here
    f_name = 'uploads/final/'+user_input.filename
    uploadedIMG = os.path.join(f_name)
    user_input.save(uploadedIMG)
    
    save_mfcc(DATASET_PATH, JSON_PATH, num_segments=10)
    # pick a sample to predict from the test set
    tX_train, tX_validation, tX_test, ty_train, ty_validation, ty_test = prepare_datasets(0.25, 0.2, JSON_PATH)
    X_to_predict = tX_test[0]
    y_to_predict = ty_test[0]

    # predict sample
    a, b = predict(model, X_to_predict, y_to_predict)
    print("\na=", a, "\nb=", b)
    f = open('upload.json', 'r+')
    f.truncate(0)
    f.close()
    os.chdir("./uploads/final/")
    for file in glob.glob("*.au"):
        os.remove(file)
    os.chdir("../../")
    if b==1:
        return "Blues"
    elif b==2:
        return "Classical"
    elif b==3:
        return "Country"
    elif b==4:
        return "Disco"
    elif b==5:
        return "HipHop"
    elif b==6:
        return "Jazz"
    elif b==7:
        return "Metal"
    elif b==8:
        return "Pop"
    elif b==9:
        return "Reggae"
    elif b==10:
        return "Rock"

#Run Flask app when the python file is ran
if __name__ == "__main__":
    app.run(debug=True)

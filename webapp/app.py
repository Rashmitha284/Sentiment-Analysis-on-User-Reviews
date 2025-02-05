from flask import Flask,render_template,request
import joblib

app = Flask(__name__)

with open('models/rf_bow.pkl', 'rb') as file:
    loaded_model = joblib.load(file)

with open('models/vectorizer.pkl', 'rb') as file:
    loaded_vectorizer = joblib.load(file)

@app.route('/')
def home():
    clear_text = request.args.get('clear_text')
    return render_template("home.html",clear_text=clear_text)

@app.route('/predict',methods = ['GET','POST'])
def predict():
    user_review = request.form.get("input_text")

    if not user_review:
        return render_template("predict.html", sentiment="No text provided")
    text_vector = loaded_vectorizer.transform([user_review])
    sentiment = loaded_model.predict(text_vector)
    
    return render_template("predict.html", user_review=user_review,sentiment=sentiment[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
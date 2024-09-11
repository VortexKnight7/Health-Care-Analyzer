import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
dicease = pickle.load(open('dicease.pkl','rb'))
insurance_p = pickle.load(open('insurance_cost.pkl','rb'))
breast_p = pickle.load(open('breast_p.pkl','rb'))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

@app.route('/heart_report', methods=['GET','POST'])
def Heart_Report():
    return render_template('Heart_Report.html')

@app.route('/breast_report', methods=['GET','POST'])
def Breast_Report():
    return render_template('Breast_Report.html')

@app.route('/diabetes_report', methods=['GET','POST'])
def Diabetes_Report():
    return render_template('Diabetes_Report.html')

@app.route('/insurance_report', methods=['GET','POST'])
def Insurance_Report():
    return render_template('insurance_Report.html')

@app.route('/', methods=['GET','POST'])
def landing():
    return render_template('landing.html')

@app.route('/heart-main', methods=['GET','POST'])
def heart_main():
    return render_template('prac_heart.html')

@app.route('/diabetes-main', methods=['GET','POST'])
def diabetes_main():
    return render_template('prac_diabetes.html')

@app.route('/cancer-main', methods=['GET','POST'])
def cancer_main():
    return render_template('prac_cancer.html')

@app.route('/insurance-main', methods=['GET','POST'])
def insurance_main():
    return render_template('healthcare.html')

@app.route('/heart-form', methods=['GET','POST'])
def heart_form():
    return render_template('form-heart.html')

@app.route('/cancer-form', methods=['GET','POST'])
def cancer_form():
    return render_template('form_cancer.html')

@app.route('/diabetes-form', methods=['GET','POST'])
def diabetes_form():
    return render_template('form_diabetes.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    if prediction == 1:
        output='Positive'
    else:
        output = 'Negative'
    return render_template('form_diabetes.html',prediction_text = f' {output}')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method=='POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        data = Data(name=name, phone=phone, address=address, email=email)
        db.session.add(data)
        db.session.commit()
        
    allData = Data.query.all() 
    return render_template('Contact.html',allData=allData)

@app.route('/heart',methods=['GET','POST'])
def heart():
    float_features = [float(x) for x in request.form.values()]
    mean_value = [0,49.58494573,0,9.00308862,0,0,0,0,236.7215855,132.3524068,82.8934639,25.80200758,75.87892377,81.96675325]
    std_dev_value = [1,8.572159925,1,11.92009359,1,1,1,1,44.59033432,22.03809664,11.9108496,4.080111062,12.02659635,23.95999819]
    reverse_scaled_features = []
    for i in range(len(float_features)):
        reverse_scaled_features.append((float_features[i] - mean_value[i])/std_dev_value[i])
    features = [np.array(reverse_scaled_features)]
    prediction = dicease.predict(features)
    if prediction == 1:
        vla='Positive'
    else:
        vla = 'Negative'
    return render_template('form-heart.html',Heart_text = f' {vla}')

@app.route('/breast',methods=['GET','POST'])
def breast():
    float_features = [float(x) for x in request.form.values()]
    print(float_features)
    features = [np.array(float_features)]
    print(features)
    prediction = breast_p.predict(features)
    print(prediction)
    if prediction == 4:
        out='Positive'
    else:
        out = 'Negative'
    return render_template('form_cancer.html',breast_text = f' {out}')

@app.route('/insurance',methods=['GET','POST'])
def insurance():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = insurance_p.predict(features)
    print(float_features)
    print(features)
    print(prediction)
    return render_template('healthcare.html',insurance_text = f' {prediction}')

if __name__ == '__main__':
    app.run(debug=True)
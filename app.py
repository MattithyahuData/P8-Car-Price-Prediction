# Importing project dependencies 

# Model importing
import pickle

# Webapp creation and model use template rendering and requests for HMTL interaction
from flask import Flask, request, render_template 

# Data handling
import pandas as pd
import numpy as np

# Creating flask app / Initiating app
app = Flask(__name__)

# Load pickle model
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

# Define the home page
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

# route() decorator to tell Flask what URL should trigger our function.
@app.route("/predict", methods=['POST'])

# Predict method
def predict():
    # Fuel_Type_Diesel=0

    # Inputs from deployment inputs 
    if request.method == 'POST':

        # Converting web inputs to correct data types 
        # INPUTS # 
        # Year = int(request.form['Year'])
        # Present_Price=float(request.form['Present_Price'])
        # Kms_Driven=int(request.form['Kms_Driven'])
        # Kms_Driven2=int(Kms_Driven)
        # Owner=int(request.form['Owner'])
        # Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        # Seller_Type_Individual=request.form['Seller_Type_Individual']
        # Transmission_Mannual=request.form['Transmission_Mannual']

        # Kms Driven input # 1
        Kms_Driven=int(request.form['Kms_Driven'])


        # Owners input # 2
        Owner=int(request.form['Owner'])


        # Sale price input # 3
        Present_Price=float(request.form['Present_Price'])


        # Year input # 4
        Year = int(request.form['Year'])
        # Subtracting input year from current year 
        Year=2021-Year


        # Fuel type input # 5 & 6
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        # Converting categorical values into numbers before feeding into model 
        if(Fuel_Type_Petrol=='Petrol'):
            # If Fuel type is petrol then petrol == 1 else 0 
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0

        # Converting categorical values into numbers before feeding into model       
        elif(Fuel_Type_Petrol=='Diesel'):
            # If Fuel type is diesel then diesel == 1 else 0 
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1

        # else if Fuel type not Diesel or petrol assign to 0 therefore == to CNG
        else:
            # If Fuel type if not petrol or diesel then petrol == 0 and diesel == 0 meaning CNG == 1
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        

        # Seller type input # 7
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        # If selection is indivual
        if(Seller_Type_Individual=='Individual'):
            # Then set field == 1
            Seller_Type_Individual=1
        # Else if selection not equal to individual then
        else:
            # Set field to 0 
            Seller_Type_Individual=0	


        # Transmission type input # 8
        Transmission_Mannual=request.form['Transmission_Mannual']
        # If selection is manual
        if(Transmission_Mannual=='Mannual'):
            # Then set field == 1
            Transmission_Mannual=1
         # Else if selection not equal to manual then  
        else:
            # Set field to 0 
            Transmission_Mannual=0
            

        # Feeding input values into model 
        prediction=model.predict([[Kms_Driven,Owner,Present_Price,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])

        # Rouding prediction to 2 d.p
        output=round(prediction[0],2)
        
        # Returning car value prediction 
        return render_template('index.html',prediction_text=f"Estimated car value: £{output}")
    
    # Else request.method != 'POST' 
    else:
        # Returning to index.html if no input
        return render_template('index.html')

# Only allowing file to run from this file 
if __name__=="__main__":
    app.run(debug=True)


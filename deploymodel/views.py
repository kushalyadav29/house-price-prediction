from django.shortcuts import render
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_directory, "..", "Arp.csv")




def input(request):
    json_data = open('columns.json').read()   
    data1 = json.loads(json_data)
    data3 = data1['data_columns']
    locality = data3[3:-6]
    property_type = data3[-6:]
    return render(request,'main.html',{'locality':locality,'type':property_type})

def result(request):
    if request.method == 'POST':
        bedroom = request.POST.get('bhk')
        area = request.POST.get('area')
        bathroom = request.POST.get('bathroom')
        locality = request.POST.get('dropdown').capitalize()
        Property_type = request.POST.get('dropdown1').capitalize()
        data = predict_price(bedroom,area,bathroom,locality,Property_type)
        return render(request,'result.html',{'Data':data})
    
def predict_price(bedroom,area,bathroom,locality,property_type): 
    df = pd.read_csv(file_path)
    X = df.drop('price',axis='columns')
    y = df.price
    x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=10)
    lr_model = LinearRegression()
    lr_model.fit(x_train,y_train)   
    loc_index = np.where(X.columns==locality)[0]
    prop_index =  np.where(X.columns==property_type)[0]
    x = np.zeros(len(X.columns))
    x[0] = bedroom
    x[1] = bathroom
    x[2] = area
    if loc_index >= 0:
        x[loc_index] = 1
    if prop_index>=0:
        x[prop_index] = 1

    prediction = round(lr_model.predict([x])[0])
    if prediction <= 0 or prediction >= 1000000:
        return "No such property available in the particular area"
    else:
        return "Rs. " + str(prediction)

# predict_price(3,600,3,'Paldi','Apartment')
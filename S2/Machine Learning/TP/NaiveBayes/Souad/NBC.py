from sklearn import preprocessing
import numpy as np
from sklearn.naive_bayes import GaussianNB

data = {
    'Outlook':     ['Sunny','Sunny','Overcast','Rainy','Rainy','Rainy','Overcast',
                    'Sunny','Sunny','Rainy','Sunny','Overcast','Overcast','Rainy'],
    'Temperature': ['Hot','Hot','Hot','Mild','Cool','Cool','Cool',
                    'Mild','Cool','Mild','Mild','Mild','Hot','Mild'],
    'Play':        ['No','No','Yes','Yes','Yes','No','Yes',
                    'No','Yes','Yes','Yes','Yes','No','No']
}

le = preprocessing.LabelEncoder()

weather_encoded = le.fit_transform(data['Outlook'])
print(weather_encoded)

temp_encoded = le.fit_transform(data['Temperature'])
print(temp_encoded)

label = le.fit_transform(data['Play'])
print(label)

features = np.array(list(zip(weather_encoded, temp_encoded)))
print(features)

model = GaussianNB()
model.fit(features, label)

predicted = model.predict([[0, 2]])
print("Predicted Value (No=0, Yes=1):", predicted)
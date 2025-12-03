from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

iris = load_iris()

x = iris.data   #features
y = iris.target     #lables


#Split into train and test
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)


clf = SVC()

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

print(classification_report(y_test, y_pred))








"""
#importer le dataset Iris
from sklearn.datasets import load_iris
iris = load_iris() # chargement du jeu de données de fleurs d’iris
X = iris.data # récupérer les données d’entrée dans X
y = iris.target # récupérer les données de sortie dans y
feature_names = iris.feature_names # récupérer la liste des caractéristiques des fleurs
target_names = iris.target_names # récupérer la liste des résultats désirés
print("Feature names:", feature_names)
# afficheFeature names: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width(cm)']
print("Target names:", target_names)
# afficheTarget names: ['setosa' 'versicolor' 'virginica']
"""
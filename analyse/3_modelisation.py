import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, accuracy_score, f1_score
import pickle

connection = sqlite3.connect("olist.db")

df = pd.read_sql_query("SELECT * FROM TrainingDataset",connection)

connection.close()

y = df['score']
X = df[["produit_recu"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

model = LogisticRegression()

model.fit(X_train,y_train)


recall_train = round(recall_score(y_train, model.predict(X_train)),4)
acc_train = round(accuracy_score(y_train, model.predict(X_train)),4)
f1_train = round(f1_score(y_train, model.predict(X_train)),4)

print(f"Pour le jeu d'entrainement: \n le recall est de {recall_train}, \n l'accuracy de {acc_train} \n le f1 score de {f1_train}")

recall_test = round(recall_score(y_test, model.predict(X_test)),4)
acc_test = round(accuracy_score(y_test, model.predict(X_test)),4)
f1_test = round(f1_score(y_test, model.predict(X_test)),4)

print(f"Pour le jeu de test: \n le recall est de {recall_test}, \n l'accuracy de {acc_test} \n le f1 score de {f1_test}")

model_name = 'log_produitrecu'
print(f"['{model_name}', {recall_train}, {acc_train}, {f1_train}, {recall_test}, {acc_test}, {f1_test} ],")

# Save the model to a file using pickle
with open('best_reg_lin_produit_recu.pkl', 'wb') as file:
    pickle.dump(model, file)
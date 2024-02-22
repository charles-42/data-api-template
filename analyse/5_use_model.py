import pickle
import pandas as pd

with open('best_reg_log_produit_recu.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

produit_recu = input("Avez reçu votre produit?")

if produit_recu == "oui":
    produit_recu = 1
else:
    produit_recu = 0

data = {'produit_recu':[produit_recu]}
df_to_predict = pd.DataFrame(data)

prediction = loaded_model.predict(df_to_predict)

if prediction[0]==1:
    print("Alors vous devez être content")
else:
    print("Je suppose que vous êtes frustré")


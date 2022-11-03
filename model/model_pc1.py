import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle

data = pd.read_csv(config.pc1_local_data_path, sep=';', decimal=",", index_col=False)

X = data[config.pc1_features]

Y = data[config.pc2_target].values.ravel()

print(X)
print(Y)
input()
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=16)

logreg = LogisticRegression(random_state=16, max_iter=1000)

logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

# dump the model into a file
with open("exported_models/pc1_model.bin", 'wb') as f_out:
    pickle.dump(logreg, f_out)  # write final_model in .bin file
    f_out.close()  # close the file

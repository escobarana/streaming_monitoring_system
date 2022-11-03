import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

data = pd.read_csv(config.rasb_local_data_path, sep=';', decimal=",",index_col=False)


X = data[config.rasb_features]
print(X.head)
#Cleaning target variable


data[config.rasb_target] = data[config.rasb_target].apply(lambda x: x=='0x0')

Y = data[config.rasb_target].values.ravel()
print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=16)

logreg = LogisticRegression(random_state=16,max_iter=1000 )

logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

        
##dump the model into a file
with open("exported_models/rassb_model.bin", 'wb') as f_out:
    pickle.dump(logreg, f_out) # write final_model in .bin file
    f_out.close()  # close the file

"""


class_names=[0,1] # name  of classes
fig, ax = plt.subplots()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')

plt.show()


"""
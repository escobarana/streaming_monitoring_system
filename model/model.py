import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib as plt
import numpy as np
import pickle
import seaborn as sns
import os


class PCTrainer:
    def __init__(self,
                 device_name: str = "pc1",
                 output_folder: str = config.output_folder,
                 data_source: str = config.pc1_local_data_path,
                 features: list = config.pc1_features,
                 target: str = config.pc_target
                 ):
        """
            Creates an instance of our PCTrainer model creator
        :param output_folder : Folder where the models are going to be stored
        :param data_source: training data  csv file produced either locally or retrieved from dynamo db
        :param features: independent variable to train the model
        :param target: dependant variable
        """
        self.device_name = device_name
        self.output_folder = output_folder
        self.data = pd.read_csv(data_source, sep=';', decimal=",", index_col=False)
        self.features = features
        self.target = target
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []

    def split_data(self):
        """
            Train and export the model
        :return: The model
        """
        X = self.data[self.features]
        Y = self.data[self.target].values.ravel()

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, Y, test_size=0.25, random_state=16)

        model = LogisticRegression(random_state=16, max_iter=1000)

        model.fit(self.X_train, self.y_train)

        return model

    def create_confusion_matrix(self, model):
        """
            This function creates a confusion matrix
        :param model: model to apply on data
        :return: None
        """
        y_pred = model.predict(self.X_test)

        cnf_matrix = metrics.confusion_matrix(self.y_test, y_pred)
        return cnf_matrix

    def plot_confusion(self, matrix):
        """
            This function plots the confusion matrix
        :param matrix: confusion matrix
        :return: plot of the graph
        """
        class_names = [0, 1]
        fig, ax = plt.subplots()
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names)
        plt.yticks(tick_marks, class_names)
        sns.heatmap(pd.DataFrame(matrix), annot=True, cmap="YlGnBu", fmt='g')
        ax.xaxis.set_label_position("top")
        plt.tight_layout()
        plt.title('Confusion matrix', y=1.1)
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')

        plt.show()

    def export_model(self, model: LogisticRegression):
        """
            This function exports the model to a .bin file
        :param model: LogisticRegression Class
        :return: None
        """
        with open(os.path.join(self.output_folder, self.device_name), 'wb') as f_out:
            pickle.dump(model, f_out)
            f_out.close()

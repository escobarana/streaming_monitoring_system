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
import logging
import boto3
from botocore.exceptions import ClientError


class PCTrainer:
    def __init__(self,
                 device_name: str,
                 output_folder: str,
                 data_source: str,
                 features: list,
                 target: str
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

    def train_model(self):
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

    def export_model_local(self, model: LogisticRegression):
        """
            This function exports the model to a .bin file in a local folder
        :param model: LogisticRegression Class
        :return: None
        """
        with open(os.path.join(self.output_folder, f'{self.device_name}_model.bin'), 'wb') as f_out:
            pickle.dump(model, f_out)

    def export_model_s3(self, file_name: str, bucket: str, object_name: str = None):
        """
            This function uploads a .bin file (ML Model) to AWS S3 bucket to the corresponding object
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True


if __name__ == '__main__':

    # --- UPDATE MODELS ON S3 BUCKET --- #

    # PC1
    pc1_trainer = PCTrainer(device_name="pc1",
                            output_folder=config.output_folder,
                            data_source=config.pc1_local_data_path,
                            features=config.pc1_features,
                            target=config.pc_target)

    model_pc1 = pc1_trainer.train_model()
    pc1_trainer.export_model_local(model_pc1)
    file_name_pc1 = f'{config.output_folder}/pc1_model.bin'
    pc1_trainer.export_model_s3(file_name_pc1, "dstimlmodels", "pc1_model.bin")

    # PC2
    pc2_trainer = PCTrainer(device_name="pc2",
                            output_folder=config.output_folder,
                            data_source=config.pc2_local_data_path,
                            features=config.pc2_features,
                            target=config.pc_target)

    model_pc2 = pc2_trainer.train_model()
    pc2_trainer.export_model_local(model_pc2)
    file_name_pc2 = f'{config.output_folder}/pc2_model.bin'
    pc2_trainer.export_model_s3(file_name_pc2, "dstimlmodels", "pc2_model.bin")

    # RASPBERRY
    raspb_trainer = PCTrainer(device_name="raspb",
                              output_folder=config.output_folder,
                              data_source=config.rasb_local_data_path,
                              features=config.rasb_features,
                              target=config.rasb_target)

    model_rasp = raspb_trainer.train_model()
    raspb_trainer.export_model_local(model_rasp)
    file_name_raspb = f'{config.output_folder}/raspb_model.bin'
    pc1_trainer.export_model_s3(file_name_raspb, "dstimlmodels", "raspb_model.bin")

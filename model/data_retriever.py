
from django.urls import conf
import config
import pandas as pd

class DATA:

    def __init__(self,environment="local") :
        self.environment = environment
        self.local_data_path = config.local_data_path
    
    #retireve data from data base
    def get_data_from_kafka(self):
        pass


    #add the data where the "needs intervention is 1"
    def augment_data(self):
        pass

    #get data from local csv
    def get_local_data(self):
        try:
            data_frame = pd.read_csv(config.local_data_path)
            return data_frame
        except Exception as error:
            print('Error wile reading local data '+str(error))
            return False
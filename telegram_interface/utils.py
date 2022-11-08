

import config
import requests
from boto3.dynamodb.conditions import Attr
from dynamodb import dynamodb
import pickle



class PREDICT:

    def __init__(self,url_pc1=config.link_model_pc1,url_pc2=config.link_model_pc2,url_rasb=config.link_model_rassberry):
        self.pc1_model_url  = url_pc1
        self.pc2_model_url  = url_pc2
        self.rasb_model_url = url_rasb
    
    def download_model(self,url):
        try:
            response = requests.get(url).content
            return response
        except:
            return False

    def predict_output(self, device):
        url=""
        data_input = []
        if device=="pc1":
            url = self.pc1_model_url
        elif device=="pc2":
            url = self.pc2_model_url
        elif device=="raspberry":
            url = self.rasb_model_url
            val = self.get_data_dynamodb(device)
            for i,elt in enumerate(config.rasb_features):
                for data in val:
                    if data==elt:
                        print(i,data, val[data])
                        data_input.append(float(val[data]))

        model_raw = self.download_model(url)       
        model= pickle.loads(model_raw)

        data = data_input
        
        prediction = model.predict([data_input])
        return data, prediction


    def get_data_dynamodb(self,device):
   
        query_response = dynamodb.Table('sensors_data').scan(FilterExpression=Attr("device").eq(device),
                                                            IndexName="device-loading_datetime-index")
        print(query_response["Items"][-1])
        return query_response["Items"][-1]



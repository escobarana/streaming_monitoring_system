from sklearn.model_selection import train_test_split
import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



class MODEL:

    def __init__(self,columns,data):
        self.columns = columns
        self.data = data

    
    def develop_model(self):
        pass
        
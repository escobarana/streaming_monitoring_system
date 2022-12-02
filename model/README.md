# 🤖 ML Model

## Run locally

### Prerequisites

Install requirements from root folder

````shell
pip install -r requirements.txt
````

### Execute

````shell
cd model
````

Save `.csv` files

````shell
python data_retriever.py
````

Since versioning is enabled on the S3 bucket objects, we can update the versions by executing:

````shell
python model.py
````


##  🏋️‍♂️ Model Training

### 📈Model type

> We want to predict if the machine is going to need a technical intervention. Thus, we need classification algorithm. 
We opted for logistic regression.


### 📈 Data source

| Source       | Description                                                          |
|--------------|----------------------------------------------------------------------|
| Local data   | Collected from computer and store in csv file                        |
| Data from DB | Retrieved from the database after and after being comsumed by kafka  |

### 📈Data augmentation

> Our target variable has 2 values either 0 or 1. 
With 1 being `stressed` and 0 being `not stressed`. 
Since the computer will not be able to send data when it is down, the rows of 0 are invented by us. 
In fact we took edge values and generated around them.


### 📈 Model training

> The training of models is triggered manually by the user. The process is simple and straight forward.
The result is stored in bin file via the pickle model.


## Model deployment and prediction

### 🪣 S3 bucket

> This is where we store our trained models.
We enable versioning to replace the models whenever needed while keeping  track of previous version


### 💼 Use case

> The model is called by the kafka consumer whenever new stream of data comes in.
The result of prediction is sent to the user via telegram alert

## Packages 

- `Pandas`
- `Sickit-learn`
- `Pickle`


Test of the alerting message sent by the Telegram Bot after making the prediction with the model, and correcting the 
prediction by the user so the model keeps learning:

![Alert message PC1 + correction of prediction](../image/pc1_alert_with_correction.png "Alert PC1")

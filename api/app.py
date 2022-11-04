from flask import Flask, request, render_template
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from werkzeug.serving import run_simple
from kafka.cpu_consumer import launch_consumer_and_predicter
from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from werkzeug.serving import run_simple
from helpers.config_mongodb import get_data_from_mongodb
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

# Blueprint definition for monitoring purposes
# MAIN = Blueprint("main", __name__)

app = Flask(__name__)

# metrics = PrometheusMetrics(app, group_by='endpoint')  # Prometheus monitoring

api = Api(app,
          version='1.0',
          title='Monitoring Device Prediction REST API',
          description='Documentation of the Monitoring Device Prediction REST API',
          doc='/doc/'
          )

ns = api.namespace('predictions', description='operations')

prediction = api.model('Prediction', {
    'device': fields.String(required=True, description="The device name of the prediction."),
    'example': fields.String(required=True, description="This is another example.")
})


@app.route('/home', methods=["GET", "POST"])
def home():
    return render_template('index.html', context='templates')


@ns.doc('get_results')
@app.route('/results', methods=['GET'])
def output_results():
    return render_template('output.html', context='templates')


@ns.doc('post_prediction')
# @ns.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    # print(" I am in predict ")
    # print("Request.method:", request.method)
    # print("Request.TYPE", type(request))

    # if request.method == 'POST':
    launch_consumer_and_predicter()
    # return outputResults(records_dict['Clock CPU Core #1'],
    #                      records_dict['Temperature CPU Package'],
    #                      records_dict['Load CPU Total'],
    #                      records_dict['Power CPU Package'],
    #                      records_dict['Temperature GPU Core'],
    #                      records_dict['Load GPU Core'],
    #                      resultPredicted)


class AppDAO(object):
    def __init__(self):
        if len(get_data_from_mongodb()) > 0:  # The list is not empty
            self.pred_data = get_data_from_mongodb()
        else:
            self.pred_data = []

    def list(self) -> list:
        return self.pred_data

    def get(self, device: str) -> list:
        predictions = []
        for pred in self.pred_data:
            if pred['device'] == device:
                predictions.append(pred)
        if len(predictions) > 0:
            return predictions
        logging.error("Prediction for {} doesn't exist".format(device))
        api.abort(404, "Prediction for {} doesn't exist".format(device))

    def get_status(self, device: str) -> dict:
        for pred in self.pred_data:
            if pred['device'] == device:
                return pred['status']
        logging.error("Status for {} unavailable".format(device))
        api.abort(404, "Status for {} unavailable".format(device))


DAO = AppDAO()


# --- START ENDPOINTS --- #
@ns.route('/', methods=["GET", "POST"])
class Home(Resource):
    def get(selfs):
        """Access main page"""
        return render_template('index.html', context='templates')


# @MAIN.route('/')
@ns.route('/doc', methods=['GET'])
class PredictionList(Resource):
    """Shows a list of all predictions"""

    @ns.doc('list_predictions')
    @ns.marshal_list_with(prediction, skip_none=True)
    def get(self):
        """List all predictions"""
        return DAO.list()


@ns.route('/doc/<string:device>')
@ns.response(404, 'Prediction not found')
@ns.param('device', 'The device to get the prediction from [raspberry, pc1, pc2]')
# @MAIN.route('/<string:device>')
class Prediction(Resource):
    """Show the predictions for a given device"""

    @ns.doc('get_device')
    @ns.marshal_with(prediction, skip_none=True)
    def get(self, device):
        """List all predictions for a given device"""
        return DAO.get(device=device)


@ns.route('/doc/<string:device>/status')
@ns.response(404, 'Status not found')
@ns.param('device', 'The device to get the prediction from [raspberry, pc1, pc2]')
# @MAIN.route('/<string:device>')
class Status(Resource):
    """Show the latest status for a given device"""

    @ns.doc('get_status')
    @ns.marshal_with(prediction, skip_none=True)
    def get(self, device):
        """Get the latest prediction status for a given device"""
        return DAO.get_status(device=device)


# def get_prediction():
#     """
#         This method is to be called by kafka
#         it will return a prediction of the status of the machine
#     """
#     data = json.loads(request.data)
#
#     if data["device"] in model.config.map_device_mode.keys():
#         trained_model = model.config.map_device_mode[data["device"]]
#         data_x = data["data"]
#         x = []
#
#         for elt in model.config.map_device_x[data["device"]]:
#             print(elt)
#             x.append(data_x[elt])
#
#         with open(trained_model, 'rb') as f:
#             lr = pickle.load(f)
#             prediction = lr.predict([x])
#
#             return {
#                 "prediction": str(prediction)
#             }
#
#             print(str(prediction))
#     return ""


# --- END ENDPOINTS --- #


# --- MONITORING --- #
# Provide app's version and deploy environment/config name to set a gauge metric
# app.register_blueprint(MAIN)
# register_metrics(app, app_version="v1.0", app_config="staging")

# Plug metrics WSGI app to the app with dispatcher
# dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
# --- MONITORING --- #


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # run_simple(hostname="0.0.0.0", port=5000, application=dispatcher)

'''
        # Parse the command line.
        parser = ArgumentParser()
        parser.add_argument('config_file', type=FileType('r'))
        parser.add_argument('--reset', action='store_true')
        args = parser.parse_args()

        # Loads the environmental variables within the .env file
        load_dotenv()
        # Initializes a configuration dictionary
        config =    {'bootstrap.servers': os.environ['BOOTSTRAP.SERVERS'], 'security.protocol': os.environ['SECURITY.PROTOCOL'], 
                    'sasl.mechanisms': os.environ['SASL.MECHANISMS'], 'sasl.username': os.environ['KAFKA_CLUSTER_KEY'], 
                    'sasl.password': os.environ['KAFKA_CLUSTER_SECRET'], 'group.id': os.environ['GROUP.ID'], 
                    'auto.offset.reset': os.environ['AUTO.OFFSET.RESET']}
        # Creates a Consumer instance
        consumer = Consumer(config)

        # Set up a callback to handle the '--reset' flag.
        def reset_offset(consumer, partitions):
            if args.reset:
                for p in partitions:
                    p.offset = OFFSET_BEGINNING
                consumer.assign(partitions)
        # Select the Kafka topic in confluenct cloud we will be consuming records from
        topic = os.environ['TOPIC_NAME']
        consumer.subscribe([topic], on_assign=reset_offset)


        # Poll for new messages from Kafka and print them.
        try:
            # Initializes a dictionary of records consumed from the kafka topic, it contains 6 key-value pairs that represents device components

            #records_dict = {key_dict: [] for key_dict in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}
            records_dict = {key: None for key in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}
            #records_dict_max_values = {key_dict: [] for key_dict in ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package', 'Temperature GPU Core', 'Load GPU Core']}

            # Initiliazes a counter to determine when to predict
            count = 0    
            while True:
                msg = consumer.poll(1.0)

                if msg is None:
                    # Initial message consumption may take up to
                    # `session.timeout.ms` for the consumer group to
                    # rebalance and start consuming
                    print("Waiting...")
                elif msg.error():
                    print("ERROR: %s".format(msg.error()))
                else:
                    # Extract the key and value and append the value to the corresponding list
                    topic=msg.topic()              
                    key=msg.key().decode('utf-8')           
                    value=msg.value().decode('utf-8')

                    # Appends the value consumed to the 'records_dict' dictionary
                    records_dict[key] = float(value)
                    print()
                    #print(" Consumed event from topic "+topic+" -- "+key+" -- "+str(value_parsed_3[0]))
                    #print(" Consumed event from topic "+topic+" -- "+key+" -- "+value)
                    count += 1
                    #print(" Count = "+str(count)+" Length Dict = "+str(len(records_dict)))
                    print()

                    # Condition to check is current size of 'record_dict' dictionary reached the number of devices components    
                    if count == len(records_dict):
                        print()
                        print(" I am in prediction condition  ")
                        print()
                        count = 0

                        #model = pickle.load(open('ml_model.pkl', 'rb'))                       
                        model = pickle.load(open('model/exported_models/pc1_model.bin', 'rb'))
                        #print("Model Object: ", model)


                        list_for_prediction_to_display = [records_dict['Clock CPU Core #1'], 
                                                            records_dict['Temperature CPU Package'],
                                                            records_dict['Load CPU Total'],
                                                            records_dict['Power CPU Package'],
                                                            records_dict['Temperature GPU Core'],
                                                            records_dict['Load GPU Core']]


                        # Creates the list to predict
                        list_for_prediction = [list_for_prediction_to_display]
                        print()
                        print(list_for_prediction)
                        print()
                        # Predicts the result
                        print("In the process of making a prediction.")                                                                                          
                        prediction = model.predict(list_for_prediction)

                        # Displays Results and Prediction in the CLI
                        print()
                        print(" Consumed events from Kafka and their prediction: ")
                        print()
                        print(pd.DataFrame(list_for_prediction_to_display, index=records_dict.keys()))
                        print()
                        print(" Prediction is: ")
                        print()
                        predicted = "No technical intervention is required" if prediction else "Technical intervention is required"
                        print(predicted+" for this device ")
                        print()
                        print() 

                        # Sends the results to the template page 'index_two.html'


                        # TO COMPLETE for auto refresh webpage feature 
                        resultPredicted = f"The model has predicted that the result is: {predicted}"                     
                        #outputResultsTest()

                        page = outputResults(records_dict['Clock CPU Core #1'], 
                                            records_dict['Temperature CPU Package'],
                                            records_dict['Load CPU Total'],
                                            records_dict['Power CPU Package'],
                                            records_dict['Temperature GPU Core'],
                                            records_dict['Load GPU Core'], 
                                            resultPredicted)

                        return outputResults(records_dict['Clock CPU Core #1'], 
                                            records_dict['Temperature CPU Package'],
                                            records_dict['Load CPU Total'],
                                            records_dict['Power CPU Package'],
                                            records_dict['Temperature GPU Core'],
                                            records_dict['Load GPU Core'], 
                                            resultPredicted)



        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            consumer.close()            




        return render_template('index_two.html', 
                                resultClock=2, 
                                resultTemperatureCPU=6, 
                                resultLoadCPUTotal=8, 
                                resultPowerCPUPackage=10,
                                resultTemperatureGPUCore=12, 
                                resultLoadGPUCore=14, resultPrediction=result)    


'''

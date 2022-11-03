from flask import Flask, request, Blueprint
from flask_restx import Api, Resource, fields
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from werkzeug.serving import run_simple
from helpers.config_mongodb import get_data_from_mongodb
import json
import logging
import model.config
import pickle

logging.basicConfig()
logger = logging.getLogger(__name__)

# Blueprint definition for monitoring purposes
# MAIN = Blueprint("main", __name__)

app = Flask(__name__)

# metrics = PrometheusMetrics(app, group_by='endpoint')  # Prometheus monitoring

api = Api(app,
          version='1.0',
          title='Monitoring Device Prediction REST API',
          description='Documentation of the Monitoring Device Prediction REST API'
          )

ns = api.namespace('predictions', description='operations')

prediction = api.model('Prediction', {
    'device': fields.String(required=True, description="The device name of the prediction."),
    'example': fields.String(required=True, description="This is another example.")
})


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

# @MAIN.route('/')
@ns.route('/', methods=['GET'])
class PredictionList(Resource):
    """Shows a list of all predictions"""

    @ns.doc('list_predictions')
    @ns.marshal_list_with(prediction, skip_none=True)
    def get(self):
        """List all predictions"""
        return DAO.list()


@ns.route('/<string:device>')
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


@ns.route('/<string:device>/status')
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

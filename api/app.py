from flask import Flask
from flask_restx import Api, Resource, fields
from helpers.queries import get_all_data, get_data_device, get_device_status
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


# Start Flask API
app = Flask(__name__)

api = Api(app,
          version='1.0',
          title='Monitoring Device Prediction REST API',
          description='Documentation of the Monitoring Device Prediction REST API'
          )

ns = api.namespace('devices', description='operations')


pc1 = api.model('PC1', {
    'uuid': fields.String(required=True, description="Universal Unique Identifier"),
    'device': fields.String(required=True, description="The name of the device (pc1)."),
    'ClockCPUCoreOne': fields.String(required=True, description="Clock CPU in Core 1."),
    'TemperatureCPUPackage': fields.String(required=True, description="CPU Package Temperature in ºC."),
    'LoadCPUTotal': fields.String(required=True, description="Total Load of the CPU."),
    'PowerCPUPackage': fields.String(required=True, description="Power of the CPU package."),
    'TemperatureGPUCore': fields.String(required=True, description="GPU Core Temperature in ºC."),
    'LoadGPUCore': fields.String(required=True, description="Load GPU Core.")
})

pc2 = api.model('PC2', {
    'uuid': fields.String(required=True, description="Universal Unique Identifier"),
    'device': fields.String(required=True, description="The name of the device (pc2)."),
    'ClockCPUCoreOne': fields.String(required=True, description="Clock CPU in Core 1."),
    'TemperatureCPUPackage': fields.String(required=True, description="CPU Package Temperature in ºC."),
    'LoadCPUTotal': fields.String(required=True, description="Total Load of the CPU."),
    'PowerCPUPackage': fields.String(required=True, description="Power of the CPU package.")})

rasp = api.model('Raspberry', {
    'uuid': fields.String(required=True, description="Universal Unique Identifier"),
    'device': fields.String(required=True, description="The name of the device (raspberry)."),
    'GPU_temp_celsius': fields.String(required=True, description="Temperature of GPU in ºC."),
    'CPU_temp_celsius': fields.String(required=True, description="Temperature CPU in ºC."),
    'frequency_arm_hz': fields.String(required=True, description="ARM frequency in Hz."),
    'frequency_core_hz': fields.String(required=True, description="Core frequency in Hz."),
    'frequency_pwm_hz': fields.String(required=True, description="Power frequency in Hz."),
    'voltage_core_v': fields.String(required=True, description="Core Voltage V."),
    'voltage_sdram_c_v': fields.String(required=True, description="SDRAM Voltage C V."),
    'voltage_sdram_i_v': fields.String(required=True, description="SDRAM Voltage I V."),
    'voltage_sdram_p_v': fields.String(required=True, description="SDRAM Voltage P V."),
    'memory_arm_bytes': fields.String(required=True, description="Memory ARM in Bytes."),
    'memory_gpu_bytes': fields.String(required=True, description="Memory GPU in Bytes."),
    'throttled': fields.String(required=True, description="Indicates whether the Raspberry Pi is stressed.")
})


# --- START ENDPOINTS --- #
@ns.route('/')
class DeviceList(Resource):
    """Shows a list of all devices and its sensor's values"""

    @ns.doc('list_devices')
    # @ns.marshal_list_with(, skip_none=True)
    def get(self):
        """List all devices"""
        return get_all_data()


@ns.route('/pc1')
@ns.response(404, 'Device not found')
class PC1Device(Resource):
    """Show the data for PC1"""

    @ns.doc('get_pc1')
    @ns.marshal_with(pc1, skip_none=True)
    def get(self):
        """List all predictions for the PC1 device"""
        return get_data_device(device='pc1')


@ns.route('/pc2')
@ns.response(404, 'Device not found')
class PC2Device(Resource):
    """Show the data for PC2"""

    @ns.doc('get_pc2')
    @ns.marshal_with(pc2, skip_none=True)
    def get(self):
        """List all predictions for the PC2 device"""
        return get_data_device(device='pc2')


@ns.route('/raspberry')
@ns.response(404, 'Device not found')
class RaspDevice(Resource):
    """Show the data for Raspberry"""

    @ns.doc('get_raspberry')
    @ns.marshal_with(rasp, skip_none=True)
    def get(self):
        """List all predictions for the Raspberry Pi device"""
        return get_data_device(device='raspberry')


@ns.route('/pc1/status')
@ns.response(404, 'Status not found')
class PC1Status(Resource):
    """Show the latest status for the PC1 device"""

    @ns.doc('get_pc1_status')
    def get(self):
        """Get the latest prediction status for pc1"""
        return get_device_status(device='pc1')


@ns.route('/pc2/status')
@ns.response(404, 'Status not found')
class PC2Status(Resource):
    """Show the latest status for the PC2 device"""

    @ns.doc('get_pc2_status')
    def get(self):
        """Get the latest prediction status for pc2"""
        return get_device_status(device='pc2')


@ns.route('/raspberry/status')
@ns.response(404, 'Status not found')
class RaspStatus(Resource):
    """Show the latest status for the raspberry device"""

    @ns.doc('get_raspberry_status')
    def get(self):
        """Get the latest prediction status for raspberry"""
        return get_device_status(device='raspberry')

# --- END ENDPOINTS --- #


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

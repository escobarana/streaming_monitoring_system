import wmi
from api.sensors.sensor import Sensor
import uuid
from datetime import datetime


class Measures:
    """
        Class Measures which measures different types of CPU sensors (Temperature, Power, Load)
    """

    def __init__(self):
        """
            Initialization of the class Measures using wmi library and OpenHardMonitor Software
        """
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        self.temperature_info = w.Sensor()

    def get_temperature_info(self):
        """
            This is a getter to return the temperature_info attribute of an Measures object
        """
        return self.temperature_info

    def get_temperature(self) -> Sensor:
        """
            Function to measure CPU temperature in celsius
        :return: Sensor object containing CPU temperature sensor relevant information
        """
        sensor = Sensor(sensor_id="", name="", sensor_type="", measure=0, maximum=0)
        for each in self.temperature_info:
            if each.SensorType == 'Temperature':
                sensor.sensor_id = each.InstanceId
                sensor.name = each.Name
                sensor.sensor_type = each.SensorType
                sensor.measure = each.Value
                sensor.maximum = each.Max
        return sensor

    def get_power(self) -> Sensor:
        """
            Function to measure CPU power in watt
        :return: Sensor object containing CPU power sensor relevant information
        """
        sensor = Sensor(sensor_id="", name="", sensor_type="", measure=0, maximum=0)
        for each in self.temperature_info:
            if each.SensorType == 'Power':
                sensor.sensor_id = each.InstanceId
                sensor.name = each.Name
                sensor.sensor_type = each.SensorType
                sensor.measure = each.Value
                sensor.maximum = each.Max
        return sensor

    def get_load(self) -> Sensor:
        """
            Function to measure CPU load in percentage
        :return: Sensor object containing CPU load sensor relevant information
        """
        sensor = Sensor(sensor_id="", name="", sensor_type="", measure=0, maximum=0)
        for each in self.temperature_info:
            if each.SensorType == 'Load':
                sensor.sensor_id = each.InstanceId
                sensor.name = each.Name
                sensor.sensor_type = each.SensorType
                sensor.measure = each.Value
                sensor.maximum = each.Max
        return sensor

    def get_voltage(self) -> Sensor:
        """
            Function to measure CPU voltage in volts
        :return: Sensor object containing CPU voltage sensor relevant information
        """
        sensor = Sensor(sensor_id="", name="", sensor_type="", measure=0, maximum=0)
        for each in self.temperature_info:
            if each.SensorType == 'Voltage':
                sensor.sensor_id = each.InstanceId
                sensor.name = each.Name
                sensor.sensor_type = each.SensorType
                sensor.measure = each.Value
                sensor.maximum = each.Max
        return sensor

    def get_fan(self) -> Sensor:
        """
            Function to measure CPU fan in CFM
        :return: Sensor object containing CPU fan sensor relevant information
        """
        sensor = Sensor(sensor_id="", name="", sensor_type="", measure=0, maximum=0)
        for each in self.temperature_info:
            if each.SensorType == 'Fan':
                sensor.sensor_id = each.InstanceId
                sensor.name = each.Name
                sensor.sensor_type = each.SensorType
                sensor.measure = each.Value
                sensor.maximum = each.Max
        return sensor

    def get_clock(self) -> Sensor:
        """
            Function to measure CPU clock in GHz
        :return: Sensor object containing CPU clock sensor relevant information
        """
        sensor = Sensor(sensor_id="", name="", sensor_type="", measure=0, maximum=0)
        for each in self.temperature_info:
            if each.SensorType == 'Clock':
                sensor.sensor_id = each.InstanceId
                sensor.name = each.Name
                sensor.sensor_type = each.SensorType
                sensor.measure = each.Value
                sensor.maximum = each.Max
        return sensor

    def get_desired_data(self, device_name: str):
        """
            This method returns the desired data structure to be produced to the Kafka topic
        :param device_name: name of the device
        :return: dictionary containing all the sensors' data in the desired format
        """
        my_dict = {}
        if device_name == 'pc1':
            # Initialization of a list of sensor types and their names according to the list 'temperature_info'
            data_fields = ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package',
                           'Temperature GPU Core', 'Load GPU Core']

            data_values = [[x.SensorType + " " + x.Name, x.Value] for x in self.temperature_info if
                           x.SensorType + " " + x.Name in data_fields]

            my_dict = {'uuid': str(uuid.uuid4()), 'device': device_name,
                       'loading_datetime': datetime.today().strftime('%Y-%m-%d@%H:%M:%S')}

            for i in range(6):
                user_id = ((data_values[i][0]).replace("#1", "One")).replace(" ", "")
                product = data_values[i][1]

                my_dict[user_id] = product

        elif device_name == 'pc2':
            # Initialization of a list of sensor types and their names according to the list 'temperature_info'
            data_fields = ['Clock CPU Core #1', 'Temperature CPU Package', 'Load CPU Total', 'Power CPU Package']

            # A List Comprehension to create of a list of lists containing the sensor types, the names and the values
            data_values = [[x.SensorType + " " + x.Name, x.Value] for x in self.temperature_info if
                           x.SensorType + " " + x.Name in data_fields]

            my_dict = {'uuid': str(uuid.uuid4()), 'device': device_name,
                       'loading_datetime': datetime.today().strftime('%Y-%m-%d@%H:%M:%S')}

            for i in range(4):
                user_id = ((data_values[i][0]).replace("#1", "One")).replace(" ", "")
                product = data_values[i][1]

                my_dict[user_id] = product
        else:
            print(f"'{device_name}' is not a valid device name.")

        return my_dict

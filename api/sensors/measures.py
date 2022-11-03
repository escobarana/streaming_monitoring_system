import wmi
from api.sensors.sensor import Sensor


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

class Sensor:
    """
    Class to identify the properties of a sensor and deserialize the data when consuming from a Kafka topic
    """

    def __init__(self, sensor_id, name, sensor_type, measure, maximum):
        """
        Initialization of class Sensor
        :param sensor_id: Unique identifier of the sensor
        :param name: Sensor's name
        :param sensor_type: Type of the sensor (Temperature, Power, Load)
        :param measure: The value of the measure (ºC, w, %)
        :param maximum: Maximum value the sensor can reach
        """
        self.sensor_id = sensor_id
        self.name = name
        self.sensor_type = sensor_type
        self.measure = measure
        self.maximum = maximum

    def set_sensor_id(self, sensor_id):
        self.sensor_id = sensor_id

    def set_name(self, name):
        self.name = name

    def set_sensor_type(self, sensor_type):
        self.sensor_type = sensor_type

    def set_measure(self, measure):
        self.measure = measure

    def set_maximum(self, maximum):
        self.maximum = maximum

    def get_measure(self):
        return self.measure

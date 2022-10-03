class Sensor(object):
    """
        Class to identify the properties of a sensor and deserialize the data when consuming from a Kafka topic
    """
    _device = None
    _sensor_id = None
    _name = None
    _sensor_type = None
    _measure = None
    _maximum = None

    def __new__(cls, sensor_id, name, sensor_type, measure, maximum):
        """
            Initialization of class Sensor
        :param sensor_id: Unique identifier of the sensor
        :param name: Sensor's name
        :param sensor_type: Type of the sensor (Temperature, Power, Load)
        :param measure: The value of the measure (ºC, w, %)
        :param maximum: Maximum value the sensor can reach
        """
        cls._device = 'CPU'
        cls._sensor_id = sensor_id
        cls._name = name
        cls._sensor_type = sensor_type
        cls._measure = measure
        cls._maximum = maximum

    # --- GETTERS AND SETTERS --- #
    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, val):
        self._device = val

    @property
    def sensor_id(self):
        return self._sensor_id

    @sensor_id.setter
    def sensor_id(self, val):
        self._sensor_id = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def sensor_type(self):
        return self._sensor_type

    @sensor_type.setter
    def sensor_type(self, val):
        self._sensor_type = val

    @property
    def measure(self):
        return self._measure

    @measure.setter
    def measure(self, val):
        self._measure = val

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, val):
        self._maximum = val

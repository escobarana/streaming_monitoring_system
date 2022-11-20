class Pc(object):
    """
        Class Measures which measures different types of CPU sensors (Temperature, Power, Load)
    """

    def __init__(self, uuid, device, loading_datetime, ClockCPUCoreOne, TemperatureCPUPackage, LoadCPUTotal,
                 PowerCPUPackage, TemperatureGPUCore=None, LoadGPUCore=None):
        """
            Initialization of the class Measures using wmi library and OpenHardMonitor Software
        """

        self.uuid = uuid
        self.device = device
        self.loading_datetime = loading_datetime
        self.ClockCPUCoreOne = ClockCPUCoreOne
        self.TemperatureCPUPackage = TemperatureCPUPackage
        self.PowerCPUPackage = PowerCPUPackage
        self.LoadCPUTotal = LoadCPUTotal
        # Optional #
        self.TemperatureGPUCore = TemperatureGPUCore
        self.LoadGPUCore = LoadGPUCore

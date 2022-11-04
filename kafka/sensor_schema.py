schema = """
{
  "description": "Sensor's measurements",
  "properties": {
  "Device": {
      "description": "Device name",
      "type": "string"
    },
    "ClockCPUCoreOne": {
      "description": "",
      "type": "number"
    },
    "TemperatureCPUPackage": {
      "description": "",
      "type": "number"
    },
    "LoadCPUTotal": {
      "description": "",
      "type": "number"
    },
    "PowerCPUPackage": {
      "description": "",
      "type": "number"
    }
    "TemperatureGPUCore": {
      "description": "",
      "type": "number"
    },
    "LoadGPUCore": {
      "description": "",
      "type": "number"
    },
    "Throttled": {
      "description": "",
      "type": "number"
    },
    "loading_datetime": {
      "description": "",
      "type": "string"
    }
  },
  "required": [
    "Device",
    "ClockCPUCoreOne",
    "TemperatureCPUPackage",
    "LoadCPUTotal",
    "PowerCPUPackage",
    "TemperatureGPUCore",
    "LoadGPUCore",
    "Throttled",
    "loading_datetime"
  ],
  "title": "Sensor",
  "type": "object"
}
"""

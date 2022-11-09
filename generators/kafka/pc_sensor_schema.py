"""This file represents the topic 'pc' schema for data validation purposes"""
schema = """
{
  "description": "Pc's measurements",
  "properties": {
  "uuid": {
      "description": "UUID4",
      "type": "string"
    },
  "device": {
      "description": "Device name",
      "type": "string"
    },
    "ClockCPUCoreOne": {
      "description": "Clock measurement of the CPU Core number 1",
      "type": "number"
    },
    "TemperatureCPUPackage": {
      "description": "Temperature of the CPU",
      "type": "number"
    },
    "LoadCPUTotal": {
      "description": "Total load of the CPU",
      "type": "number"
    },
    "PowerCPUPackage": {
      "description": "Power of the CPU",
      "type": "number"
    },
    "TemperatureGPUCore": {
      "description": "Temperature measurement of the GPU Core",
      "type": "number"
    },
    "LoadGPUCore": {
      "description": "Load measurement of the GPU Core",
      "type": "number"
    },
    "loading_datetime": {
      "description": "Loading datetime of the message",
      "type": "string"
    }
  },
  "required": [
    "uuid",
    "device",
    "ClockCPUCoreOne",
    "TemperatureCPUPackage",
    "LoadCPUTotal",
    "PowerCPUPackage",
    "loading_datetime"
  ],
  "title": "PC",
  "type": "object"
}
"""
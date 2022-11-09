"""This file represents the topic 'pc' schema for data validation purposes"""
schema = """
{
  "description": "Pc's measurements",
  "properties": {
    "ClockCPUCoreOne": {
      "description": "Clock measurement of the CPU Core number 1",
      "type": "number"
    },
    "LoadCPUTotal": {
      "description": "Total load of the CPU",
      "type": "number"
    },
    "LoadGPUCore": {
      "description": "Load measurement of the GPU Core",
      "type": "number"
    },
    "PowerCPUPackage": {
      "description": "Power of the CPU",
      "type": "number"
    },
    "TemperatureCPUPackage": {
      "description": "Temperature of the CPU",
      "type": "number"
    },
    "TemperatureGPUCore": {
      "description": "Temperature measurement of the GPU Core",
      "type": "number"
    },
    "device": {
      "description": "Device name",
      "type": "string"
    },
    "loading_datetime": {
      "description": "Loading datetime of the message",
      "type": "string"
    },
    "uuid": {
      "description": "UUID4",
      "type": "string"
    }
  },
  "required": [
    "uuid",
    "device",
    "loading_datetime",
    "ClockCPUCoreOne",
    "PowerCPUPackage",
    "LoadCPUTotal",
    "TemperatureCPUPackage"
  ],
  "title": "PC",
  "type": "object"
}
"""
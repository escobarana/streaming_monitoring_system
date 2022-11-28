"""This file represents the topic 'raspberry' schema for data validation purposes"""
schema = """
{
  "description": "Raspberry Pi measurements",
  "properties": {
  "uuid": {
      "description": "UUID4",
      "type": "string"
    },
  "device": {
      "description": "Device name",
      "type": "string"
    },
    "GPU_temp_celsius": {
      "description": "GPU temperature value",
      "type": "number"
    },
    "CPU_temp_celsius": {
      "description": "CPU temperature value",
      "type": "number"
    },
    "frequency_arm_hz": {
      "description": "Frequency value of ARM",
      "type": "number"
    },
    "frequency_core_hz": {
      "description": "Frequency value of core",
      "type": "number"
    },
    "frequency_pwm_hz": {
      "description": "",
      "type": "number"
    },
    "voltage_core_v": {
      "description": "Voltage value of core",
      "type": "number"
    },
    "voltage_sdram_c_v": {
      "description": "Voltage value of SDRAM cv",
      "type": "number"
    },
    "voltage_sdram_i_v": {
      "description": "Voltage value of SDRAM iv",
      "type": "number"
    },
    "voltage_sdram_p_v": {
      "description": "Voltage value of SDRAM pv",
      "type": "number"
    },
    "memory_arm_bytes": {
      "description": "ARM memory value",
      "type": "number"
    },
    "memory_gpu_bytes": {
      "description": "GPU memory value",
      "type": "number"
    },
    "throttled": {
      "description": "Throttled value",
      "type": "string"
    },
    "loading_datetime": {
      "description": "Datetime value of the produced message",
      "type": "string"
    }
  },
  "required": [
    "uuid",
    "device",
    "GPU_temp_celsius",
    "CPU_temp_celsius",
    "frequency_arm_hz",
    "frequency_core_hz",
    "frequency_pwm_hz",
    "voltage_core_v",
    "voltage_sdram_c_v",
    "voltage_sdram_i_v",
    "voltage_sdram_p_v",
    "memory_arm_bytes",
    "memory_gpu_bytes",
    "throttled",
    "loading_datetime"
  ],
  "title": "RaspberryPi",
  "type": "object"
}
"""

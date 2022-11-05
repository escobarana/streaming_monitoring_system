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
      "description": "",
      "type": "number"
    },
    "CPU_temp_celsius": {
      "description": "",
      "type": "number"
    },
    "frequency_arm_hz": {
      "description": "",
      "type": "number"
    },
    "frequency_core_hz": {
      "description": "",
      "type": "number"
    },
    "frequency_pwm_hz": {
      "description": "",
      "type": "number"
    },
    "voltage_core_v": {
      "description": "",
      "type": "number"
    },
    "voltage_sdram_c_v": {
      "description": "",
      "type": "number"
    },
    "voltage_sdram_i_v": {
      "description": "",
      "type": "number"
    },
    "voltage_sdram_p_v": {
      "description": "",
      "type": "number"
    },
    "memory_arm_bytes": {
      "description": "",
      "type": "number"
    },
    "memory_gpu_bytes": {
      "description": "",
      "type": "number"
    },
    "throttled": {
      "description": "",
      "type": "string"
    },
    "loading_datetime": {
      "description": "",
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

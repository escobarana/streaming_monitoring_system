map_device_mode = {
    "pc1": "model/exported_models/pc1_model.bin",
    "pc2": "model/exported_models/pc1_model.bin",
    "raspberry": "model/exported_models/raspb_model.bin"
}

pc2_local_data_path = "data/datasetWithOnesAndZeros2.csv"
pc2_features = ['ClockCPUCoreOne', 'TemperatureCPUPackage',
                'LoadCPUTotal', 'PowerCPUPackage']
pc2_target = ['NoTechnicalInterventionRequired']

pc1_local_data_path = "data/datasetWithOnesAndZeros.csv"
pc1_features = ['ClockCPUCoreOne', 'TemperatureCPUPackage',
                'LoadCPUTotal', 'PowerCPUPackage', 'TemperatureGPUCore', 'LoadGPUCore']
pc1_target = ['NoTechnicalInterventionRequired']

rasb_local_data_path = "data/raspberrypi_data.csv"
rasb_features = ['GPU_temp_celsius', 'CPU_temp_celsius',
                 'frequency_arm_hz', 'frequency_core_hz', 'frequency_pwm_hz',
                 'voltage_core_v']

map_device_x = {
    "pc1": pc1_features,
    "pc2": pc2_features,
    "raspberry": rasb_features
}

raspb_target = ['throttled']

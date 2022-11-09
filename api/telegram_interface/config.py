"""
    Configuration file with templates to write the data in the Telegram channel
"""
template_message_pc2 = "PC 2\n" + \
                       " 🕒 ClockCPUCoreOne          : {var1} \n" + \
                       " 🌡️ TemperatureCPUPackage   : {var2} \n" + \
                       " ⌛ LoadCPUTotal             : {var3} \n" + \
                       " ⚡ PowerCPUPackage          : {var4} \n" + \
                       " --------------------------------- \n" + \
                       " 📊 Prediction               : {var5} "

template_message_pc1 = "PC 1\n" + \
                       " 🕒 ClockCPUCoreOne          : {var1} \n" + \
                       " 🌡️ TemperatureCPUPackage   : {var2} \n" + \
                       " ⌛ LoadCPUTotal             : {var3} \n" + \
                       " ⚡ PowerCPUPackage          : {var4} \n" + \
                       " 🌡️ TemperatureGPUCore      : {var5} \n" + \
                       " ⌛ LoadGPUCore              : {var6} \n" + \
                       " --------------------------------- \n" + \
                       " 📊 Prediction               : {var7} "

template_message_rasp = "RASPBERRY PI 4B \n" + \
                        " 🕒 ClockCPUCoreOne         : {var1} \n" + \
                        " 🌡️ TemperatureCPUPackage  : {var2} \n" + \
                        " ⌛ LoadCPUTotal            : {var3} \n" + \
                        " ⚡ PowerCPUPackage         : {var4} \n" + \
                        " 🌡️ TemperatureGPUCore     : {var5} \n" + \
                        " ⌛ LoadGPUCore             : {var6} \n" + \
                        " --------------------------------- \n" + \
                        " 📊 Prediction              : {var7} "

pc2_features = ['ClockCPUCoreOne', 'TemperatureCPUPackage', 'LoadCPUTotal', 'PowerCPUPackage']

pc1_features = ['ClockCPUCoreOne', 'TemperatureCPUPackage', 'LoadCPUTotal', 'PowerCPUPackage', 'TemperatureGPUCore',
                'LoadGPUCore']

rasb_features = ['GPU_temp_celsius', 'CPU_temp_celsius', 'frequency_arm_hz', 'frequency_core_hz', 'frequency_pwm_hz',
                 'voltage_core_v']

link_model_pc1 = "https://dstimlmodels.s3.amazonaws.com/pc1_model.bin"
link_model_pc2 = "https://dstimlmodels.s3.amazonaws.com/pc2_model.bin"
link_model_raspberry = "https://dstimlmodels.s3.amazonaws.com/raspb_model.bin"

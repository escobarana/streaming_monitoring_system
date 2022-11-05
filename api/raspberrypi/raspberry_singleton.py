import vcgencmd
import subprocess
from datetime import datetime
import uuid


class Raspberry(object):
    """
        This class defines a Raspberry Pi object with its attributes in order to monitor its health
    """
    _raspberry_instance = None  # Initialize the instance to 'None' for Singleton Pattern

    _uuid = None
    _device = None
    _gpu_temp_celsius = None
    _cpu_temp_celsius = None
    _frequency_arm_hz = None
    _frequency_core_hz = None
    _frequency_pwm_hz = None
    _voltage_core_v = None
    _voltage_sdram_c_v = None
    _voltage_sdram_i_v = None
    _voltage_sdram_p_v = None
    _memory_arm_bytes = None
    _memory_gpu_bytes = None
    _throttled = None

    def __new__(cls):
        """
            This function creates a new raspberry pi instance if it doesn't exist yet
        """
        if cls._raspberry_instance is None:
            cls._raspberry_instance = super(Raspberry, cls).__new__(cls)

            my_cmd = vcgencmd.Vcgencmd()

            cls._uuid = uuid.uuid4()  # Generates a random and secured UUID.
            cls._device = "raspberry"
            cls._gpu_temp_celsius = my_cmd.measure_temp()

            cpu = subprocess.Popen(['cat', '/sys/class/thermal/thermal_zone0/temp'],
                                   stdout=subprocess.PIPE).communicate()[0]
            cls._cpu_temp_celsius = (int(cpu) / 1000)
            cls._frequency_arm_hz = my_cmd.measure_clock('arm')
            cls._frequency_core_hz = my_cmd.measure_clock('core')
            cls._frequency_pwm_hz = my_cmd.measure_clock('pwm')
            cls._voltage_core_v = my_cmd.measure_volts('core')
            cls._voltage_sdram_c_v = my_cmd.measure_volts('sdram_c')
            cls._voltage_sdram_i_v = my_cmd.measure_volts('sdram_i')
            cls._voltage_sdram_p_v = my_cmd.measure_volts('sdram_p')
            cls._memory_arm_bytes = my_cmd.get_mem('arm')
            cls._memory_gpu_bytes = my_cmd.get_mem('gpu')

            throttled_out = subprocess.Popen(['vcgencmd', 'get_throttled'], stdout=subprocess.PIPE).communicate()
            throttled_value = throttled_out[0].decode().split('=')[1]
            cls._throttled = throttled_value.split('\n')[0]

        return cls._raspberry_instance

    # --- GETTERS [NO SETTERS - DATA CANNOT BE MODIFIED] ---#
    @property
    def uuid(self):
        return self._uuid

    @property
    def device(self):
        return self._device

    @property
    def gpu_temp_celsius(self):
        return self._gpu_temp_celsius

    @property
    def cpu_temp_celsius(self):
        return self._cpu_temp_celsius

    @property
    def frequency_arm_hz(self):
        return self._frequency_arm_hz

    @property
    def frequency_core_hz(self):
        return self._frequency_core_hz

    @property
    def frequency_pwm_hz(self):
        return self._frequency_pwm_hz

    @property
    def voltage_core_v(self):
        return self._voltage_core_v

    @property
    def voltage_sdram_c_v(self):
        return self._voltage_sdram_c_v

    @property
    def voltage_sdram_i_v(self):
        return self._voltage_sdram_i_v

    @property
    def voltage_sdram_p_v(self):
        return self._voltage_sdram_p_v

    @property
    def memory_arm_bytes(self):
        return self._memory_arm_bytes

    @property
    def memory_gpu_bytes(self):
        return self._memory_gpu_bytes

    @property
    def throttled(self):
        return self._throttled

    @property
    def json(self):
        """
            This function returns a json document with all the raspberry pi information
        :return: json document
        """
        return {
            "device": self.device,
            "loading_datetime": datetime.today().strftime('%Y-%m-%d@%H:%M:%S'),
            "GPU_temp_celsius": self.gpu_temp_celsius,
            "CPU_temp_celsius": self.cpu_temp_celsius,
            "frequency_arm_hz": self.frequency_arm_hz,
            "frequency_core_hz": self.frequency_core_hz,
            "frequency_pwm_hz": self.frequency_pwm_hz,
            "voltage_core_v": self.voltage_core_v,
            "voltage_sdram_c_v": self.voltage_sdram_c_v,
            "voltage_sdram_i_v": self.voltage_sdram_i_v,
            "voltage_sdram_p_v": self.voltage_sdram_p_v,
            "memory_arm_bytes": self.memory_arm_bytes,
            "memory_gpu_bytes": self.memory_gpu_bytes,
            "throttled": self.throttled
        }

    def __str__(self):
        return str(self.json)

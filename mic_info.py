import pyaudio
PA = pyaudio.PyAudio()
for device_index in range(PA.get_device_count()):
    info = PA.get_device_info_by_index(device_index)
    for key in info.keys():
        print(key, ' = ', info[key])

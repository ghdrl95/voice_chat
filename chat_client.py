import socket
import pyaudio
import sys
import threading

# 음성 출력 설정
RATE = 44100
CHANNELS = 1
FORMAT = pyaudio.paInt16
O_DEVICE_INDEX = 4  # 스피커 장치 인댁스 동봉된 mic_info 파일로 확인해서 변경
I_DEVICE_INDEX = 1  # 마이크 장치 인댁스 동봉된 mic_info 파일로 확인해서 변경
CHUNK = 8192

pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    global s1
    s1.sendall(in_data)  # buffer size

    return (None, pyaudio.paContinue)

def speaker_thread():
    global data, stream
    while True:
        if data:
            stream.write(data[0])
            del data[0]

stream = pa.open(rate=RATE, channels=CHANNELS, format=FORMAT, output=True,
                 output_device_index=O_DEVICE_INDEX,
                 frames_per_buffer=CHUNK, start=False)#, stream_callback=callback)

stream1 = pa.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True,
                 input_device_index=I_DEVICE_INDEX,
                 frames_per_buffer=CHUNK, start=False, stream_callback=callback)


# 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        print('클라이언트 시작')
        host = '192.168.0.23'
        port = 8000
        s.connect((host, port))
        s1.connect((host, port))
        print('서버 접속')
        stream.start_stream()
        stream1.start_stream()
        data = []
        t1 = threading.Thread(target=speaker_thread())
        t1.start()

        while True:
            # 음성 데이터 받기
            data.append(s.recv(8192))  # buffer size
            #print(data)
            # 음성 데이터 출력
            #stream.write(data)
            #data=''
            pass
        stream.stop_stream()
        stream1.stop_stream()
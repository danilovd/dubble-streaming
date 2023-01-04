import pyaudio

import dubble_pb2_grpc
import dubble_pb2
import time
import grpc

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096


def get_client_stream():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print('recording...')

    seconds = 15
    for i in range(0, int(RATE/CHUNK * seconds)):

        data = stream.read(CHUNK)
        req = dubble_pb2.AudioData(data=data, channels=CHANNELS, rate=RATE, format=FORMAT)
        yield req

    stream.stop_stream()
    stream.close()
    audio.terminate()

def run():


    with grpc.insecure_channel('localhost:50051') as channel:
        stub = dubble_pb2_grpc.DubbleStub(channel)
        replies = stub.translateAndVoiceStream(get_client_stream())
        print('got replies')
        for r in replies:
            print('reply {}'.format(r))



if __name__ == "__main__":
    run()

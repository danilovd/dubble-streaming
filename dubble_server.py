from concurrent import futures
import time
import pyaudio

import wave

import grpc
import dubble_pb2
import dubble_pb2_grpc
from utils import random_string

class DubbleServiceImpl(dubble_pb2_grpc.DubbleServicer):

    def translateAndVoiceStream(self, request_iterator, context):
        print('translate and voice')
        frames = []
        for req in request_iterator:
            print('got request {}', req.data)
            frames.append(req.data)

        audio = pyaudio.PyAudio()
        wave_file = wave.open("file_{}.wav".format(random_string(4)), 'wb')
        wave_file.setnchannels(1)
        wave_file.setframerate(44100)
        wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        res = dubble_pb2.AudioData()
        yield res

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dubble_pb2_grpc.add_DubbleServicer_to_server(DubbleServiceImpl(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

import numpy as np
import matplotlib.pyplot as plt
import time
import pyaudio

from AUDIOENCODING import binary_to_tones, play_tone
from receiver import record_sound, on_off_keying

CHUNK = 2**5  # bytes of data per chunk of the audio signal
RATE = 44100  # sample rate in kHz
MSGLEN = 10  # length of msg. in seconds. will eventually need to switch to be continuous

message_map = {"LOW OXYGEN": "0110",
        "RISE NOW": "1001",
        "COME HERE":"1110",}

def sender():
    ID_1 = "0101"
    ID_2 = "1010"


    single_packet = ID_1 + message_map["LOW OXYGEN"]
    
    binary_to_tones(single_packet)

# sender()

amplitudes = record_sound(CHUNK, RATE, MSGLEN)
reconstr = on_off_keying(amplitudes)

for message, encoding in message_map.items():
    if encoding in reconstr:
        print(30*":")
        print(message)
        print(30*":")








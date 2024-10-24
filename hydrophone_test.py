import numpy as np
import matplotlib.pyplot as plt
import time
import pyaudio
import wave
import re

from AUDIOENCODING import binary_to_tones, play_tone
from receiver import record_sound, on_off_keying

CHUNK = 2**5  # bytes of data per chunk of the audio signal
RATE = 44100  # sample rate in kHz
MSGLEN = (
    10  # length of msg. in seconds. will eventually need to switch to be continuous
)

message_map = {
    "1011": "wav_files/Low_O2.wav",
    "1001": "wav_files/Return_to_Boat.wav",
    "1110": "wav_files/Look_at_This.wav",
    "0011": "wav_files/SOS.wav",
}

EVAN = "0101"
SARAH = "1010"
SEB = "0110"

id_dict = {
    EVAN: "wav_files/Evan_ID.wav",
    SARAH: "wav_files/Sarah_ID.wav",
    SEB: "wav_files/Seb_ID.wav",
}


def sender():
    EVAN = "0101"
    SARAH = "1010"
    SEB = "0110"

    single_packet = ID_1 + message_map["LOW OXYGEN"]

    binary_to_tones(single_packet)


# sender()

# amplitudes = record_sound(CHUNK, RATE, MSGLEN)
# reconstr = on_off_keying(amplitudes)

# for message, encoding in message_map.items():
#     if encoding in reconstr:
#         print(30*":")
#         print(message)
#         print(30*":")

infile = "putty.log"

important = []
keep_phrases = ["Data"]

with open(infile) as f:
    f = f.readlines()

for line in f:
    for phrase in keep_phrases:
        if phrase in line and "Port" not in line:
            important.append(line)
            break  # NOTE is hthis break necessary?
print(important)

for line in important:
    """split message, take 1st index to get part with data,
    take 11th-2nd to last index to get binary then make it
    into a string"""

    message = re.split("\x1b", line)[1][11:-1]
    print("MESSAGE: ", message)
    msg_str = ""
    for char in message:
        if char not in "[],":
            msg_str += char
    print(msg_str)
    name = msg_str[:4]
    phrase = msg_str[4:]
    print(id_dict[name], message_map[phrase])

    if phrase in message_map:
        msg_file = message_map[phrase]
        name_id = id_dict[name]
        sound = wave.open(msg_file, "rb")
        identifier = wave.open(name_id, "rb")

        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(
            format=p.get_format_from_width(identifier.getsampwidth()),
            channels=identifier.getnchannels(),
            rate=identifier.getframerate(),
            output=True,
        )
        # read data
        data = identifier.readframes(CHUNK)

        # play stream
        while data:
            stream.write(data)
            data = identifier.readframes(CHUNK)

        # stop stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(
            format=p.get_format_from_width(sound.getsampwidth()),
            channels=sound.getnchannels(),
            rate=sound.getframerate(),
            output=True,
        )
        # read data
        data = sound.readframes(CHUNK)

        # play stream
        while data:
            stream.write(data)
            data = sound.readframes(CHUNK)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()
    # if message in {[1, 0, 0, 1]: "LOW OXYGEN"}.keys():
    #     engine = pyttsx3.init()
    #     engine.setProperty("rate", 150)
    #     engine.say("LOW OXYGEN")
    #     engine.runAndWait()

# print(important)

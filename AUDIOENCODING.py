
import numpy as np
import time
import pyaudio
'''Make a fequency based on button press'''
# PyAudio setup
p = pyaudio.PyAudio()
SAMPLE_RATE = 44100
DURATION = .5  # Duration of tone (in seconds)
button_map = {
        "LOW OXYGEN": 250,
        "SOMETHING'S WRONG": 350,
        "RISE NOW": 150,
         "BOAT": 550,
}

def generate_tone(freq, duration):
    '''Generates the tone that will be outputted'''
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = np.sin(2 * np.pi * freq * t)
    return (tone * 32767).astype(np.int16).tobytes()

def play_tone(freq):
    '''Plays Frequency freq'''
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True)
    
    tone = generate_tone(freq, DURATION)
    stream.write(tone)
    stream.stop_stream()
    stream.close()

#Will use when we want to do amplitude control and do binary
def binary_to_tones(binary_code):
    '''Will us to make instances of hi and lo frequencies to encode messages'''
    LOW_FREQ = 440  # A4 note
    HIGH_FREQ = 880  # A5 note
    
    # LOW_FREQ = 10000
    # HIGH_FREQ = 20000

    for bit in binary_code:
        if bit == '0':
            play_tone(LOW_FREQ)
        elif bit == '1':
            play_tone(HIGH_FREQ)
        time.sleep(.1)  # Short pause between tones

# Main execution
# try:
#     while True:
#         '''Simulate Button Press'''
#         user_input = input("Enter a button call (LOW OXYGEN, SOMETHING'S WRONG, RISE NOW, BOAT): ")
#         if user_input.lower() == 'q':
#             break
#         if user_input not in button_map:
#             print("Please enter a valid Button.")
#             continue
#         freq = button_map[user_input]
#         play_tone(freq)
# finally:
#     p.terminate()
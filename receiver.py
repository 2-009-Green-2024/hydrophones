import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import warnings
import pyttsx3

CHUNK = 2**5  # bytes of data per chunk of the audio signal
RATE = 44100  # sample rate in kHz
LEN = 5  # length of msg. in seconds. will eventually need to switch to be continuous


def record_sound(chunk, rate, length):
    """
    Records sound data from laptop's internal
    microphone, then saves the recording to a
    continuous stream of audio data flattened from (points, chunk) to
    (points * chunk, 1) numpy array
    """
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    player = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )

    frames = []

    for i in range(int(LEN * RATE / CHUNK)):  # go for a LEN seconds
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        # player.write(data,CHUNK) NOTE this is for playing audio back real time
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # print("PLAYER DATA: ",player.read())
    print("FRAME DATA: ", frames)

    sound = np.asarray(frames)

    chunks, samples = np.shape(sound)
    amplitudes = np.reshape(sound, chunks * samples)
    times = np.linspace(0, LEN, chunks * samples, endpoint=True)

    print("AMPSHAPE: ", np.shape(sound))
    print("TSHAPES: ", np.shape(times))
    # plt.xlim((0,LEN))

    # plt.plot(times, amplitudes)
    # plt.show()

    return amplitudes


def fftPlot(sig, dt=None, plot=True):
    """
    plot/output the FFT of a signal given sound
    amplitude data
    """
    # Here it's assumes analytic signal (real signal...) - so only half of the axis is required

    if dt is None:
        dt = 1
        t = np.arange(0, sig.shape[-1])
        xLabel = "samples"
    else:
        t = np.arange(0, sig.shape[-1]) * dt
        xLabel = "freq [Hz]"

    if sig.shape[0] % 2 != 0:
        warnings.warn("signal preferred to be even in size, autoFixing it...")
        t = t[0:-1]
        sig = sig[0:-1]

    sigFFT = np.fft.fft(sig) / t.shape[0]  # Divided by size t for coherent magnitude

    freq = np.fft.fftfreq(t.shape[0], d=dt)

    # Plot analytic signal - right half of frequence axis needed only...
    firstNegInd = np.argmax(freq < 0)
    freqAxisPos = freq[0:firstNegInd]
    sigFFTPos = 2 * sigFFT[0:firstNegInd]  # *2 because of magnitude of analytic signal

    if plot:
        plt.figure()
        plt.plot(freqAxisPos, np.abs(sigFFTPos))
        plt.xlabel(xLabel)
        plt.ylabel("mag")
        plt.title("Analytic FFT plot")
        plt.show()

    return sigFFTPos, freqAxisPos


def interpret_messages(msg_freq):
    """
    given a message frequency, map that to
    an output message then play the audible output
    through the computer's microphones
    """
    message_dict = {
        (200, 299): "LOW OXYGEN",
        (300, 399): "SOMETHING'S WRONG",
        (100, 199): "RISE NOW",
        (500, 599): "BOAT",
    }

    for freq_range in message_dict.keys():
        low, high = freq_range

        if low <= msg_freq <= high:
            print("MESSAGE FOUND")
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.say(message_dict[freq_range])
            engine.runAndWait()


if __name__ == "__main__":
    dt = 1 / RATE

    signal = record_sound(CHUNK, RATE, LEN)
    # Result in frequencies
    sigFFTPos, freqAxisPos = fftPlot(signal, dt=dt, plot=False)
    msg_freq = freqAxisPos[np.argmax(sigFFTPos)]
    print(f"MESSAGE FREQUENCY IS {msg_freq} Hz")
    interpret_messages(msg_freq)
    # Result in samples (if the frequencies axis is unknown)
    # fftPlot(sig)

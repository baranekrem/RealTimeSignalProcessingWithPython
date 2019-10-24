#!/usr/bin/env python
# encoding: utf-8

## Module infomation ###
# Python (3.4.4)
# numpy (1.10.2)
# PyAudio (0.2.9)
# matplotlib (1.5.1)
# All 32bit edition
########################
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import Filter

filterState = 1

class SpectrumAnalyzer:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000
    CHUNK = 2048
    START = 0
    N = 2048

    R = 1000            # R Ohm
    C = 150e-9          # C Farad
    Ts = 1.0 / RATE     # sampling Frequency

    wave_x = 0
    wave_y = 0
    spec_x = 0
    spec_y = 0

    data = [0] * CHUNK
    filteredata = []

    myFilter = Filter.LowPassFilter(data, R, C, Ts)

    def __init__(self):
        self.pa = pyaudio.PyAudio()

        self.stream = self.pa.open(
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            output = False,
            frames_per_buffer = self.CHUNK)
        self.loop()

    def loop(self):
        try:
            while True :
                # Ses Alımı.
                self.data = self.stream.read(self.CHUNK)
                self.data = np.fromstring(self.data, np.float32)

                # Filtreleme.
                if filterState == 1:
                    self.filteredata = self.myFilter.FilterApply(self.data)
                    self.data = self.filteredata

                # FFT Alma.
                self.fft()

                # Grafiğe Çizme.
                self.graphplot()

        except KeyboardInterrupt:
            print("End...")

    def fft(self):
        self.wave_x = range(self.START, self.START + self.N)
        self.wave_y = self.data[self.START:self.START + self.N]
        self.spec_x = np.fft.fftfreq(self.N, d = 1.0 / self.RATE)
        y = np.fft.fft(self.data[self.START:self.START + self.N])
        self.spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in y]

    def graphplot(self):
        plt.clf()
        # wave
        plt.subplot(311)
        plt.plot(self.wave_x, self.wave_y)
        plt.axis([self.START, self.START + self.N, -1, 1])
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        #Spectrum
        plt.subplot(312)
        plt.plot(self.spec_x, self.spec_y, marker= '', linestyle='-')
        plt.axis([0, self.RATE / 2, 0, 50])
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude spectrum")
        #Pause
        plt.pause(.0001)

if __name__ == "__main__":
    spec = SpectrumAnalyzer()

from scipy import arctan, pi

class LowPassFilter(object):
    def __init__(self, x, R, C, period):
        self.__R = R
        self.__C = C
        self.__T = period
        self.__y = [0] * len(x)

        self.__K1 = (self.__T / (self.__T + 2 * self.__R * self.__C))
        self.__K2 = (self.__T / (self.__T + 2 * self.__R * self.__C))
        self.__K3 = ((self.__T - 2 * self.__R * self.__C) / (self.__T + 2 * self.__R * self.__C))

    def FilterApply(self, __x):
        for i in range(len(__x)):
            self.__y[i] = (__x[i] * self.__K1) + (__x[i - 1] * self.__K2) - (self.__y[i - 1] * self.__K3)
        return (self.__y)

    def GetFrequency(self):
        return (1 / (2 * pi * self.__R * self.__C))

    def GetWarping(self):
        return (2 / self.__T) * arctan(2 * pi * self.GetFrequency() * self.__T / 2) / (2 * pi)


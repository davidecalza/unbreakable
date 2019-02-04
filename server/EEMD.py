"""
Copyright (c) 2017 Fondazione Bruno Kessler
Author: Marco Roveri roveri@fbk.eu
See LICENSE.txt for licensing information
See CREDITS.txt for other credits
"""
from __future__ import print_function

import numpy as np

import logging


try:
    from scipy._lib.six import xrange
except ImportError:
    print("Failing to import xrange from scipy._lib.six")


class EEMD:

    def __init__(self):

        self.__logger = logging.getLogger('EEMD')
        # self.__logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.__logger.addHandler(ch)

        # Import libraries
        from EMD_main import EMD

        # Declare constants
        self.stdThreshold = 0.5
        self.scaledVarThreshold = 0.001
        self.powerThreshold = -5
        self.totalPowerThreshold = 0.01
        self.rangeThreshold = 0.001

        self.reduceScale = 1
        self.maxIteration = 20
        self.scaleFactor = 100

        # Ensemble constants
        self.noiseWidth = 0.3
        self.trials = 100

        self.EMD = EMD()
        self.EMD.FIXE_H = 5

    def getLogger(self):
        return self.__logger

    def getExtremaNo(self, S):
        d = np.diff(S)
        return np.sum(d[1:]*d[:-1]<0)

    def eemd(self, S, timeLine, maxImf=-1):

        N = len(S)
        E_IMF = np.zeros((1,N))
        E_TIME = np.zeros(1)
        E_ITER = np.zeros(1)


        for trial in xrange(self.trials):
            self.__logger.debug("trial: %s" % trial)

            noise = np.random.normal(loc=0, scale=self.noiseWidth, size=N)

            tmpIMF, tmpEXT, tmpITER, imfNo = self.emd(S+noise, timeLine, maxImf)

            while(E_IMF.shape[0] < imfNo):
                E_IMF = np.vstack((E_IMF, np.zeros(N)))
                E_ITER = np.append(E_ITER,0)

            for n in range(imfNo):
                E_IMF[n] += tmpIMF[n]
                E_ITER[n] += tmpITER[n]

        E_IMF /= self.trials
        E_EXT = np.array([self.getExtremaNo(E_IMF[n]) for n in range(E_IMF.shape[0])])

        return E_IMF, E_EXT, E_ITER, E_IMF.shape[0]

    def emd(self, S, timeLine, maxImf=-1):
        IMF, EXT, ITER, imfNo = self.EMD.emd(S, timeLine, maxImf)
        return IMF, EXT, ITER, imfNo

###################################################
## Beggining of program

if __name__ == "__main__":
    reduceScale = 1
    PLOT = 0
    INTERACTIVE = 1

    REPEATS = 1

    N = 500
    maxImf = -1

    t = timeLine = np.linspace(0, 2*np.pi, N)

    n = 2
    s1 = 3*np.sin(4*t)
    s2 = 4*np.sin(9*t)
    s3 = np.sin(11*t)
    S = np.sum( [-eval("s%i"%i) for i in range(1,1+n)], axis=0)

    S = np.random.normal(0,1, len(t))
    IMF, EXT, ITER, imfNo = EEMD().eemd(S, timeLine, maxImf)

    c = np.floor(np.sqrt(imfNo+3))
    r = np.ceil( (imfNo+3)/c)

    import pylab as py
    py.ioff()
    py.subplot(r,c,1)
    py.plot(timeLine, S, 'r')
    py.title("Original signal")

    py.subplot(r,c,2)
    py.plot([EXT[i] for i in xrange(imfNo)], 'o')
    py.title("Number of extrema")

    py.subplot(r,c,3)
    py.plot([ITER[i] for i in xrange(imfNo)], 'o')
    py.title("Number of iterations")

    def extF(s):
        state1 = np.r_[np.abs(s[1:-1]) > np.abs(s[:-2])]
        state2 = np.r_[np.abs(s[1:-1]) > np.abs(s[2:])]
        return np.arange(1,len(s)-1)[state1 & state2]

    for num in xrange(imfNo):
        py.subplot(r,c,num+4)
        py.plot(timeLine, IMF[num],'g')
        #~ py.plot(timeLine[extF(IMF[num])], IMF[num][extF(IMF[num])],'ok')
        py.title("Imf no " +str(num) )

    py.show()

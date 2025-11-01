import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.linalg import toeplitz
from scipy import linalg

filename = "e.wav"


samplerate, data = wavfile.read(filename)


def param_lpc(xs, P):
  autocorr = np.correlate(xs,xs,"full")/len(xs)
  R = toeplitz(autocorr[:(P-1)])
  r = autocorr[1:P]
  A = linalg.inv(R)*r.transpose()
  G = autocorr[0]
  for i in range(1,P):
    G -= A[i-1]*autocorr[i]
  return A,np.sqrt(G)

A, G = param_lpc(data,5)

print(A)
print(G)


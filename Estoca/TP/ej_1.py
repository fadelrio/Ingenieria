import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.linalg import toeplitz
from scipy import linalg

filename = "e.wav"


samplerate, data = wavfile.read(filename)


def param_lpc(xs, P):
  autocorr = np.correlate(xs,xs,"full")/len(xs)
  print(autocorr)
  R = toeplitz(autocorr[int(len(autocorr)/2):int(len(autocorr)/2+(P-1))])
  r = autocorr[int(len(autocorr)/2):int(len(autocorr)/2) + P]
  A = linalg.inv(R)*r.transpose()
  G = autocorr[int(len(autocorr)/2)]
  for i in range(1,P):
    G -= A[i-1]*autocorr[int(len(autocorr)/2) + i]
  return A,np.sqrt(G)

A, G = param_lpc(data,5)

print(A)
print(G)


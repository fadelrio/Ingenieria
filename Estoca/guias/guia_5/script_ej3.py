import numpy as np
import matplotlib.pyplot as plt

M = 1000

N = 10

a = .1

gamma = .98

sigma_v = 1/(1-a**2)

W = np.random.normal(0, 1, M)

V = np.empty_like(W)

for i in range(M):
	for j in range(N):
		V[i] += (a**j)*W[i-j]

#rezo xq esta sea la forma correcta de armar V

##para el punto 3
S = np.ones(N)

#FILTRO COMPLEMENTARIO
#
def filtro(x, s, Cv):
	o = np.dot(x,np.linalg.inv(Cv))
	return np.dot(o,s)

Cv = np.empty([N,N])

for i in range(N):
	for j in range(N):
		Cv[i,j] = a**(np.abs(j-i))


Cv = Cv*sigma_v

#ejercicio 3

s = np.ones(N)

S = np.pad(s,[int((M-N)/2),int((M-N)/2)], mode = 'constant', constant_values = 0)

X = V + np.pad(s,[int((M-N)/2),int((M-N)/2)], mode = 'constant', constant_values = 0)

gammap = np.log(gamma) + (1/2)*np.dot(np.dot(np.transpose(s),np.linalg.inv(Cv)),s)

x = np.lib.stride_tricks.sliding_window_view(X, N)

out = np.zeros_like(X)

for i in range(len(x)):
	if (filtro(x[i],s,Cv) >= gammap):
		np.put(out,np.arange(N) + i, x[i])

plt.figure()

plt.bar(np.arange(len(X)),X)

plt.bar(np.arange(M), S)

plt.figure()

plt.bar(np.arange(len(out)),out)

plt.bar(np.arange(M), X*S)

#ejercicio 4

M = 1001

N = 11

a = -.5

gamma = .99999


sigma_v = 1/(1-a**2)

W = np.random.normal(0, 1, M)

V = np.empty_like(W)

for i in range(M):
	for j in range(N):
		V[i] += (a**j)*W[i-j]


Cv = np.empty([N,N])

for i in range(N):
	for j in range(N):
		Cv[i,j] = a**(np.abs(j-i))

Cv = Cv*sigma_v

s_1 = np.array([1,1,1,-1,-1,-1,1,-1,-1,1,-1])

s_1 = 1*s_1

S_1 = np.pad(s_1,[int((M-N)/2),int((M-N)/2)], mode = 'constant', constant_values = 0)

X_1 = V + np.pad(s_1,[int((M-N)/2),int((M-N)/2)], mode = 'constant', constant_values = 0)

gammap = np.log(gamma) + (1/2)*np.dot(np.dot(np.transpose(s_1),np.linalg.inv(Cv)),s_1)

x_1 = np.lib.stride_tricks.sliding_window_view(X_1, N)

out = np.zeros_like(X_1)

for i in range(len(x_1)):
	if (filtro(x_1[i],s_1,Cv) >= gammap):
		np.put(out,np.arange(N) + i, x_1[i])



s = np.ones(N)

S = np.pad(s,[int((M-N)/2),int((M-N)/2)], mode = 'constant', constant_values = 0)

plt.figure()

plt.title("Ej4 sin filtro")

plt.bar(np.arange(len(X_1)),X_1)

plt.bar(np.arange(len(S_1)), S_1)

plt.figure()

plt.title("Ej 4 con filtro")

plt.bar(np.arange(len(out)),out)

plt.bar(np.arange(len(X_1*S)), X_1*S)

plt.show()





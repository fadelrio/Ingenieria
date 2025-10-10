import numpy as np
import matplotlib.pyplot as plt

N = 2000

X = np.random.normal(0, np.sqrt(20), N)

Y = np.random.normal(3, np.sqrt(20), N)

r_x = np.correlate(X, X, mode='full')
r_y = np.correlate(Y, Y, mode='full')

k = np.arange(-len(r_x)/2,(len(r_x)/2))

n_k = N - np.abs(k)

r_xi = r_x/n_k

r_yi = r_y/n_k

r_xs = np.correlate(X, X, mode='full')/N
r_ys = np.correlate(Y, Y, mode='full')/N

r_xi = r_x/n_k

r_yi = r_y/n_k
k = np.arange(-2000,1999)


plt.figure()
plt.plot(k,r_xi)
plt.ylim([-5,30])

plt.figure()
plt.plot(k,r_xs)
plt.ylim([-5,30])

plt.figure()
plt.plot(k,r_yi)
plt.ylim([-5,30])

plt.figure()
plt.plot(k,r_ys)
plt.ylim([-5,30])


plt.show()

#deberian dar deltas en cero montadas sobre las medias




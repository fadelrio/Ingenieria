import numpy as np


def interpolador(senal, largo, factor):
    salida = np.zeros(largo*factor)

    for i in range(0,largo):
        salida[i*(factor+1)] = senal[i]

    # print(salida)

    # for i in range(largo):
    #     m = (senal[i]-senal[i])/(ceros+1)
    #     for j in range(1,ceros+1):
    #         salida[i*(ceros)+j] = m*j + senal[i]

    return salida



senal = np.array([0,1,2,3,4,5,6,7,8,9])

print(interpolador(senal,10,4))



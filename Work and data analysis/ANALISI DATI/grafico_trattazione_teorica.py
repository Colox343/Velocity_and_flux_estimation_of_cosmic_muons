import matplotlib.pyplot as plt
import numpy as np

'''Questo programma stampa il grafico mostrato nella trattazione teorica sulla densità di probabilità di d_m'''

def func(x):
    return 1/(x**3*np.sqrt(x**2-1))

def main():
    begin = 1.01
    end = 2
    x_axis = np.linspace(begin,end,10**5)
    y_axis = []
    for x in x_axis:
        y_axis.append(func(x))

    plt.plot(x_axis,y_axis,color='blue')
    plt.xlabel("\u03BE")
    plt.ylabel("f(\u03BE)")

    plt.show()

if __name__ == "__main__":
    main()
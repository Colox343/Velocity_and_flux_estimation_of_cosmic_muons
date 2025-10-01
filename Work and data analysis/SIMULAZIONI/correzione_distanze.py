import numpy as np
from random import random
import matplotlib.pyplot as plt

def random_coord(delta_coord):
    return random()*delta_coord-delta_coord/2

def random_phi():
    return random()*2*np.pi

def random_theta():
    theta = random()*np.pi/2
    y = random()
    while (np.cos(theta))**2 < y:
        y = random()
        theta = random()*np.pi/2
    return theta

def main():
    delta_x = 30        #Dimensioni degli scintillatori in cm
    delta_y = 80
    d = 9.8              #Distanza tra gli scntillatori in cm. Modificare questo parametro per studiare più distanze
    N_max = 10**6       #Numero di eventi da raggiungere
    N_tot = 0           #Numero di muoni totali che passano
    data = []           #Distanze percorse dai muoni che passano per entrambi gli scntillatori


    '''Simulazione del passaggio dei muoni. Se una particella attraversa entrambi gli scntillatori
    viene memorizzata la distanza totale percorsa'''
    while len(data)<N_max:
        phi = random_phi()
        theta = random_theta()
        x1 = random_coord(delta_x)
        y1 = random_coord(delta_y)
        x2 = d*np.tan(theta)*np.cos(phi)+x1
        y2 = d*np.tan(theta)*np.sin(phi)+y1
        if np.abs(x2) < delta_x/2 and np.abs(y2) < delta_y/2:
            data.append(d/np.cos(theta))
        N_tot += 1
    
    #Calcolo della media e l'incertezza
    mean = 0
    stdv = 0
    stdv_mean = 0
    s = 0
    for i in range(N_max):      #Calcolo della media
        s += data[i]
    mean = s/N_max
    s = 0
    for i in range(N_max):
        s += (data[i]-mean)**2
    stdv = np.sqrt(s/(N_max-1))
    stdv_mean = stdv/np.sqrt(N_max)

    print("Rate muoni tenuti:",N_max/N_tot*100,"%\n")
    print("Distanza media:",mean,"cm\n")
    print("Deviazione standard:",stdv,"cm\n")
    print("Deviazione standard della media:",stdv_mean,"cm")

    #Generazione e stampa dell'istogramma
    N_bins = 100
    bin_edges = np.linspace(min(data),max(data))
    fig, ax = plt.subplots(ncols=1,nrows=1)
    plt.xlabel('distanza (cm)')
    plt.ylabel('conteggi')
    ax.hist(data,bins=bin_edges)

    entries = len(data)
    text_str = f"Entries: {entries}\nMean: {mean:.2f}\nStd Dev: {stdv:.2f}"
    plt.text(0.7,0.95,text_str,transform=plt.gca().transAxes,fontsize=12,verticalalignment='top',bbox=dict(facecolor='white',alpha=0.5))

    plt.show()

if __name__ == "__main__":
    main()
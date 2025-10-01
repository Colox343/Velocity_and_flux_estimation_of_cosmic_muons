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
    d = 9.8             #Distanza tra gli scntillatori in cm. Modificare questo parametro per studiare più distanze
    N_max = 10**6       #Numero di eventi da raggiungere
    N_tot = 0           #Numero di muoni totali che passano
    S1_x = []           #Coordinate attraversate dai muoni attraverso gli scintillatori S1 ed S2
    S1_y = []
    S2_x = []
    S2_y = []


    '''Simulazione del passaggio dei muoni. Se una particella attraversa entrambi gli scntillatori
    vengono memorizzate le sue coordinate su di essi'''
    while N_tot<N_max:
        phi = random_phi()
        theta = random_theta()
        x1 = random_coord(delta_x)
        y1 = random_coord(delta_y)
        x2 = d*np.tan(theta)*np.cos(phi)+x1
        y2 = d*np.tan(theta)*np.sin(phi)+y1
        if np.abs(x2) < delta_x/2 and np.abs(y2) < delta_y/2:
            S1_x.append(x1)
            S1_y.append(y1)
            S2_x.append(x2)
            S2_y.append(y2)
            N_tot += 1
            if(N_tot%(N_max*0.05) == 0):
                print(N_tot/N_max*100,"%\n")
    
    #Generazione e stampa degli istogrammi
    L_bins = 1
    N_bins = [int(delta_x/L_bins),int(delta_y/L_bins)]
    fig, ax = plt.subplots(nrows=1,ncols=2)
    ax[0].set_title("Muoni incidenti su S1")
    ax[1].set_title("Muoni incidenti su S2")
    ax[0].hist2d(S1_x,S1_y,bins=N_bins)
    ax[1].hist2d(S2_x,S2_y,bins=N_bins)
    plt.show()

if __name__ == "__main__":
    main()
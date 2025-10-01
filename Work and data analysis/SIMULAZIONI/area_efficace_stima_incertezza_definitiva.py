import numpy as np
from random import random

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

def random_correction_factor(delta_x,delta_y,d,N_max):
    N_muons = 0         #Numero di muoni che passano per entrambi gli scntillatori
    N_tot = 0           #Numero di muoni totali generati

    '''Simulazione del passaggio dei muoni. Se una particella attraversa entrambi gli scntillatori
    vengono memorizzate le sue coordinate su di essi'''
    while N_muons<N_max:
        phi = random_phi()
        theta = random_theta()
        x1 = random_coord(delta_x)
        y1 = random_coord(delta_y)        
        y2 = y1+d*np.tan(theta)*np.sin(phi)
        x2 = x1+d*np.tan(theta)*np.cos(phi)

        N_tot += 1
        if np.abs(x2) < delta_x/2 and np.abs(y2) < delta_y/2:
            N_muons += 1
    return N_muons/N_tot

def main():
    delta_x = 30        #Dimensioni degli scintillatori in cm
    delta_y = 80
    d = 21              #Distanza tra gli scntillatori in cm. Modificare questo parametro per studiare più distanze
    N_max = 10**6       #Numero di eventi da raggiungere
    N_factors = 5               #Numero di fattori di correzione da generare
    correction_factors = []     #Fattori di correzione memorizzati
    file_name = "risultati.txt"     #File in cui vengono salvati i risultati. Assicurarsi che sia presente in cartella

    for i in range(N_factors):
        correction_factors.append(random_correction_factor(delta_x,delta_y,d,N_max))
        print((i+1)/N_factors*100,"%",end="\r")

    #Calcolo della media
    mean = 0
    for i in range(N_factors):
        mean += correction_factors[i]
    mean = mean/N_factors

    #Calcolo dell'incertezza
    sum = 0
    for i in range(N_factors):
        sum += (correction_factors[i]-mean)**2
    stdv = np.sqrt(sum/(N_factors-1))
    stdv_mean = stdv/np.sqrt(N_factors)

    #Stampa dei risultati
    print("Fattore di correzione area medio:",mean)
    print("Deviazione standard:",stdv)
    print("Deviazione standard della media:",stdv_mean)

    #Stampa dei risultati sul file
    try:
        f = open(file_name, "a")
        f.write("Angolo utilizzato: "+str(alpha*180/np.pi)+" gradi\n")
        f.write("Fattore di correzione area medio: "+str(mean)+"\n")
        f.write("Deviazione standard: "+str(stdv)+"\n")
        f.write("Deviazione standard della media: "+str(stdv_mean)+"\n\n")
        f.close()
    except:
        print("\nImpossibile scrivere il file")

if __name__ == "__main__":
    main()
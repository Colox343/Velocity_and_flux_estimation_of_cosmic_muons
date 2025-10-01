import matplotlib.pyplot as plt
import numpy as np

'''Questo programma importa i dati provenienti dall'ADC e dalla TDC e genera due grafici dei tempi in funzione delle 
ampiezze del segnale (uno per adc1 e uno per adc2). Il grafico contiene le medie dei tempi associati a ogni bin di 
un istogramma, che sono associate ai centri dei relativi intervalli.'''

# Leggi il file e conserva solo la terza e la quarta colonna
def processa_file(nome_file):
    # Carica il file, considera che i valori sono separati da spazi o tab
    dati = np.loadtxt(nome_file)
    
    # Estrai 
    dati_filtrati = dati[:, [0,1,2]]
    
    # Elimina righe con tutti zeri
    #dati_filtrati = dati_filtrati[~np.all(dati_filtrati == 0, axis=1)]
    dati_filtrati = dati_filtrati[~((dati_filtrati[:, 1] == 0) & (dati_filtrati[:, 2] == 0))]
    
    return dati_filtrati

def crea_grafico(x,y,title,xlabel,ylabel):
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()

def crea_grafico_scatterato(x,y,title,xlabel,ylabel):
    plt.scatter(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()

#Questa funzione genera un grafico con le medie dei valori di y per ogni intevrallo di x
def crea_grafico_medie(x,y,title,xlabel,ylabel,n_edges=100):
    #Creazione degli array ordinati
    sorted_indices = np.argsort(x)
    y1 = np.array(y)[sorted_indices]
    x.sort()
    
    #Generazione dei bordi
    bin_edges = np.linspace(min(x),max(x),n_edges)
    amp = []
    means = []

    #Calcolo delle medie degli intervalli
    for i in range(n_edges-1):
        n = 0
        mean = 0
        for j in range(len(x)):
            if x[j] >= bin_edges[i] and x[j] < bin_edges[i+1]:
                mean += y1[j]
                n += 1
        if n != 0:
            amp.append((bin_edges[i]+bin_edges[i+1])/2)  
            mean /= n
            means.append(mean)
    
    #Stampa dei risultati
    plt.plot(amp,means)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()

def main():
    nome_file = "Dati_tdcadc5.txt"
    data = processa_file(nome_file)
    times = []
    adc1 = []
    adc2 = []
    A = 2.06
    B = 0.0916
    n_edges = 100

    #Creazione garfico per S1
    for row in data:
        times.append(A+B*row[0])
        adc1.append(row[1])
        adc2.append(row[2])

    crea_grafico_medie(adc1,times,"Tempi in funzione delle ampiezze del segnale S1","Ampiezze (ADC)","Tempi (ns)",n_edges)

    #Creazione garfico per S2
    crea_grafico_medie(adc2,times,"Tempi in funzione delle ampiezze del segnale S2","Ampiezze (ADC)","Tempi (ns)",n_edges)
    

if __name__ == "__main__":
    main()
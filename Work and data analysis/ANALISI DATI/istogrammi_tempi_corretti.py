import numpy as np
import matplotlib.pyplot as plt


def processa_file(nome_file):
    # Carica il file, considera che i valori sono separati da spazi o tab
    dati = np.loadtxt(nome_file)
    
    # Estrai 
    dati_filtrati = dati[:, [0,1]]
    
    # Elimina righe con tutti zeri
    #dati_filtrati = dati_filtrati[~np.all(dati_filtrati == 0, axis=1)]
    dati_filtrati = dati_filtrati[~((dati_filtrati[:, 1] == 0) & (dati_filtrati[:, 1] == 0))]
    
    return dati_filtrati





def main():
    nome_file='Tempi_corretti5.txt'
    data = processa_file(nome_file)
    T=[]
    for row in data:
        T.append(row[0])

    plt.hist(T, 40)
    plt.show()





if __name__ == "__main__":
    main()

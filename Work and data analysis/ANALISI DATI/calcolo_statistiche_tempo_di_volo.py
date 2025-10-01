import numpy as np

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

def main():
    f = open("risultati_tempi_misurati_in_ns.txt","w")
    A = 2.06
    B = 0.0916
    stdv_A = 0.31
    stdv_B = 0.0014
    for i in range(1,6):
        #import dei dati dai file
        nome_file = "Dati_tdcadc"+str(i)+".txt"
        data = processa_file(nome_file)
        times = []
        stdvs = []
        for row in data:
            times.append(row[0])
            stdvs.append(np.sqrt(stdv_A**2+(row[0]*stdv_B)**2))
        #Calcolo della media e dell'incertezza con una media pesata
        s_stdv = 0
        s = 0
        for j in range(len(times)):
            s_stdv += 1/(stdvs[j]**2)
            s += times[i]/(stdvs[j]**2)
        mean = s/len(times)
        stdv = 1/np.sqrt(s_stdv)

        print("Data set",i,":")
        print("Valore d'aspettazione:",mean,"ns")
        print("Incertezza:",stdv,"ns\n\n")

        f.write(str(mean)+" ")
        f.write(str(stdv)+"\n")

    f.close()

if __name__ == "__main__":
    main()
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

def medie(f):
    data=processa_file(f)
    A=[]
    s=[]
    R=[]
    for row in data:
        A.append(row[0])
        s.append(row[1])
    somma=sum(A)
    media=somma/len(A)
    R.append(media)
    S=sum(s)/len(s)
    sigma=S/np.sqrt(len(A))
    R.append(sigma)
    return R



def main():
    nome_file1 = "Tempi_corretti1.txt"   
    nome_file2 = "Tempi_corretti1.txt" 
    nome_file4 = "Tempi_corretti1.txt" 
    nome_file5 = "Tempi_corretti1.txt" 
    X=[]
    Xerr=[]
    for i in range(4):
        if i==0:
            K=medie(nome_file1)
            X.append(K[0])
            Xerr.append(K[1])
        elif i==1:
            K=medie(nome_file2)
            X.append(K[0])
            Xerr.append(K[1])
        elif i==2:
            K=medie(nome_file4)
            X.append(K[0])
            Xerr.append(K[1])
        elif i==3:
            K=medie(nome_file5)
            X.append(K[0])
            Xerr.append(K[1])
    M=[1,2,3,4]
    print(X, '\n', Xerr)
    plt.errorbar(M, X, Xerr, color='blue', fmt='o')
    plt.show()


if __name__ == "__main__":
    main()








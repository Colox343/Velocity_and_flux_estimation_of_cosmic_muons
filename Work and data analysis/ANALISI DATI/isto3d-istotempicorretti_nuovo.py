import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from hist import Hist
import scipy
from iminuit import Minuit
from scipy.stats import chi2
from iminuit.cost import LeastSquares


'''Inizialmente avevamo provato a stimare il valore di Vs tramite i minimi quadrati. Quello che abbiamo ottenuto è stato
Vs1 = 2.5 e Vs2 = 3.8, quindi abbiamo selezionato un Vs uguale alla loro media Vs = (Vs1+Vs2)/2 con incertezza uguale alla deviazione
standard della media'''

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

def modello1(x, A, tau):        #Modello per la stima dei parametri di S1
    return(A-tau*np.log(x/(x-3.15)))

def modello2(x, A, tau):        #Modello per la stima dei parametri di S2
    return(A+tau*np.log(x/(x-3.15)))

def correzione(tN, x1, f):
    t=[]
    for  i in range(len (tN)):
        t.append(2.06*tN[i]+0.0916)
    means_result = scipy.stats.binned_statistic(x1, t, bins=200, range=(min(x1), max(x1)), statistic='mean')
    std_result = scipy.stats.binned_statistic(x1, t, bins=200, range=(min(x1), max(x1)), statistic='std')
    means = means_result.statistic
    var = std_result.statistic
    bin_edges = means_result.bin_edges

    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.


    X=[]
    Y=[]
    Yerr=[]
    for i in range(len(means)):
        if var[i]!=0 and bin_centers[i]>0 and bin_centers[i]<100:        #means[i+1]+var[i+1])>means[i] and
            X.append(bin_centers[i])
            Y.append(means[i])
            Yerr.append(var[i])
    least_squares = LeastSquares (X, Y, Yerr, f)
    my_minuit = Minuit (least_squares, A=0, tau=1*10**(-9))

    #Impostazione dei constraint per i valori dei parametri
    #my_minuit.limits['Vs'] = (0,min(X)-0.01)
    my_minuit.limits['tau'] = (-1e-9,1e-9)
    my_minuit.limits['A'] = (100,1000)

    my_minuit.migrad ()  # finds minimum of least_squares function
    my_minuit.hesse ()
    print(my_minuit.values)
    print(my_minuit.errors)
    return my_minuit.values

# Conta le occorrenze di ogni numero in un array (attualemnte inutile)
def conta_occorrenze(colonna):
    valori, conteggi = np.unique(colonna, return_counts=True)
    return valori, conteggi

# Crea i grafici
def crea_grafici(x1, x2, t):
    #crea l'istogramma 2d
    plt.hist2d(x1,x2, bins=45, range=[[0, 200],[0,400]])
    plt.colorbar(label='counts')    
    plt.show()
    # da 37 a 100
    hist, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])
    hist2, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])
    hist3, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])
    max=0
    print(hist[1][1])
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            if max< hist[i][j]:
                max=hist[i][j]
    print(max)
    tagli=max/10
    #sezione che taglia l'istogramma centrandosi al picco e mantenendo arbitrari 
    # valori ad ogni lato
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            if hist[i][j]==max:
                k=i
                kk=j
    z=max
    m=1
    beta=k
    while(z>tagli):
        beta=beta+1
        z=hist[beta][kk]
        if z<tagli:
            beta=beta+2
            for i in range(len(hist[0])-beta):
                    for j in range(len(hist[0])):
                        hist[beta+i][j]=0

    z=max
    beta=k-1
    while(z>tagli):
        beta=beta-1
        z=hist[beta][kk]
        if z<tagli:
            beta=beta-2
            for i in range(beta):
                    for j in range(len(hist[0])):
                        hist[i][j]=0
    z=max
    beta=kk
    while(z>tagli):
        beta=beta+1
        z=hist[k][beta]
        if z<tagli:
            beta=beta+2
            for i in range(len(hist[0])-beta):
                    for j in range(len(hist[0])):
                        hist[j][beta+i]=0

    z=max
    beta=kk
    while(z>tagli):
        beta=beta-1
        z=hist[k][beta]
        if z<tagli:
            for i in range(beta):
                    for j in range(len(hist[0])):
                        hist[j][i]=0
    
    plt.imshow(hist)
    plt.show()
    
    prova=False
    i=0
    j=0
    Quadrox=[]
    Quadroy=[]
    #sezione che serve a recuperare sulla base della matrice dei dati originari
    #  i valori che fanno parte della sezione tenuta in considerazione
    for O in range (len(hist)):
        for P in range(len (hist)):
            hist2[O][P]=hist[O][P]
            hist3[O][P]=hist[O][P]


    while(prova==False):
        if hist[i][j]!=0:
            for seg in range(len(hist[0])):
                    if hist[i][seg]!=0:
                        Quadroy.append(yedges[seg+1])
                    if hist[seg][j]!=0:
                        Quadrox.append(xedges[seg+1])
            prova=True
        i=i+1
        if i==44:
             i=0
             j=j+1
    tveri=[]
    Cor=[]
    Cor2=[]
    Cor=correzione(t,x1,f=modello1)
    Cor2=correzione(t,x2,f=modello2)
    tau1=float(Cor[1])
    tau2=float(Cor2[1])
    #Vs1=float(Cor[2])
    #Vs2=float(Cor2[2])
    Vs1 = 3.15
    Vs2 = 3.15


    print(len(xedges))
    for i in range(len(t)):
        if x1[i]< np.amax((Quadrox)):
            if x1[i]>np.amin(Quadrox):
                if x2[i]<np.amax(Quadroy):
                    if x2[i]>np.amin(Quadroy):
                        tveri.append((2.06*t[i]+0.0916)-tau2*np.log(x2[i]/(x2[i]-Vs2))+tau1*np.log(x1[i]/(x1[i]-Vs1)))
    plt.hist(tveri, bins=40)
    plt.show()


# Nome del file
nome_file = "dati_tdcadc2.txt"


# Esegui il processo
try:
    dati = processa_file(nome_file)
    t=[]
    x1=[]
    x2=[]
    for i in range(len(dati)):
        t.append(dati[i, 0])
        x1.append(dati[i, 1])
        x2.append(dati[i, 2])
    
    

    # Crea i grafici
    crea_grafici( x1, x2, t)

    print(len(x1))
except Exception as e:
    print(f"Errore durante l'elaborazione: {e}")
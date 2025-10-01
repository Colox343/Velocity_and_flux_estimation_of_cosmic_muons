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

def modello(x, A, tau, Vs1):
    #Vs1=75 millivolt
    return(A-tau*np.log(x/(x-Vs1)))

def correzione(t, x2, x1):
    
    means_result = scipy.stats.binned_statistic(x1, t, bins=200, range=(min(x2), max(x2)), statistic='mean')
    std_result = scipy.stats.binned_statistic(x1, t, bins=200, range=(min(x2), max(x2)), statistic='std')
    means = means_result.statistic
    means2 = means_result.statistic
    var = std_result.statistic
    bin_edges = means_result.bin_edges

    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.

    plt.errorbar(x=bin_centers, y=means, yerr=var, linestyle='none', marker='.')
    plt.show()
    X=[]
    Y=[]
    Yerr=[]
    prova=False
    i=0
    X.append(float(bin_centers[0]))
    Y.append(float(means[0]))
    Yerr.append(float(var[0]))
    while(prova==False):
        if (means[i+1]+var[i+1])>means[i] and var[i+1]!=0 and bin_centers[i]>50:
            X.append(bin_centers[i+1])
            Y.append(means[i+1])
            Yerr.append(var[i+1])
            print('ok')
            i=i+1
        elif((means[i+1]+var[i+1])>means[i] and var[i+1]!=0 and bin_centers[i]<0):
            i=i+1
        else:
            prova=True
    least_squares = LeastSquares (X, Y, Yerr, modello)
    my_minuit = Minuit (least_squares, A=0, tau=1*10**(-9), Vs1=1)
    #my_minuit.limits = {'A':None,'tau':(0,None),'Vs1':(0,min(X))}
    my_minuit.limits['Vs1'] = (0,min(X)-0.001)

    my_minuit.migrad ()  # finds minimum of least_squares function
    my_minuit.hesse ()
    print(my_minuit.values)
    A=float(my_minuit.values[0])
    tau=float(my_minuit.values[1])
    Vs1=float(my_minuit.values[2])
    return my_minuit.values

# Conta le occorrenze di ogni numero in un array (attualemnte inutile)
def conta_occorrenze(colonna):
    valori, conteggi = np.unique(colonna, return_counts=True)
    return valori, conteggi

# Crea i grafici
def crea_grafici( x1, x2, t):
    #crea l'istogramma 2d
    plt.hist2d(x1,x2, bins=45, range=[[0, 200],[0,400]])
    plt.colorbar(label='counts')    
    plt.show()
    # da 37 a 100
    hist, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])
    hist2, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])
    hist3, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])
    print(hist)
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
    print('ciao',Quadrox, '\n', Quadroy, 'ciao')
    print('si')
    tveri=[]
    MM=-1
    X=[]
    Y=[]
    
    print(len(xedges))
    for i in range(len(t)):
        if x1[i]< np.amax((Quadrox)):
            if x1[i]>np.amin(Quadrox):
                if x2[i]<np.amax(Quadroy):
                    if x2[i]>np.amin(Quadroy):
                        #tveri.append((2.06*t[i]+0.0916)-tau2*np.log(x2[i]/(x2[i]-Vs2))+tau1*np.log(x1[i]/(x1[i]-Vs1)))
                        tveri.append((2.06*t[i]+0.0916))
                        X.append(x1[i])
                        Y.append(x2[i])
                        #tutto questo blocco serve a vedere quali dati fanno l'ultima colonna
                        #non servono davvero nell'analisi
                        #MM=MM+1
                        #if tveri[MM]>=(2.06*150+0.0916) and tveri[MM]<=(2.06*154+0.0916):
                            # for N in range(len(hist)):
                                  #print('prova cose:', xedges[N], '\n', xedges[N+1], '\n', x1[i])
                                  #if x1[i]>xedges[N] and x1[i]<xedges[N+1]:
                                   # print('prova cose:', xedges[i], '\n', xedges[i+1], '\n', x1[N])
                                    #for j in range(len(hist)):
                                      # if x2[i]>yedges[j] and x2[i]<yedges[j+1]:
                                          # print('prova cose:', hist2[i][j])
                                           #hist2[N][j]=hist2[N][j]-1
                                           #print('prova cose:', hist2[i][j])
   # for i in range(len(tveri)):
     #   tveri[i]=(2.06*t[i]+0.0916)-tau2*np.log(V2/(V2-Vs2))+tau1*np.log(V1/(V1-Vs1))
    
    #for i in range (len(hist)):
    #    for j in range(len (hist)):
    #        hist3[i][j]=hist[i][j]-hist2[i][j]
    #plt.imshow(hist3)
    #plt.show()
    #print(tveri)
    Cor=[]
    Cor2=[]
    Cor=correzione(tveri, X, Y)
    Cor2=correzione(tveri, X, Y)
    tau1=float(Cor[1])
    tau2=float(Cor2[1])
    Vs1=float(Cor[2])
    Vs2=float(Cor2[2])
    print(Cor, '\n', Cor2, '\n')
    for i in range(len(tveri)):
        tveri[i]=(tveri[i]-tau2*np.log(x2[i]/(x2[i]-Vs2))+tau1*np.log(x1[i]/(x1[i]-Vs1)))
    print("Massimo e minimo:",float(np.amin(Quadrox)),float(np.amax(Quadrox)))
    print("Massimo e minimo:",float(np.amin(Quadroy)),float(np.amax(Quadroy)))
    for i in range (len(tveri)):
        if tveri[i]==np.inf or tveri[i]==-np.inf:
            #print('cazzi')
            #print(tveri[i])
            A=A
    #print(xedges)
    plt.hist(tveri, bins=40)
    print('ciao')
    plt.show()
    print('questo:', Cor)
    

             
             




    # array per ancorare le colonne nello spazio 3d
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    ## array per dividere le colonne
    #dx = dy = 0.5 * np.ones_like(zpos) (creava colonne separate tra loro)
    dx = np.diff(xedges)[0]  # La larghezza di un bin lungo l'asse x
    dy = np.diff(yedges)[0]  # La profondità di un bin lungo l'asse y
    dz = hist.flatten()
    print(dz, dx, dy)

    #normalizza sulle z così che cambino i colori dei bin in base all'altezza
    norm = Normalize(vmin=dz.min(), vmax=dz.max())
    colors = cm.viridis(norm(dz))  # Usa il colormap 'viridis'


    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d( x=xpos,y=ypos, z=zpos, dx=dx, dy=dy, dz=dz, zsort='average', color=colors)

    plt.show()

# Nome del file
nome_file = "dati_tdcadc4.txt"


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









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
    dati_filtrati = dati_filtrati[~np.isnan(dati_filtrati).any(axis=1)]  # Rimuove le righe contenenti NaN
    dati_filtrati = dati_filtrati[~np.isinf(dati_filtrati).any(axis=1)]  # Rimuove le righe contenenti infiniti

    return dati_filtrati

def modello(x, A, tau, Vs1):
    #Vs1=75 millivolt
    return(A-tau*np.log(x/(x-Vs1)))


nome_file = "dati_tdcadc2.txt"
try:
    dati = processa_file(nome_file)
    tN=[]
    x1=[]
    x2=[]
    for i in range(len(dati)):
        tN.append(dati[i, 0])
        x1.append(dati[i, 1])
        x2.append(dati[i, 2])


    t=[]
    for i in range(len (tN)):
        t.append(2.06*tN[i]+0.0916)
    means_result = scipy.stats.binned_statistic(x1, t, bins=200, range=(min(x2), max(x2)), statistic='mean')
    std_result = scipy.stats.binned_statistic(x1, t, bins=200, range=(min(x2), max(x2)), statistic='std')
    means = means_result.statistic
    means2 = means_result.statistic
    var = std_result.statistic
    bin_edges = means_result.bin_edges

    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.

    '''plt.errorbar(x=bin_centers, y=means, yerr=var, linestyle='none', marker='.')
    plt.show()'''
    X=[]
    Y=[]
    Yerr=[]
    prova=False
    i=0
    #X.append(float(bin_centers[0]))
    #Y.append(float(means[0]))
    #Yerr.append(float(var[0]))
    while(prova==False):
        if (means[i+1]+var[i+1])>means[i] and var[i+1]!=0 and bin_centers[i]>50:
        #if (means[i+1]+var[i+1])>means[i] and var[i+1]!=0:
            print('ciao')
            X.append(bin_centers[i+1])
            Y.append(means[i+1])
            Yerr.append(var[i+1])
            i=i+1
        elif(means[i+1]+var[i+1])>means[i] and var[i+1]!=0 and bin_centers[i]<50:
            if(bin_centers[i+1]>=50):
                X.append(float(bin_centers[i+1]))
                Y.append(float(means[i+1]))
                Yerr.append(float(var[i+1]))
            i=i+1
            print('ciaone')
        else:
            prova=True
    print(X)
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

    fig, ax = plt.subplots ()
    plt.errorbar(X, Y, Yerr, ls='', fmt='.', color='blue')
    x_coord=np.linspace(Vs1+1, Vs1+250, 1000)
    y_coord=modello(x_coord, A, tau, Vs1)
    plt.plot(x_coord, y_coord, color='red')
    ax.set_title ('linear model', size=12)
    ax.set_xlabel ('x')
    ax.set_ylabel ('y')
    plt.grid=True
    
    plt.show()

    
    
       # accurately computes uncertainties
    # NB: adding additional instructions prevents the automatic visualisation of the fit result

        









    
    

    
except Exception as e:
    print(f"Errore durante l'elaborazione: {e}")
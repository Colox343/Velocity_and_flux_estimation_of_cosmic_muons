import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D

# Leggi il file e conserva solo la terza e la quarta colonna
def processa_file(nome_file):
    # Carica il file, considera che i valori sono separati da spazi o tab
    dati = np.loadtxt(nome_file)
    
    # Estrai 
    dati_filtrati = dati[:, [0,1,2]]
    
    # Elimina righe con tutti zeri
    dati_filtrati = dati_filtrati[~np.all(dati_filtrati == 0, axis=1)]
    
    return dati_filtrati

# Conta le occorrenze di ogni numero in un array (attualemnte inutile)
def conta_occorrenze(colonna):
    valori, conteggi = np.unique(colonna, return_counts=True)
    return valori, conteggi

# Crea i grafici
def crea_grafici( x1, x2):
    #crea l'istogramma 2d
    plt.hist2d(x1,x2, bins=45, range=[[0, 200],[0,400]])
    plt.colorbar(label='counts')    
    plt.show()

    hist, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])

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
nome_file = "dati_tdcadc3.txt"


# Esegui il processo
try:
    dati = processa_file(nome_file)
    y=[]
    x1=[]
    x2=[]
    for i in range(10000):
        x1.append(dati[i, 1])
        x2.append(dati[i, 2])
    
    

    # Crea i grafici
    crea_grafici( x1, x2)
    print(len(x1))
except Exception as e:
    print(f"Errore durante l'elaborazione: {e}")









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
    #dati_filtrati = dati_filtrati[~np.all(dati_filtrati == 0, axis=1)]
    dati_filtrati = dati_filtrati[~((dati_filtrati[:, 1] == 0) & (dati_filtrati[:, 2] == 0))]
    
    return dati_filtrati

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
    hist4, xedges, yedges = np.histogram2d(x1, x2, bins=45, range=[[0, 200], [0, 400]])

    for i in range(len(hist)):
         for j in range(len(hist[0])):
              hist2[i][j]=hist[i][j]

    for i in range(len(hist)):
         for j in range(len(hist[0])):
              hist3[i][j]=hist[i][j]
    max=0
    print(hist[1][1])
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            if max< hist[i][j]:
                max=hist[i][j]
    print(max)
    tagli=max/10
    
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
    tveri1=[]
    for i in range(len(t)):
        if x1[i]< np.amax((Quadrox)):
            if x1[i]>np.amin(Quadrox):
                if x2[i]<np.amax(Quadroy):
                    if x2[i]>np.amin(Quadroy):
                        tveri1.append(float(t[i]))
    print(tveri1)
    print("Massimo e minimo:",float(np.amin(Quadrox)),float(np.amax(Quadrox)))
    print("Massimo e minimo:",float(np.amin(Quadroy)),float(np.amax(Quadroy)))
    print(xedges)
    plt.hist(tveri1, bins=40)
    plt.show()


    for i in range(len(hist)):
         for j in range(len(hist[0])):
              hist4[i][j]=hist[i][j]




    #secondo taglio

    for i in range(len(hist[0])):
         hist2[0][i]=0
    plt.imshow(hist2)
    plt.show()
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            hist[i][j]=hist2[i][j]-hist[i][j]

    max=0
    print(hist[1][1])
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            if max< hist[i][j]:
                max=hist[i][j]
    print(max)
    tagli=max/10
    
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
    print('ok')
    prova=False
    i=0
    j=0
    Quadrox=[]
    Quadroy=[]
    print(hist)
    plt.imshow(hist)
    plt.show()
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
    i=0
    j=0
    print('ciao',Quadrox, '\n', Quadroy, 'ciao')
    tveri=[]
    print("Massimo e minimo:",float(np.amin(Quadrox)),float(np.amax(Quadrox)))
    print("Massimo e minimo:",float(np.amin(Quadroy)),float(np.amax(Quadroy)))
    #print(float(np.sort(x2.astype('f'))))
    #x1[10]=np.float(20)
    #x2[10]=np.float(220)
    plt.imshow(hist2)
    plt.show()
    for i in range(len(t)):
        if i==1000:
             print('ok')
        if x1[i]< np.amax(Quadrox):
            if x1[i]>np.amin(Quadrox):
                if x2[i]<np.amax(Quadroy):
                    if x2[i]>np.amin(Quadroy):
                        tveri.append(float(t[i]))
    print(len(tveri))
    print(len(t))
    plt.hist(tveri, bins=40)
    plt.show()


    #terzo taglio
    plt.imshow(hist)
    plt.show()

    for i in range(len(hist)):
         for j in range(len(hist[0])):
            hist[i][j]=hist2[i][j]-hist[i][j]-hist4[i][j]

    #for i in range(len(hist)):
     #    for j in range(len(hist[0])):
      #      hist[i][j]=0
    #for i in range(len(hist)):
     #   for j in range(len(hist[0])):
      #      if float(x1[i])< 82.0:
       #         if float(x1[i])>33.0:
        #            if float(x2[j])<87.0:
         #               if float(x2[j])>39.0:
          #                  hist[i][j]=hist2[i][j]
    plt.imshow(hist)
    plt.show()


    max=0
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            if max< hist[i][j]:
                max=hist[i][j]
    print(max)
    tagli=max/10
    
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
    print('ok')
    prova=False
    i=0
    j=0
    Quadrox=[]
    Quadroy=[]
    print(hist)
    plt.imshow(hist)
    plt.show()
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
    i=0
    j=0
    print('ciao',Quadrox, '\n', Quadroy, 'ciao')
    tverin=[]
    print("Massimo e minimo:",float(np.amin(Quadrox)),float(np.amax(Quadrox)))
    print("Massimo e minimo:",float(np.amin(Quadroy)),float(np.amax(Quadroy)))
    #print(float(np.sort(x2.astype('f'))))
    #x1[10]=np.float(20)
    #x2[10]=np.float(220)
    for i in range(len(t)):
        if i==1000:
             print('ok')
        if x1[i]< np.amax(Quadrox):
            if x1[i]>np.amin(Quadrox):
                if x2[i]<np.amax(Quadroy):
                    if x2[i]>np.amin(Quadroy):
                        tverin.append(float(t[i]))
    print(len(tveri))
    print(len(t))
    plt.hist(tverin, bins=40)
    plt.show()

    plt.hist(tveri1, bins=40, color='red')
    plt.hist(tveri, bins=40, color='green')
    plt.hist(tverin, bins=40, color='pink')
    plt.show()
             
             




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









import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares

def processa_file(nome_file):
    # Carica il file, considera che i valori sono separati da spazi o tab
    dati = np.loadtxt(nome_file)
    
    # Estrai 
    dati_filtrati = dati[:, [0,1]]
    
    # Elimina righe con tutti zeri
    #dati_filtrati = dati_filtrati[~np.all(dati_filtrati == 0, axis=1)]
    dati_filtrati = dati_filtrati[~((dati_filtrati[:, 1] == 0) & (dati_filtrati[:, 1] == 0))]
    
    return dati_filtrati

def line_model(x,m):
    return m*x

#Funzione che stima i parametri m e q per un fit lineare y = mx
def fit_lineare(x_coord,sigma_x,y_coord,sigma_y):
    # generate a least-squares cost function
    least_squares = LeastSquares (x_coord, y_coord, sigma_y, line_model)
    my_minuit = Minuit (least_squares, m = 1)  # starting values for m
    my_minuit.migrad ()  # finds minimum of least_squares function
    my_minuit.hesse ()   # accurately computes uncertainties

     # Estrazione dei risultati
    m_fit = my_minuit.values['m']
    m_err = my_minuit.errors['m']
    chi2_value = my_minuit.fval

    return [m_fit,m_err,chi2_value]

def medie(f):
    data=processa_file(f)
    A=[]
    s=[]
    R=[]
    for row in data:
        A.append(row[0])
        s.append(row[1])
    somma = 0
    somma_sigma = 0
    for i in range(len(A)):
        somma += A[i]/(s[i]**2)
        somma_sigma += 1/(s[i]**2)
    media=somma/somma_sigma
    R.append(media)
    sigma=1/np.sqrt(somma_sigma)
    R.append(sigma)
    return R


def main():
    nome_file1 = "Tempi_corretti1.txt"   
    nome_file2 = "Tempi_corretti2.txt" 
    nome_file4 = "Tempi_corretti4.txt" 
    nome_file5 = "Tempi_corretti5.txt"
    nomi =[nome_file1,nome_file2,nome_file4,nome_file5]
    X=[]
    Xerr=[]
    Y = [11.5e-2,41.7e-2,101e-2,172.4e-2]
    Yerr = []
    for nome_file in nomi:
        K=medie(nome_file)
        X.append(K[0])
        Xerr.append(K[1])
        Yerr.append(0.5e-2)
    M=[1,2,3,4]
    print(X, '\n', Xerr)
    plt.errorbar(M, X, Xerr, color='blue', fmt='o')
    plt.show()

    vel, sigma_vel, chi2 = fit_lineare(X,Xerr,Y,Yerr)
    print("Velocità stimata:",vel)
    print("Incertezza sulla velocità:",sigma_vel)
    print("Chi-quadro:",chi2)

    plt.errorbar(X, Y, yerr=Yerr, color='blue', fmt='o')
    x_coord = np.linspace(2e-8,max(X),1000)
    y_coord = vel*x_coord + vel*2*10**(-8)
    y_err = sigma_vel * x_coord
    plt.errorbar(x_coord,y_coord, yerr=y_err, color='red')
    plt.show()

if __name__ == "__main__":
    main()
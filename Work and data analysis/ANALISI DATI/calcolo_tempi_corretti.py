import numpy as np

#funzioni di propagazione degli errori
#Funzione che calcola l'incertezza su una somma di due termini
def sigmaSomma(sigmaA, sigmaB):
    S=sigmaA*sigmaA+sigmaB*sigmaB
    return np.sqrt(S)

#Funzione che calcola l'incertezza per un singolo delta_t
def sigmaDeltaT(V_max,Vs,tau,sigma_Vs,sigma_tau):
    log1 = np.log(V_max/(V_max-Vs))
    term1 = log1*sigma_tau
    term2 = tau*sigma_Vs/(V_max-Vs)
    return np.sqrt(term1**2+term2**2)


def processa_file(nome_file):
    # Carica il file, considera che i valori sono separati da spazi o tab
    dati = np.loadtxt(nome_file)
    
    # Estrai 
    dati_filtrati = dati[:, [0,1,2]]
    
    # Elimina righe con tutti zeri
    #dati_filtrati = dati_filtrati[~np.all(dati_filtrati == 0, axis=1)]
    dati_filtrati = dati_filtrati[~((dati_filtrati[:, 1] == 0) & (dati_filtrati[:, 1] == 0))]
    
    return dati_filtrati

def main():
    tau = 1e-9
    sigma_tau = 1.7e-9
    Vs = 3.15
    sigma_Vs = 0.65
    A = 2.06e-9
    B = 0.0916e-9
    sigma_A = 0.31e-9
    sigma_B = 0.0014e-9
    nome_file = "datitempitagliati4.txt"   #Sostituire comn il nome del file da utilizzare

    data = processa_file(nome_file)
    print (data)
    t = []
    sigma_t = []
    adc1 = []
    adc2 = []
    t_cor = []
    sigma_t_cor = []

    #Divisione dei valori importati dal file
    for row in data:
        t.append(A+B*row[0])
        sigma_t.append(np.sqrt(sigma_A**+(row[0]*sigma_B)**2))
        adc1.append(row[1])
        adc2.append(row[2])

    #Calcolo dei tempi corretti
    for i in range(len(t)):
        #Calcolo dei tempi corretti
        V1 = adc1[i]
        V2 = adc2[i]
        t_cor.append(t[i]-tau*(np.log(V2/(V2-Vs)-np.log(V1/(V1-Vs)))))

        #Calcolo dell'incertezza per delta_t1
        sigma1 = sigmaDeltaT(V1,Vs,tau,sigma_Vs,sigma_tau) 

        #Calcolo dell'incertezza per delta_t2
        sigma2 = sigmaDeltaT(V2,Vs,tau,sigma_Vs,sigma_tau) 

        #Calcolo dell'incertezza finale
        sigma = sigmaSomma(sigma1,sigma2)

        sigma_t_cor.append(sigma)

    f = open("Tempi_corretti4.txt","w")
    for i in range(len(t_cor)):
        f.write(str(t_cor[i])+" "+str(sigma_t_cor[i])+"\n")
    f.close()

if __name__ == "__main__":
    main()
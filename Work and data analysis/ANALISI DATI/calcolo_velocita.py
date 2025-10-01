import numpy as np

# Leggi il file e conserva solo la terza e la quarta colonna
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
    nome_file = "nome_file_con_tempi_corretti"
    data = processa_file(nome_file)
    d = [0.115,0.417,0.757,1.01,1.724]
    sigma_d = 0.005
    t = []
    sigma_t = []
    for row in data:
        t.append(row[0]*(10**(-9)))
        sigma_t.append(row[1]*(10**(-9)))
    v = []
    sigma_v = []
    for i in range(len(t)):
        v.append(d[i]/t[i])
        sigma_v.append(np.sqrt(sigma_d**2+(d[i]/t[i]*sigma_t[i])**2)/t[i])
    #v = v/(2.99*10**8)
    #sigma_v = sigma_v/(2.99*10**8)

    print(v)
    print(sigma_v)


if __name__ == "__main__":
    main()
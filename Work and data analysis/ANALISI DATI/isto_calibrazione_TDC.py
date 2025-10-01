import numpy as np
from iminuit import Minuit
from math import floor, ceil
from iminuit.cost import ExtendedBinnedNLL
from matplotlib import pyplot as plt
from scipy.stats import expon, norm

# Apri il file in modalità lettura
file_path = "TDC11s40t3.txt"  # Sostituisci con il percorso del tuo file

# Legge i dati dal file e li salva in un array
try:
    with open(file_path, "r") as file:
        sample_gaus = [float(line.strip()) for line in file if line.strip() and line.strip() != "0"]  # Rimuove eventuali spazi vuoti, righe vuote e gli 0
    
    print("Dati letti dal file:", sample_gaus)
except FileNotFoundError:
    print(f"Errore: Il file '{file_path}' non è stato trovato.")
except Exception as e:
    print(f"Si è verificato un errore: {e}")

N_evt=len(sample_gaus)
print(sample_gaus)

bin_edges = np.arange(floor(min(sample_gaus))-2, ceil(max(sample_gaus)) + 3)  # Genera bordi dei bin con larghezza unitaria
bin_content, _ = np.histogram(sample_gaus, bins=bin_edges)


def mod_signal_bin (bin_edges, N_signal, mu, sigma):
    return N_signal * norm.cdf (bin_edges, mu, sigma)

my_cost_func_bin = ExtendedBinnedNLL (bin_content, bin_edges, mod_signal_bin)
my_minuit_bin = Minuit (
                        my_cost_func_bin, 
                        N_signal = sum (bin_content), 
                        mu = np.mean (sample_gaus), 
                        sigma = np.std (sample_gaus),
                       )
my_minuit_bin.limits['N_signal', 'sigma'] = (0, None)
my_minuit_bin.migrad ()
#assert my_minuit_bin.valid


# get the estimate of the N_background and tau parameter for the final fit
mean_bin = [my_minuit_bin.values[1], my_minuit_bin.errors[1]]
sigma_bin = [my_minuit_bin.values[2], my_minuit_bin.errors[2]]
print(mean_bin, sigma_bin)
print(my_minuit_bin.values[2]+my_minuit_bin.errors[2])


# Aggiunta: Grafico
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])  # Calcola i centri dei bin

# Calcola i valori della distribuzione fittata corretti per i bin
fit_values = mod_signal_bin(bin_edges, my_minuit_bin.values['N_signal'], 
                            my_minuit_bin.values['mu'], my_minuit_bin.values['sigma'])
fit_values = np.diff(fit_values)  # Differenza cumulativa per ottenere i valori per bin
fit_values /= np.diff(bin_edges)  # Normalizza per la larghezza del bin

# Griglia più densa per la curva interpolata
x_dense = np.linspace(bin_edges[0], bin_edges[-1], 1000)
fit_dense = my_minuit_bin.values['N_signal'] * norm.pdf(x_dense, my_minuit_bin.values['mu'], my_minuit_bin.values['sigma'])

plt.hist(sample_gaus, bins=bin_edges, alpha=0.5, label='Dati', color='blue', edgecolor='black')
plt.plot(bin_centers, fit_values, label='Fit (Bin)', color='green', linewidth=2)
plt.plot(x_dense, fit_dense, label='Fit (Denso)', color='red', linestyle='--', linewidth=2)
plt.xlabel('Valore')
plt.ylabel('Conteggi')
plt.legend()
plt.title('Istogramma con Fit Sovrapposto')
plt.show()
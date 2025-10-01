import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Definizione della funzione costante per il fit
def costante(x, a):
    return a

# Leggi i dati dal file
# Modifica "dati.txt" con il percorso del tuo file
file_name = "SPURIEOK.txt"
x, y, err_y, err_x = np.loadtxt(file_name, unpack=True)

# Selezione dei dati del fondo
# Specifica l'intervallo in cui si trova il fondo
# Ad esempio, escludiamo il range della gaussiana [x_min_gauss, x_max_gauss]
x_min_gauss = -35.0  # Sostituisci con il valore reale
x_max_gauss = 26.0  # Sostituisci con il valore reale
mask_fondo = (x < x_min_gauss) | (x > x_max_gauss)  # Dati al di fuori della gaussiana

# Filtra i dati del fondo
x_fondo = x[mask_fondo]
y_fondo = y[mask_fondo]
err_y_fondo = err_y[mask_fondo]
err_x_fondo = err_x[mask_fondo]

# Fit dei dati del fondo con la funzione costante (utilizzando gli errori sulle y come pesi)
popt, pcov = curve_fit(costante, x_fondo, y_fondo, sigma=err_y_fondo, absolute_sigma=True)

# Estrai i parametri del fit e l'errore
a_fit = popt[0]
a_err = np.sqrt(pcov[0, 0])

# Calcolo di chi-quadro
residui = y_fondo - costante(x_fondo, *popt)
chi2 = np.sum((residui / err_y_fondo) ** 2)
ndof = len(y_fondo) - len(popt)  # Gradi di libertà
chi2_ridotto = chi2 / ndof

# Stampa i risultati
print(f"Parametro del fit (a): {a_fit:.4f} ± {a_err:.4f}")
print(f"Chi-quadro: {chi2:.2f}")
print(f"Gradi di libertà: {ndof}")
print(f"Chi-quadro ridotto: {chi2_ridotto:.2f}")

# Plot dei dati e del fit
plt.errorbar(x, y, yerr=err_y, xerr=err_x, fmt='o', label='Tutti i dati', ecolor='black', capsize=3)
plt.errorbar(x_fondo, y_fondo, yerr=err_y_fondo, xerr=err_x_fondo, fmt='o', label='Dati del fondo', ecolor='blue', capsize=3)
plt.axhline(y=a_fit, color='red', linestyle='--', label=f'Fit fondo: y = {a_fit:.4f} ± {a_err:.4f}')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fit del fondo con funzione costante')

# Aggiungi testo sul grafico per chi-quadro e altri dettagli
text = (f"$\chi^2$ = {chi2:.2f}\n"
        f"DoF = {ndof}\n"
        f"$\chi^2_{{ridotto}}$ = {chi2_ridotto:.2f}")
plt.text(0.05, 0.95, text, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

plt.legend()
plt.grid()
plt.show()



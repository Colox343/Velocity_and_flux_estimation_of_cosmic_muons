import matplotlib.pyplot as plt
from iminuit.cost import LeastSquares
from iminuit import Minuit
import scipy.special as SC
from math import exp, pi

# Funzione modello: somma di distribuzione uniforme e gaussiana
def model(n, lamb, B):
    Poisson=(lamb**(n)/(SC.factorial((abs(n)))))*exp(-lamb)
    uniform = B
    return Poisson + uniform

# Legge i dati da file
file_path = "accidentali.txt"  # Sostituire con il percorso del file
x_data, y_data, y_err = [], [], []
with open(file_path, "r") as file:
    for line in file:
        cols = line.split()
        print(cols[0])
        x_data.append(float(cols[0]))
        y_data.append(float(cols[1]))
        y_err.append(float(cols[2]))


print(x_data)
print(y_data)
#per normalizzare
S=sum(y_data)
for i in range(len(y_data)):
    y_data[i]=y_data[i]/S
    y_err[i]=y_err[i]/S
    #l'interpolazione non ha senso
# Creazione della funzione chi2
#LS = LeastSquares(x_data, y_data, y_err, model)
#m = Minuit(LS, lamb=0.1, B=0)  # Stima iniziale dei parametri
#m.migrad()  # Ottimizzazione

# Parametri ottimali
#lamb_fit = m.values["lamb"]
#B_fit = m.values["B"]

# Plot dei dati e del fit

#x_fit = [-50 + i * (100) / 1000 for i in range(1001)]
#y_fit = [model(x, lamb_fit, B_fit) for x in x_fit]

plt.errorbar(x_data, y_data, yerr=y_err, fmt="o", label="Data", color="blue", markersize=4)
#plt.plot(x_fit, y_fit, label="Fit", color="red", linewidth=2)
plt.xlabel("x")
plt.ylabel("y")
plt.title("grafico spurie")
plt.legend()
plt.show()

# Stampa del valor medio della distribuzione gaussiana
#print(f"Valor medio della distribuzione poissoniana (mu): {lamb_fit}")

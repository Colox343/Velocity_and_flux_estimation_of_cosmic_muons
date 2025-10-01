import numpy as np
from iminuit import Minuit
import matplotlib.pyplot as plt
from scipy.stats import chi2

y = np.array([5.20, 7.40, 11.40, 13.20, 15.20, 17.40, 19.20, 21.60, 25.40, 27.00, 31.40, 37.40])
x = np.array([24.4, 59.0, 101.8, 126.8, 148.8, 169.6, 189.0, 211.0, 257.7, 272.5, 316.1, 383.0])
sigma_y = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
sigma_x = np.array([1.2, 0.06, 0.4, 0.4, 0.4, 0.5, 0.04, 0.04, 0.5, 0.5, 0.4, 0.04])

def linear_model(x, B, A):
    return B * x + A

class LinearFitWithSigmaX:
    def __init__(self, x, y, sigma_y, sigma_x):
        self.x = x
        self.y = y
        self.sigma_y = sigma_y
        self.sigma_x = sigma_x

    def __call__(self, B, A):
        # Valore previsto dal modello
        y_pred = linear_model(self.x, B, A)
        # Deviazione standard combinata
        sigma_eff = np.sqrt(self.sigma_y**2 + (B * self.sigma_x)**2)
        chi2 = np.sum(((self.y - y_pred) / sigma_eff) ** 2)
        return chi2

cost = LinearFitWithSigmaX(x, y, sigma_y, sigma_x)

B_init = 1.0  
A_init = 0.0  

minuit = Minuit(cost, B=B_init, A=A_init)
minuit.migrad() 

chi2_value = minuit.fval  
ndof = len(y) - len(minuit.parameters) 
chi2_reduced = chi2_value / ndof
Prob = 1 - chi2.cdf(chi2_value, ndof) 


print("Risultati del fit:")
print(f"B (pendenza) = {minuit.values['B']} ± {minuit.errors['B']}")
print(f"A (intercetta) = {minuit.values['A']} ± {minuit.errors['A']}")
print(f"Chi-quadro = {chi2_value:.2f}")
print(f"Chi-quadro ridotto = {chi2_reduced:.2f} (chi2/ndof)")
print(f"Prob = {Prob:.4f}")


x_fit = np.linspace(min(x), max(x), 500)
y_fit = linear_model(x_fit, minuit.values['B'], minuit.values['A'])

plt.errorbar(x, y, yerr=sigma_y, xerr=sigma_x, fmt='o', markersize=1.5, ecolor='grey', color='black', capsize=3)
plt.plot(x_fit, y_fit, color='red', linestyle='--')
plt.xlabel('Canali TDC')
plt.ylabel('$T_{delay}[ns]$')
plt.title('Fit lineare per calibrazione del TDC')

text = (f"B = {minuit.values['B']:.4f} $\pm$ {minuit.errors['B']:.4f}\n"
        f"A = {minuit.values['A']:.4f} $\pm$ {minuit.errors['A']:.4f}\n"
        f"$\chi^2$ = {chi2_value:.3f}\n"
        f"DoF = {ndof}\n"
        f"$\chi^2_{{ridotto}}$ = {chi2_reduced:.3f}\n"
        f"Prob = {Prob:.4f}")
plt.text(0.05, 0.95, text, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
plt.grid(True, alpha=0.2)
plt.show()

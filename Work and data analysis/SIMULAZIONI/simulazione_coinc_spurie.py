import numpy as np
from random import random

#Questo programma simula il verificarsi di coincidenze spurie fra i due scintillatori. Si suppone che abbiano dimensioni di 30x80cm e una frequenza di incidenza dei muoni di 2400 muoni/min

#I numeri sono generati seguendo una poissoniana
 
def random_exp():
	return -np.log(1-random())

def random_poisson(mean):
	n = 0
	s = random_exp()
	while s < mean:
		n += 1
		s += random_exp()
	return n

def main():
	res = 9*(10**(-9))	#Risoluzione dell'unità di coincidenza
	t = 60*60		#Tempo di simulazione in secondi
	mean = 40*t		#Numero di muoni medi nel tempo t
	delta_t = res*2		#Intervallo di tempo in cui può verificarsi una coincidenza spuria dato il passaggio di un muone per il primo scintillatore
	mu = delta_t*40		#Numero medio di muoni incidenti nel tempo delta_t
	N_experiments = 1000
	n_coincidences = []
	
	'''Simulazione delle coincidenze spurie. Se nell'intervaòllo di tempo delta_t passa almeno un muone per il secondo scintillatore
	il conteggio delle coincidenze spurie è incerementato di 1'''
	for i in range(N_experiments):
		n = random_poisson(mean)
		s = 0
		for j in range(n):
			if random_poisson(mu) != 0:
				s += 1
		n_coincidences.append(s)
	
	#Calcolo di media e varianza
	coinc_mean = 0
	coinc_stdv = 0
		
	for i in range(N_experiments):
		coinc_mean += n_coincidences[i]
	coinc_mean /= N_experiments
	
	for i in range(N_experiments):
		coinc_stdv += (n_coincidences[i]-coinc_mean)**2
	coinc_stdv = np.sqrt(coinc_stdv/((N_experiments)*(N_experiments-1)))
	
	#Stampa dei risultati
	print("Coincidenze spurie\nMedia:",coinc_mean,"\nIncertezza:",coinc_stdv)

if __name__ == "__main__":
	main()

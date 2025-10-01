from random import random
import numpy as np

'''Questo è un simulatore delle coincidenze totali fra gli scintillatori S1(di sopra) ed S2(di sotto) al variare del ritardo nella presa dati di S2 in rapporto a S1.
NOTA: Questo programma è ancora da completare.'''

def random_exp():	#Generatore di numeri casuali secondo una distribuzione esponenziale
	return -np.log(1-random())

def random_theta():         #Generatore di un numero casuale con la densità di probabilità sin(2*theta) fra 0 e pi/2
    y = 2
    theta = 0
    while y > np.cos(theta)**2:
        y = random()
        x = random()*np.pi/2
    return y
	
def random_phi():          #Generatore di un numero casuale secondo una densità di probabilità uniforme fra 0 e 2*pi
	return random()*2*np.pi

def get_coinc(t0,times,delta_t):
    for i in range(len(times)):
        if np.abs(t0-times[i]) < delta_t:
            return True
    return False

	
def main():
	T = 60		#Tempo di presa dati in secondi
	delay = 5*(10**(-9))	#Ritardo di S2 rispetto a S1 in secondi
	res = 4.15*(10**(-9))	#Risoluzione del modulo di coincidenza
	F = T*40	#Numero di muoni medio nel tempo T
	f = T*40*0.18   #Numero medio di muoni che passa per S2 ma non per S1 nel tempo T
	v = 0.99*2.99*3*(10**8)		#Velocità dei muoni
	#Dimensioni degli scintillatori (in metri)
	delta_x = 0.3
	delta_y = 0.8
    	#Coordinata z del punto di fine (in metri)
	z = 0.1
	#Tempo impiegato da un muone con direzione verticale a percorrere la distanza tra i due scintillatori. Il tempo per una direzione theta sarà t0/cos(theta)
	t0 = z/v 
	
	times = []    #Istanti in cui entrano i muoni nel primo scintillatore
	theta_i = [] 	#Orientazioni theta dei muoni in entrata in S1
	phi = []	#Orientazioni phi dei muoni in entrata in S1
	x = []		#Coordinate x e y dei muoni in entrata in S1
	y = []
	m_in = []   #Muoni che passano sia per S1 che per S2
	s = 0
	
    	#Generazione degli istanti di tempo per cui passano i muoni per S1
	s += random_exp()/F*T	
	while s < T:
		times.append(s)
		s += random_exp()/F*T
	
    	#Generazione del resto dei parametri dei muoni che passano per S1
	length = len(times)
	for i in range(length):
		theta_i.append(random_theta())
		phi.append(random()*2*np.pi)
		x.append(delta_x*random()-delta_x/2)
		y.append(delta_y*random()-delta_y/2)
		x2 = x[i]+z*np.tan(random_theta())*np.cos(random_phi())
		y2 = y[i]+z*np.tan(random_theta())*np.sin(random_phi())
		if np.abs(x2) < delta_x/2 and np.abs(y2) < delta_y/2:
			m_in.append(True)
		else:
			m_in.append(False)
	
	#Generazione degli istanti in cui passano per S2 i muoni che non sono passati per S1
	times2 = []     #Istanti in cui questi muoni passano per S2
	s = random_exp()/f*T
	coinc = 0
	while s < T:
		times2.append(s)
		s += random_exp()/f*T
		
	for i in range(length):
		if m_in[i]:
	    		if np.abs(t0/np.cos(theta_i[i])+delay) < res:
	    			coinc += 1
	    		elif get_coinc(times[i]+delay,times2,res):
	    			coinc += 1
	#Stampa dei risultati
	print("Numero muoni:",length,"\n")
	print("Numero coincidenze",coinc,"\n")
	print("Percentuale coincidenze:",coinc/length*100,"%\n")

if __name__ == "__main__":
	main()

import random
import numpy as np

"""Questo simulatore stima quanti dei muoni che passano per lo scintillatore 1 passano anche per lo scintillatore 2.
I risultati sono espressi in maniera proporzionale, in cui il valore massimo è 1 (tutti i muoni sono compresi nel valore) 
e il minimo lo 0 (nessun muone è compreso)"""

def random_theta():         #Generatore di un numero casuale con la densità di probabilità sin(2*theta) fra 0 e pi/2
    y = 2
    theta = 0
    while y > np.cos(theta)**2:
        y = random.random()
        theta = random.random()*np.pi/2
    return theta
	
def random_phi():          #Generatore di un numero casuale secondo una densità di probabilità uniforme fra 0 e 2*pi
	return random.random()*2*np.pi

def main():
	#Dimensioni degli scintillatori (in metri)
	delta_x = 0.3
	delta_y = 0.8
    	#Coordinata z del punto di fine (in metri)
	z = 0.1
    
	m_in = []    #Numero di muoni che rimangono o escono dal perimetro
	m_out = []
	n_experiments = 1000
	n_muons = 1000

	for i in range(n_experiments):      #Simulazione Monte-Carlo
	    m_in.append(0)
	    m_out.append(0)
	    for j in range(n_muons):
		    x = random.random()*delta_x-delta_x/2		#Coordinate iniziali sul primo scintillatore
		    y = random.random()*delta_y-delta_y/2
		    theta = random_theta()
		    phi = random_phi()
		    x2 = x+z*np.tan(theta)*np.cos(phi)		#Coordinate finali sul secondo sicntillatore
		    y2 = y+z*np.tan(theta)*np.sin(phi)
		    if x2 < -delta_x/2 or x2 > delta_x/2 or y2 < -delta_y/2 or y2>delta_y/2:
			    m_out[i] += 1
		    else:
			    m_in[i] += 1
	    m_in[i] /= n_experiments
	    m_out[i] /= n_experiments
	
	mean_in = 0
	stdv_in = 0
	mean_out = 0
	stdv_out = 0
	
	#Calcolo delle medie
	for i in range(n_experiments):
		mean_in += m_in[i]
		mean_out += m_out[i]	
	mean_in /= n_experiments
	mean_out /= n_experiments
	
	#Calcolo delle incertezze	
	for i in range(n_experiments):
		stdv_in += (m_in[i]-mean_in)**2
		stdv_out += (m_out[i]-mean_out)**2	
	stdv_in = np.sqrt(stdv_in/(n_experiments-1))
	stdv_out = np.sqrt(stdv_out/(n_experiments-1))
			
    	#Stampa dei risultati
	print("Muons in:",mean_in,"+-",stdv_in,"\n")
	print("Muons out:",mean_out,"+-",stdv_out,"\n")


if __name__ == "__main__":
	main()

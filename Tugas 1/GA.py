import random
import numpy as np
import matplotlib.pyplot as plt 
from numpy import arange
from pylab import imshow,contour,clabel,axis,title,show,meshgrid
from mpl_toolkits.mplot3d import Axes3D

print("Nama  	: Irawansyah")
print("Kelas 	: IFIK-41-03")
print("Nim     : 1301174689")
print()

Rax1 			= 3  	#Batas Atas
Rbx1 			= -3 	#Batas Bawah
Rax2 			= 2  	#Batas Atas
Rbx2 			= -2 	#Batas Bawah
mutationRate	= 0.06 	#Probability Mutasi
ProbCrossOver 	= 0.67 	#Probability CrossOver
UkPop  			= 10	#Ukuran Populasi
JumGen 			= 20	#Jumlah Generasi


#Membuat Fungsi Rumus
def rumus(x1,x2):
	return(4-2.1*x1**2+x1**4/3)*x1**2+x1*x2+(-4+4*x2**2)*x2**2


bounds 		= [(-3, 3), (-2, 2)]
x11			= np.arange(-3,3,0.1)
x12			= np.arange(-2,2,0.1)
xgrid, ygrid= np.meshgrid(x11, x12)
xy 			= np.stack(rumus(xgrid, ygrid))
figure1 	= plt.figure()
BuatPloting = figure1.add_subplot(111, projection = '3d')
BuatPloting.plot_surface(xgrid, ygrid, xy, cmap='terrain')
BuatPloting.set_title('Genetic Algorithm')

#Generate Populasi
#InisialisasiPopulasiBiner
Populasi=np.random.randint(2,size = (UkPop,JumGen))

#Generate Kromosom dengan Menggunakan Batasan -3 dan 3
#DekodeKromosomBiner
def Kromosomx1(Populasi):
    MaxSum = 0
    Penampung1 =(JumGen/2)-1
    LenghtGen1 = int (JumGen)
    x1 = np.zeros([UkPop],  dtype = float)
    for kk in range(1,LenghtGen1):
    	MaxSum = MaxSum + 2**(-kk)
    for ii in range(0,UkPop):
    	for jj in range (1,LenghtGen1):
    		x1[ii] = x1[ii] + Populasi[ii][jj-1]*(2**-jj)
    	x1[ii] = Rbx1 + ((Rax1-Rbx1)/MaxSum) * x1[ii]
    return x1

#Generate Kromosom dengan Menggunakan Batasan -2 dan 2
#DekodeKromosomBiner
def Kromosomx2(Populasi):
    JumGen2=(JumGen/2)-1
    LenghtGen2 = int (JumGen)
    MaxSum = 0
    x2 = np.zeros([UkPop],  dtype = float)
    for kk in range(1,LenghtGen2):
    	MaxSum = MaxSum + 2**(-kk)
    for ii in range(0,UkPop):
    	for jj in range (1,LenghtGen2):
    		x2[ii] = x2[ii] + Populasi[ii][jj-1]*(2**-jj)
    	x2[ii] = Rbx2 + ((Rax2-Rbx2)/MaxSum) * x2[ii]
    return x2

#EvaluasiIndividu
def Fitnees(x1,x2):
	BilKecil = 0.001
	h = 1/(4-2.1*x1**2+x1**4/3)*x1**2+x1*x2+(-4+4*x2**2)*x2**2
	Fitnees = 1 / (h + BilKecil)
	return Fitnees

#RouletteWheel/Seleksi untuk Mencari Parent
def Parent(Populasi, Fitnees):
	Pindex=0
	JumlahFitness = sum(Fitnees)
	for i in range(len(Populasi)):
		if (Fitnees[i]/JumlahFitness) > np.random.uniform(0.1):
			Pindex = i
			break
		i = i + 1
	return Populasi[Pindex]

#Mencari Child berdasarkan Parent
def CrossOver(Parent1,Parent2,JumGen):
	if(np.random.rand()<ProbCrossOver):
		limit	= int(1+(np.ceil(np.random.randint(JumGen-1))))
		Child1 	= np.concatenate([Parent1[0:limit], Parent2[limit:JumGen]])
		Child2 	= np.concatenate([Parent2[0:limit], Parent1[limit:JumGen]])
		return Child1

#MutasiKromosom
def MutasiKromosom(Kromosom,JumGen, mutationRate):
	MutKrom = Kromosom
	for i in range(JumGen):
		if (np.random.uniform(0.1) < mutationRate):
			if (Kromosom[i]==0):
				MutKrom[i] = 1
			else:
				MutKrom[i] = 0
	return np.concatenate(MutKrom)

print()
print("_______Populasi______")
print(Populasi)
print()
for i in range(JumGen):
	for j in range(UkPop):
		individu		= Kromosomx1(Populasi)
		individu1 		= Kromosomx2(Populasi)
		fitnees  		= Fitnees(individu,individu1)
		#fitnees  		= Fitnees(Kromosomx1(Populasi),Kromosomx2(Populasi))
		Parent1  		= Parent(Populasi,Fitnees(Kromosomx1(Populasi),Kromosomx2(Populasi)))
		Parent2  		= Parent(Populasi,Fitnees(Kromosomx1(Populasi),Kromosomx2(Populasi)))
		Parent3 		= [[Parent1],[Parent2]]
		child    		= CrossOver(Parent1,Parent2,JumGen)
		child2   		= CrossOver(Parent1,Parent2,JumGen)
		child3	 		= [[child],[child2]]
		# Kromosom 		= (individu,individu1)
		Kromosom 		= (individu,individu1)
		offspring	  	= MutasiKromosom(Kromosom,JumGen,mutationRate)
		new_population	= child
		new_population	= child2
		# MinimasiFunction= min(rumus((individu),(individu1)))
	populasi = np.array(new_population)
	print("Generasi ke %d: "%(i+1) ,populasi)

BuatPloting.scatter(individu,individu1,s=100, lw=0, c='red', alpha=1); plt.pause(0.001)
print()
print("_____________________________Kromosom____________________________________")
print(individu)
print(individu1)
print()
print("______________________________Fitnees___________________________________")
print(fitnees)
print()
print("______________________________Parent____________________________________")
print(Parent1)
print(Parent2)
print()
print("______________________________Child_______________________________________")
print(child)
print(child2)
print()
print("_______________________________Mutasi_____________________________________")
print(offspring)
print()
print("Kromosom Terbaik")
print(min(offspring))
print()
print("Hasil Dekode Kromosom Terbaik untuk X1")
print(min(individu))
print()
print("Hasil Dekode Kromosom Terbaik untuk X2")
print(min(individu1))
print()
print("Hasil dari nilai x1 dan x2 adalah ")
print(MinimasiFunction)
print()
plt.show()
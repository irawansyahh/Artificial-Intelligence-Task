import random
import numpy as np
import math
import pandas as pd
from pandas import DataFrame
import tkinter as tk
from tkinter import filedialog

print("Nama  	: Irawansyah")
print("Kelas 	: IFIK-41-03")
print("Nim      : 1301174689")
print()

ProbMutationRate	= 0.1 #Probability Mutasi
ProbCrossOver 	  = 0.8 #Probability CrossOver
UkPop  			      = 10 
JumGen 			      = 15
Generasi          = 1000 

col_names = ['Suhu', 'Waktu', 'KondisiLangit', 'Kelembapan' , 'Terbang']
file = pd.read_csv("DataTrain.csv",sep=",",header=None,names=col_names)
data = file.values
file.head()
print(file)

Suhu          = ['Rendah', 'Normal', 'Tinggi']
Waktu         = ['Pagi', 'Siang', 'Sore', 'Malam']
Kondisi       = ['Cerah', 'Berawan', 'Rintik', 'Hujan'] 
Kelembapan    = ['Rendah', 'Normal', 'Tinggi']
Terbang       = ['Ya']

def Atas(i):
  i = (math.ceil(i / JumGen)) * JumGen
  return i

def Bawah(i):
  i = (i//JumGen) * JumGen
  return i 

def CheckAturan(kolom, aturan, data):
  i = kolom.index(data)
  Checkaturan = aturan[i] == 1
  return Checkaturan

def Split(Kromosom, SumKromosom):
  Split = [Kromosom[i:i + SumKromosom] for i in range(0, len(Kromosom), SumKromosom)]
  return Split

#Membangun Populasi 
def GeneratePopulation(x):
  Kromosom = []
  Populasi = []
  for i in range(x):
    for j in range(JumGen):
      Kromosom.append(random.randint(0, 1))
    Populasi.append(Kromosom)
  return Populasi

def DecisionTree(Kromosom, data):
	aturan = Split(Kromosom, JumGen)

	# del rules[-1:]
	for i,j in enumerate(aturan):
		suhu = j[0:3]
		waktu = j[3:7]
		kondisi = j[7:11]
		kelembapan = j[11:14]
		terbang = j[14]
		if CheckAturan(Suhu, suhu, data[0]) and CheckAturan(Waktu, waktu, data[1]) and CheckAturan(Kondisi, kondisi, data[2]) and CheckAturan(Kelembapan, kelembapan, data[3]):
			if terbang == 1:
				return 'Ya'
			else:
				return 'Tidak'
	return 'Tidak'

# DecisionTree()


#Evaluasi Individu
def Fitnees(populations):
  fitnees = []
  for i in range(UkPop):
    total = 0
    Kromosom = populations[i]
    for j in data:
      DecisionTree1 = DecisionTree(Kromosom, j)
      if DecisionTree1 == j[4]:
        total += 1
    fitnees.append({'i': i,'fitnees': total / len(data)})
  return fitnees

#Seleksi untuk Mencari Parent
def Parent(populations, fitnees):
  index = sorted(fitnees, key=lambda x: x['fitnees'], reverse=True) 
  parent1 = populations[index[0]['i']]
  parent2 = populations[index[1]['i']]
  return parent1, parent2

#Mencari Child berdasarkan Parent
def Crossover(parrent, ProbCrossOver):
  p1, p2 = parrent
  result = []
  if random.uniform(0, 1) > ProbCrossOver:
    return [p1[:], p2[:]]
  if len(p2) < len(p1):
    p1, p2 = p2, p1
  r1 =random.randint(0, len(p1)//2)
  r2 =random.randint(len(p1)//2, len(p1))
  i = [r1,r2]
  lenghtp1 = i[1] - i[0]
  p1_gap = lenghtp1 % JumGen
  p2_1 = [i[0], i[0] + lenghtp1]
  if p2_1 not in result:
    result.append(p2_1)
  p2_2 = [i[0], i[0] + p1_gap]
  if p2_2 not in result:
    result.append(p2_2)
  p2_3 = [i[1] - lenghtp1, i[1]]
  if p2_3 not in result:
    result.append(p2_3)
  p2_4 = [i[1] - p1_gap, i[1]]
  if p2_4 not in result:
    result.append(p2_4)

  index = random.randint(0, len(result)-1)
  j = result[index]
  
  # Child 1
  kiri = p1[Bawah(j[0]):j[0]]
  tengah = p2[j[0]:j[1]]
  kanan = p1[j[1]:Atas(j[1])]
  child1 = kiri + tengah + kanan

  # Child 2
  kiri = p2[0:j[0]]
  tengah = p1[i[0]:i[1]]
  kanan = p2[j[1]:]

  child2 = kiri + tengah + kanan
  return [child1, child2]

#MutasiKromosom
def Mutation(child, ProbMutationRate):
  for i in range(len(child[0])):
    if random.uniform(0, 1) < ProbMutationRate:
      if child[0][i] == 0:
        child[0][i] = 1
      else:
        child[0][i] = 0
  for i in range(len(child[1])):
    if random.uniform(0, 1) < ProbMutationRate:
      if child[1][i] == 0:
        child[1][i] = 1
      else:
        child[1][i] = 0  
  return child

#Membuat Populasi Baru
def SurvivorSelection(populations, fitnees, child):
  index = sorted(fitnees, key=lambda x: x['fitnees'], reverse=True)
  index1 = index[len(index)-1]['i']
  index2 = index[len(index)-2]['i']
  populations[index1] = child[0]
  populations[index2] = child[1]
  return populations

def exportCSV ():
    global df  
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv (export_file_path,header=False,index=None)

populations = GeneratePopulation(UkPop)
for i in range(Generasi):
  fitnees = Fitnees(populations)
  parent = Parent(populations, fitnees)
  child = Crossover(parent, ProbCrossOver)
  child = Mutation(child,ProbMutationRate )
  populations = SurvivorSelection(populations, fitnees, child)

  if i % 100 == 0:
    fitnees = Fitnees(populations)
    index = sorted(fitnees, key=lambda x: x['fitnees'], reverse=True)
    print("Accuracy to",i+100,":", index[0]['fitnees'])

fitnees = Fitnees(populations)
index = sorted(fitnees, key=lambda x: x['fitnees'], reverse=True)
BestChromosome = populations[index[0]['i']]
print()
print("Kromosom Tebaik")
print(BestChromosome)
print()

col_names = ['Suhu', 'Waktu', 'KondisiLangit', 'Kelembapan' , 'Terbang']
FileTest = pd.read_csv("Data Uji.csv", sep=",",header=None,names=col_names)
DataTest = FileTest.values
print()
print("--------------------------------")
print("Hasil Tebakan Dari Data Training")
print("--------------------------------")
for i in DataTest:
  result = DecisionTree(BestChromosome, i)
  if result == 'Ya':
    Hasil = 1
  else:
    Hasil = 0
  print(Hasil,"\t")
DataHasil = {'Hasil': [Hasil]
        }

df = DataFrame(DataHasil)
df.to_csv("Hasil.csv",index=False,sep='\t')
root= tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)
root.mainloop()
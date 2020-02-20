import csv
import pandas as pd
import matplotlib.pyplot as plt 

print("Nama     : Irawansyah")
print("Kelas    : IFIK-41-03")
print("Nim      : 1301174689")
print()


#Fuzzifikasi
def followerssangatrendah(x): 
    global sangatrendah
    if x <= 15000:
        sangatrendah = 1
    elif x >= 25000:
    	sangatrendah =  0
    else:
        sangatrendah = (25000 - x) / (25000 - 15000)
    return sangatrendah

def followersrendah(x):
    global rendah 
    if 20000 <= x <= 45000:
        rendah  = 1
    elif 15000 <= x <= 20000:
        rendah =  (x - 15000) / (20000 - 15000)
    elif 45000 < x < 50000:
        rendah =  (50000 - x) / (50000 - 45000)
    else:
        rendah = 0 
    return rendah

def followerssedang(x): 
    global sedang
    if 50000 <= x <= 70000:
        sedang = 1
    elif 35000 < x < 50000:
        sedang = (x - 35000) / (50000 - 35000)
    elif 70000 < x < 75000:
        sedang =  (75000 - x) / (75000 - 70000)
    else:
        sedang = 0
    return sedang

def followersstinggi(x): 
    global tinggi
    if x >= 80000:
        tinggi =  1
    elif x <= 65000:
        tinggi =  0
    else:
        tinggi =  (x - 65000) / (80000 - 65000)
    return tinggi

#fuzzy locic EngRate
def engraterendah(x):
    global rendah
    if x <= 3:
        rendah = 1
    elif x >= 5:
        rendah =  0
    else:
        rendah = (5 - x) / (5 - 3)
    return rendah

def engratesedang(x):
    global sedang
    if 4 <= x <= 7:
        sedang = 1
    elif 3.5 < x < 6:
        sedang = (x - 3) / ( 6- 3.5)
    elif 6 < x < 7:
        sedang = (7 - x) / (7 - 6)
    else:
        sedang = 0
    return sedang

def engratetinggi(x):
    global tinggi 
    if x >= 7:
        tinggi = 1
    elif x <= 6:
        tinggi = 0
    else:
        tinggi =  (x - 6) / (7 - 6)
    return tinggi

def FungsiEng(x):
	rendah = engraterendah(x)
	sedang = engratesedang(x)
	tinggi = engratetinggi(x)
	return rendah,sedang,tinggi

def FungsiFollowers(x):
    sangatrendah = followerssangatrendah(x)
    rendah       = followersrendah(x)
    sedang       = followerssedang(x)
    tinggi       = followersstinggi(x)
    return sangatrendah,rendah,sedang,tinggi

#Inference
def inference(Fsangatrendah, Frendah, Fsedang, Ftinggi, Erendah, Esedang, Etinggi):
    sedang = []
    rendah = []
    tinggi = []
    rules  = [[min(Fsangatrendah, Erendah),'rendah'], [min(Frendah, Erendah), 'rendah'], 
            [min(Fsedang, Erendah),'sedang'],[min(Ftinggi, Erendah), 'sedang'],
    	 	[min(Fsangatrendah, Esedang),'rendah'],[min(Frendah, Esedang), 'sedang'], 
            [min(Fsedang, Esedang),'tinggi'],[min(Ftinggi, Esedang), 'tinggi'],
    		[min(Fsangatrendah, Etinggi),'sedang'],[min(Frendah, Etinggi), 'tinggi'], 
            [min(Fsedang, Etinggi),'tinggi'],[min(Ftinggi, Etinggi), 'tinggi']]
    for i in range(len(rules)):
        if rules[i][1] == 'rendah':
            rendah.append(rules[i][0])
        elif rules[i][1] == 'sedang':
            sedang.append(rules[i][0])
        elif rules[i][1] == 'tinggi':
        	tinggi.append(rules[i][0])
    return max(rendah),max(sedang),max(tinggi)


# Defuzzification 
def Defuzzification(rendah,sedang,tinggi):
    Defuzzification =((rendah * 50) + (sedang * 70) + (tinggi * 100)) / (rendah+sedang+tinggi)
    return Defuzzification

def main():
    result = []
    brand_ambassadors = []
    file = pd.read_csv("influencers.csv",sep=",")
    file.head()
    print(file)
    followers   = file.loc[:,'followerCount']
    engrate     = file.loc[:,'engagementRate']
    
    for i in range(len(followers)):
        Fsangatrendah, Frendah, Fsedang, Ftinggi = FungsiFollowers(followers[i])
        Erendah, Esedang, Etinggi = FungsiEng(engrate[i])
        rendah,sedang,tinggi = inference(Fsangatrendah, Frendah, Fsedang, Ftinggi, Erendah, Esedang, Etinggi)
        score = Defuzzification(rendah, sedang, tinggi)
        print("score ID ke",i+1,":",score)
        result.append([score, (i + 1)])
    result.sort(reverse=True)

    for i in range(0, 20):
        brand_ambassadors.append(result[i][1])

    data = open('chosen.csv','w')
    with data:
        writer = csv.writer(data,lineterminator ='\n')
        for val in brand_ambassadors:
            writer.writerow([val])

    print()
    print("output tersimpan dalam bentuk csv dengan nama file chosen.csv")        
    print()
    print("20 Id influencers terbaik yang layak menjadi brand ambassadors adalah sebagai berikut : ")
    print(brand_ambassadors)
    # plt.scatter(followers,engrate,s=200, c='red', alpha=0.5)
    plt.plot(brand_ambassadors,c="red",alpha = 0.5 )
    plt.title("Fuzzy Logic")
    # plt.legend([""])
    plt.xlabel("20 influencers terbaik")
    plt.ylabel("Id influencers")
    plt.show()

    print()

if __name__ == "__main__":
    main()
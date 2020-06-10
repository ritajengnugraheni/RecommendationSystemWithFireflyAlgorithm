import sys, json
import pymysql
import random
from random import randint
import math
import datetime
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='ta_rita')
cur = conn.cursor()
from numpy import linalg as LA
import timeit

start = timeit.default_timer()

#Your statements here
makan = []
def intensity(a,b,gamma,fit):
    c = []
    for i in range(len(a)):
        c.append(abs(a[i]-b[i]))
    dist = LA.norm(c)
    return fit*math.exp(-gamma*dist)

def attrativeness(a,b,gamma):
    c = []
    for i in range(len(a)):
        c.append(abs(a[i]-b[i]))
    dist = LA.norm(c)
    return math.exp(-gamma*dist)

def movefl(a,b,gamma,alpha):
    c = []
    for i in range(len(a)):
        z = a[i]+attrativeness(a,b,gamma)*(b[i]-a[i])+alpha*(random.random()-0.5)
        c.append(round(z,4))
    return (c)
def fit(a,durasi):
    total = 0
    fromto = []
    z = len(a)-1
    a = discrete(a.copy())
    for i in range(len(a)):
        if i==0:
            fromto.append(str(len(a))+","+str(a[i]))
        elif i==len(a)-1:
            fromto.append(str(a[i-1])+","+str(a[i]))
            fromto.append(str(a[i])+","+str(i+1))
        else :
            fromto.append(str(a[i-1])+","+str(a[i]))
    for y in range(len(fromto)):
        for x in range(len(durasi)):
            if(durasi[x][0]==fromto[y]):
                total = total + durasi[x][2]
    return total

def discrete(a):
    b = a.copy()
    b.sort()
    con = 0
    for i in range(len(b)):
        for j in range(len(a)):
            if b[i]==a[j]:
                a[j]=con
                con += 1
    return a

def normalisasi(a,c):
    min_a = min((a[r][0]) for r in range(len(a)))
    max_a = max((a[r][0]) for r in range(len(a)))
    if c =="tarif":
        for i in range(len(a)):
            a[i][1]= round(1-((a[i][0]-min_a)/(max_a-min_a)*(1-0)+0),3)
    else :
        for i in range(len(a)):
            a[i][1]= round((a[i][0]-min_a)/(max_a-min_a)*(1-0)+0,3)
        
def normalisasitm(d):
    min_d = min((d[r][2]) for r in range(len(d)))
    max_d = max((d[r][2]) for r in range(len(d)))
##    print("min", min_d)
##    print("max", max_d)
    for i in range(len(d)):
        d[i][3] = round(1-((d[i][2]-min_d)/(max_d - min_d)*(1-0)+0),3)

def in_jam(db_jadwal,hari,id_w):
    jam_buka = datetime.timedelta(0,0)
    jam_tutup = datetime.timedelta(0,0)
    for z in range(len(db_jadwal)):
        if db_jadwal[z][3] == hari and db_jadwal[z][0] == id_w:
            jam_buka = db_jadwal[z][1]
            jam_tutup = db_jadwal[z][2]
            if jam_tutup == datetime.timedelta(0,0):
                jam_tutup = datetime.timedelta(0,72000)
    return jam_buka,jam_tutup
def min_kuliner_from(id_wisata):
    min_waktu = 0
    for row in db_kulinerfrom:## ambil waktu jam kuliner ke wisata
        if (row[1]==id_wisata):
            print(row)
            if(min_waktu==0):
                min_waktu = row[3]
                id_kuliner = row[2]
            elif(row[3]<min_waktu):
                min_waktu = row[3]
                id_kuliner = row[2]
    print("min ",min_waktu," ",id_kuliner)
    total_waktu = datetime.timedelta(0,3600)+ datetime.timedelta(0,min_waktu)## 1 jam + waktu komen diatas
    for row in db_kulinerto:
##        print(row)
        if(row[1]==id_kuliner and row[2]==id_wisata):
            print(row)
    
    return min_waktu
##def min_kuliner_to(id_wisata):
##    min_waktu = 0
##    for row in db_kulinerfrom:
##        if (row[1]==id_wisata):
##            print(row)
##            if(min_waktu==0):
##                min_waktu = row[3]
##            elif(row[3]<min_waktu):
##                min_waktu = row[3]
##    print("min ",min_waktu)
##    return min_waktu
def fit2(a,durasi,id_wisata, rating, tarif,db_jadwal,day,waktu_kunjungan,hari_ke):
    user_durasi = 1
    user_rating = 1
    user_tarif = 1
    total = 0
    f_rating = []
    f_tarif = []
    f_durasi = []
    z = len(a)-1
    a = discrete(a.copy())
    f_arr = [] 
    hasil_wisata = [] #save hasil urutan wisata
    jadwal = [] #save penjadwalan
    jam = datetime.timedelta(0,28800)#jam 8:00:00
    d = datetime.datetime.today().weekday()+hari_ke
    if d > 6 :
        d = d-7
    hari = day[d]
    c= 0
    boll = False
    i=0
    mak = False
    while i<len(a) and boll==False :   
        if c==0:
            fromto = str(len(a))+","+str(a[i])
            for n in range(len(durasi)):
                if(durasi[n][0] == fromto):
                    jam = jam+datetime.timedelta(0,durasi[n][1])
                    jam_buka,jam_tutup = in_jam(db_jadwal,hari,id_wisata[a[i]])
                    if(jam>jam_buka ):
                        w = waktu_kunjungan[id_wisata[a[i]]]
                        if(w==datetime.timedelta(0,0)):
                            w = datetime.timedelta(0,3600)# bila waktu kunjungan kosong maka diset 1 jam
                        jam_m = jam
                        jam = jam + w 
                        hasil_wisata.append(a[i])
                        jadwal.extend([jam_m,jam])
                        f_durasi.append(durasi[n][2])
                        c =1
##                        print("id ke ",len(hasil_wisata))
                    else :
                        jam = datetime.timedelta(0,28800)#jam 8:00:00
                     
        else :
            fromto = (str(a[i-1])+","+str(a[i]))
            for n in range(len(durasi)):
                if (durasi[n][0] == fromto):
                    jam = jam+datetime.timedelta(0,durasi[n][1])
                    jam_buka,jam_tutup = in_jam(db_jadwal,hari,id_wisata[a[i]])
                    w = waktu_kunjungan[id_wisata[a[i]]]
                    if(w==datetime.timedelta(0,0)):
                        w = datetime.timedelta(0,3600)
                    jam_keluar = jam + w
                    if jam >jam_buka and jam < jam_tutup and jam_keluar <jam_tutup and jam < datetime.timedelta(0,72000) and jam_keluar < datetime.timedelta(0,72000):
                        hasil_wisata.append(a[i])
                        jadwal.extend([jam,jam_keluar])
                        f_durasi.append(durasi[n][2])
                        jam = jam_keluar
                    elif jam > jam_buka:
                        jam = jam - datetime.timedelta(0,durasi[n][1])
                        c = 1
                        while(boll==False):
                            fromto3 = str(a[i-c])+","+str(len(a))
                            for nn in range(len(durasi)):
                                if(durasi[nn][0]==fromto3):
                                    jam = jam+datetime.timedelta(0,durasi[nn][1])
##                                    print(len(hasil_wisata))
                                    if(jam<datetime.timedelta(0,72000)):#jam 20.00
                                        jadwal.append(jam)
                                        f_durasi.append(durasi[nn][2])
                                        boll = True
                                    else:
                                        del f_durasi[len(f_durasi)-1]
                                        del hasil_wisata[len(hasil_wisata)-1]
                                        del jadwal[len(jadwal)-1]
                                        del jadwal[len(jadwal)-1]
                                        jam = jadwal[len(jadwal)-1]
                                        c += 1
##        print(hasil_wisata)
##        print(" ".join(str(a) for a in jadwal))
        if jam > datetime.timedelta(0,39600) and jam < datetime.timedelta(0,54000) and mak == False :# if untuk kosongkan jadwal makan
##            print("jadwal ke-",len(jadwal))
##            id_last_wisata = hasil_wisata[len(hasil_wisata)-1]
##            min_kuliner= 0
##            min_kuliner = min_kuliner_from(id_last_wisata)
##            print(min_kuliner)
##            total_kuliner = datetime.timedelta(0,3600)+ datetime.timedelta(0,min_kuliner)
##            print(total_kuliner)
            jam_kk = jam+datetime.timedelta(0,7200)
##            print("makan ",jam," ",jam_kk)
####            hasil_wisata.append(33)
##            print(db_kuliner[0])
            jadwal.extend([jam, jam_kk])
            jam = jam_kk
##            makan.append(len(jadwal))
####            print(" ".join(str(a) for a in makan))
##            print("ffgfgfgf")
            mak = True
        i += 1
##    print(hasil_wisata," ".join(str(a) for a in jadwal))
    if len(jadwal)%2==0:
        bola = False
        while(bola==False and len(hasil_wisata)!=0):
            index_akhir = len(hasil_wisata)-1
            fromto4 = str(hasil_wisata[index_akhir])+","+str(len(a))
            for z in range(len(durasi)):
                if(durasi[z][0]==fromto4):
                    jam = jam+datetime.timedelta(0,durasi[z][1])
                    if(jam<datetime.timedelta(0,72000)):#jam 20.00
                        jadwal.append(jam)
                        f_durasi.append(durasi[z][2])
                        bola = True
                    else:
                        del f_durasi[len(f_durasi)-1]
                        del hasil_wisata[len(hasil_wisata)-1]
                        del jadwal[len(jadwal)-1]
                        del jadwal[len(jadwal)-1]
                        jam = jadwal[len(jadwal)-1]

    
    for p in hasil_wisata:
        f_rating.append(rating[id_wisata[p]][1])
        f_tarif.append(tarif[id_wisata[p]][1])

    fit_rating = sum(f_rating)
    fit_tarif = sum(f_tarif)
    fit_durasi = sum(f_durasi)
    if fit_rating != 0:
        fit_rating = fit_rating/len(f_rating)
    if fit_tarif != 0:
        fit_tarif = fit_tarif/len(f_tarif)
    if fit_durasi != 0:
        fit_durasi = fit_durasi/len(f_durasi)
    total_fitness = round((user_rating * fit_rating + user_tarif * fit_tarif + user_durasi * fit_durasi)/3,8) 
    return total_fitness,hasil_wisata,jadwal

def input_id_wisata(wisata):
    id_wisata = []
    for i in range(len(wisata)):
        id_wisata.append(db_wisata.index(wisata[i]))
    return id_wisata

def inisialisasi(wisata):
    populasi = []
    i = 0
    jml_populasi = 15
    if(len(wisata)==1):
        jml_populasi = 1
    elif len (wisata) == 2:
        jml_populasi = 2
    elif len(wisata) == 3:
        jml_populasi = 6
    elif len(wisata)==4 and jml_populasi>24:
        jml_populasi = 24
    while(i<250)and(len(populasi)<jml_populasi):
        a = []
        a = random.sample(range(0,len(wisata)),len(wisata))
        if (a in populasi) == False:
            populasi.append(a)
        i += 1
    fitness = []
    jadwal = []
    node_terpilih = []
    for i in range(len(populasi)):
        total_fitness,hasil_wisata,jadwal2 =fit2(populasi[i],durasi,id_wisata,rating,tarif,db_jadwal,day,waktu_kunjungan,1)
        fitness.append(total_fitness)
        node_terpilih.append(hasil_wisata) 
        jadwal.append(jadwal2)
##        print(i,"p1",populasi[i]," ")
##        print("   ",discrete(populasi[i].copy()))
##        print("   ",node_terpilih[i]," fit", fitness[i]," node",len(node_terpilih[i]))
    return populasi,fitness,jadwal,node_terpilih

def firefly(populasi,fitness,node_terpilih,jadwal,gamma,alpha,durasi,id_wisata,rating,tarif,db_jadwal,day,waktu_kunjungan,hari_ke):
    iterasi = 0
    while iterasi < 10:
        for i in range(len(populasi)):
            li = fitness[i]
            for j in range(len(populasi)):
                lj = fitness[j]
                if(lj>li):
                    if len(node_terpilih[j]) >= len(node_terpilih[i]):
                        populasi[i] = movefl(populasi[i],populasi[j],gamma,alpha)
                        total_fitness,hasil_wisata,jadwal2 =fit2(populasi[i],durasi,id_wisata,rating,tarif,db_jadwal,day,waktu_kunjungan,hari_ke)
                        fitness[i] = total_fitness
                        node_terpilih[i] = hasil_wisata
                        jadwal[i] = jadwal2
                    
##        for i in range(len(populasi)):
####            print(i," ",discrete(populasi[i].copy()))
##            print(" ",node_terpilih[i]," fit",fitness[i]," node:",len(node_terpilih[i]))
##        print("end")
        iterasi +=1
    node_max = max(len(a) for a in node_terpilih)
    fit_max = 0
    id_max_fitness = -1
    for v in range(len(node_terpilih)):
        if(len(node_terpilih[v])==node_max):
            if(fitness[v]>fit_max):
                id_max_fitness = v
                fit_max = fitness[v]
##    print("max",node_max)
##    print("kunang2 terbaik", id_max_fitness)
    return populasi,fitness,node_terpilih,jadwal,id_max_fitness

def getwisata(node_terpilih,wisata):
    hasil_wisata = []
    for i in node_terpilih:
        hasil_wisata.append(wisata[i])
    return hasil_wisata

def delete(wisata_t,wisata):
    for x in range(len(wisata_t)):
        y = 0
        c = False
        while y<len(wisata) and c == False:
            if(wisata_t[x]==wisata[y]):
                del wisata[y]
                c = True
            y +=1

def input_durasi(id_wisata,id_hotel,db_wisatatm,db_hotelto,db_hotelfrom):
    durasi = []
    for i in range(len(id_wisata)):
        for j in range(len(id_wisata)):
            if i != j:
                for n in range(len(db_wisatatm)):
                    if id_wisata[i] == db_wisatatm[n][0] and id_wisata[j] == db_wisatatm[n][1]:
                        c = str(i)+","+str(j)
                        durasi.append([c,db_wisatatm[n][2],db_wisatatm[n][3]])

    for i in range(len(id_wisata)):
        for k in range(len(db_hotelto)):
            if id_wisata[i] == db_hotelto[k][0] and id_hotel == db_hotelto[k][1]:
                c = str(i)+","+str(len(id_wisata))
                durasi.append([c,db_hotelto[k][2],db_hotelto[k][3]])
                
        for j in range(len(db_hotelfrom)):
                if id_hotel == db_hotelfrom[j][0] and id_wisata[i]== db_hotelfrom[j][1]:
                    c = str(len(id_wisata))+","+str(i)
                    durasi.append([c,db_hotelfrom[j][2],db_hotelfrom[j][3]])
    return durasi

##def normalisasi_input_user(rating,input_rating):
##    for i in range(len(rating)):
##        rating[i][1] = 1-(abs(rating[i][1] - input_rating))
##
##def normalisasi_input_durasi(db_hotelfrom,user_durasi):
##    for i in range(len(db_hotelfrom)):
##        db_hotelfrom[i][3] = 1-(abs(db_hotelfrom[i][3] - user_durasi))
        
pilihan = []
durasi = []
rating = []
tarif = []
db_hotel = []
db_wisata = []
db_jadwal = []
waktu_kunjungan = []
db_wisatatm = []
db_hotelto = []
db_hotelfrom = [] 
db_lat_wisata = []
db_lat_hotel = []

db_kuliner = []
db_kulinerfrom = []
db_kulinerto = []

cur.execute("SELECT * FROM dummykuliner") ##0 id kuliner, 1 nama, 3 lat, 4 long
for row in cur:
##    print(row[0],row[1],row[3],row[4])
    db_kuliner.append([row[0],row[1],row[3],row[4]])
##print(db_kuliner[0])
cur.execute("SELECT * FROM dummykulinerfrom") ##0 id , 1 id wisata, 3 id kuliner, 4 durasi
for row in cur:
##    print(row[0],row[1],row[2],row[3])
    db_kulinerfrom.append([row[0],row[1],row[2],row[3]])

cur.execute("SELECT * FROM dummykulinerto") ##0 id , 1 id kuliner, 3 id wisata, 4 durasi
for row in cur:
##    print(row[0],row[1],row[2],row[3])
    db_kulinerto.append([row[0],row[1],row[2],row[3]])

cur.execute("SELECT * FROM pilihan")
for row in cur:
    pilihan.append(row[1])
    
cur.execute("SELECT * FROM dummylocation")
for row in cur: 
    tarif.append([row[8],0])
    rating.append([row[10],0])
    db_wisata.append(row[1])
    waktu_kunjungan.append(row[9])
    db_lat_wisata.append([row[2],row[3]])
    
cur.execute("SELECT * FROM dummyjadwal")
for row in cur:
    db_jadwal.append([row[1],row[2],row[3],row[4]])

cur.execute("SELECT * FROM dummywisatatimematrix")
for row in cur:
    if row[3]!=0 :
        db_wisatatm.append([row[1],row[2],row[3],0])

cur.execute("SELECT * FROM dummyhoteltmfrom")
for row in cur:
    db_hotelfrom.append([row[1],row[2],row[3],0])

cur.execute("SELECT * FROM dummyhoteltmto")
for row in cur:
    db_hotelto.append([row[1],row[2],row[3],0])

cur.execute("SELECT * FROM dummyhotel ")
for row in cur:
    db_hotel.append(row[1])
    db_lat_hotel.append([row[3],row[4]])
cur.close()
conn.close()

day = []
day.append("senin")
day.append("selasa")
day.append("rabu")
day.append("kamis")
day.append("jumat")
day.append("sabtu")
day.append("minggu")
        
##isi variabale wisata dengan pilihan dari user
wisata = [] 
id_wisata = []

for i in range(len(pilihan)):
    if i == (len(pilihan)-1):
        hotel = pilihan[i]
    else:
        wisata.append(pilihan[i])
print(wisata)
hotel = "RedDoorz @ Natuna"

a = random.sample(range(0,27),24)
##print(len(a))
##
##for i in a:
##    wisata.append(db_wisata[i])
##wisata.append(db_wisata[2])
##wisata.append(db_wisata[22])
##wisata.append(db_wisata[3])
##wisata.append(db_wisata[24])
##wisata.append(db_wisata[5])
##wisata.append(db_wisata[26])
##wisata.append(db_wisata[7])
##wisata.append(db_wisata[7])

id_wisata = input_id_wisata(wisata)
id_hotel = db_hotel.index(hotel) + 1

##normalisasi 
normalisasitm(db_hotelfrom)
normalisasitm(db_hotelto)
normalisasitm(db_wisatatm)

normalisasi(tarif,"tarif")
normalisasi(rating,"rating")
##normalisasi2(durasi)



#inputan user
##data_j = sys.argv[1]
##data2 = json.loads(data_j)
##
##user_durasi = data2[0]
##user_rating = data2[1]
##user_tarif = data2[2]

##for i in db_hotelfrom:
##    print("a",i)

##normalisasi_input_user(rating,user_rating)
##normalisasi_input_user(tarif,user_tarif)

##normalisasi_input_durasi(db_hotelfrom,user_durasi)
##normalisasi_input_durasi(db_hotelto,user_durasi)
##normalisasi_input_durasi(db_wisatatm,user_durasi)


durasi = input_durasi(id_wisata,id_hotel,db_wisatatm,db_hotelto,db_hotelfrom)
    
##inisialisai populasi kunang-kunang
populasi,fitness,jadwal,node_terpilih = inisialisasi(wisata)   
        
## inisialisasi variable
gamma = 0.3
alpha = 0.7
print(id_wisata)
#Firefly algorithm
hari_ke = 1
populasi,fitness,node_terpilih,jadwal,id_max_fitness = firefly(populasi,fitness,node_terpilih,jadwal,gamma,alpha,durasi,id_wisata,rating,tarif,db_jadwal,day,waktu_kunjungan,hari_ke)
jadwal_1 = jadwal[id_max_fitness]
fitness_1 = fitness[id_max_fitness]
wisata_1 = getwisata(node_terpilih[id_max_fitness],wisata)
id_wisata_1 = getwisata(node_terpilih[id_max_fitness],id_wisata)

##print (wisata_1)
##print("terpilih",node_terpilih[id_max_fitness])
##print("wisata",wisata)
##print("id_wisata",id_wisata)
delete(wisata_1,wisata)
id_wisata = input_id_wisata(wisata)
##print("update wisata",wisata)
##print("id_wisata",id_wisata)
wisata_2 = []
id_wisata_2 = []
if len(wisata)!=0:
    hari_ke = 2
    populasi,fitness,jadwal,node_terpilih = inisialisasi(wisata)
    populasi,fitness,node_terpilih,jadwal,id_max_fitness = firefly(populasi,fitness,node_terpilih,jadwal,gamma,alpha,durasi,id_wisata,rating,tarif,db_jadwal,day,waktu_kunjungan,hari_ke)
    jadwal_2 = jadwal[id_max_fitness]
    fitness_2 = fitness[id_max_fitness]
    wisata_2 = getwisata(node_terpilih[id_max_fitness],wisata)
    id_wisata_2 = getwisata(node_terpilih[id_max_fitness],id_wisata)

##    print("node terpilih 1",node_terpilih[id_max_fitness])
##    print("wisata1",wisata_1)
##    print("wisata2",wisata_2)
##    print("wisata",wisata)
##    print("id",id_wisata)
##    print("id_wisata1",id_wisata_1)
##    print("id_wisata2",id_wisata_2)
    delete(wisata_2,wisata)
    id_wisata = input_id_wisata(wisata)
id_wisata_3 = []
wisata_3 = []
if len(wisata)!=0:
    hari_ke = 3
    populasi,fitness,jadwal,node_terpilih = inisialisasi(wisata)
    populasi,fitness,node_terpilih,jadwal,id_max_fitness = firefly(populasi,fitness,node_terpilih,jadwal,gamma,alpha,durasi,id_wisata,rating,tarif,db_jadwal,day,waktu_kunjungan,hari_ke)
    jadwal_3 = jadwal[id_max_fitness]
    fitness_3 = fitness[id_max_fitness]
    wisata_3 = getwisata(node_terpilih[id_max_fitness],wisata)
    id_wisata_3 = getwisata(node_terpilih[id_max_fitness],id_wisata)

    delete(wisata_1,wisata)
    id_wisata = input_id_wisata(wisata)

##    print("node terpilih ",node_terpilih[id_max_fitness])
##    print("wisata1",wisata_1)
##    print("wisata2",wisata_2)
##    print("wisata3",wisata_3)
##    print("wisata",wisata)
##    print("id",id_wisata)
##    print("id_wisata1",id_wisata_1)
##    print("id_wisata2",id_wisata_2)
##    print("id_wisata3",id_wisata_3)
    delete(wisata_2,wisata)
    id_wisata = input_id_wisata(wisata)

wis = []
for i in range(len(pilihan)-1):
    wis.append(pilihan[i])
    
id_wis = input_id_wisata(wis)

print("")
print("")
print("============ Hasil ===============")
print("")
print("")
print("hari ke 1")
print("fitness ",fitness_1)
print(id_wisata_1)
print(" ".join(str(a) for a in jadwal_1))
print("")
print("total fitness 1 ",fitness_1)
print("total node",len(id_wisata_1))
print("=========")
if(hari_ke>=2):
    print("hari ke 2")
    print("fitness ",fitness_2)
    print(id_wisata_2)
    print(" ".join(str(a) for a in jadwal_2))
    print("total fitness 1+2 ",(fitness_1+fitness_2)/2)
    print("total node",(len(id_wisata_1)+len(id_wisata_2)))
    print("=========")

if(hari_ke==3): 
    print("hari ke 3")
    print("fitness ",fitness_3)
    print(id_wisata_3)
    print(" ".join(str(a) for a in jadwal_3))
    print("total fitness 1+2+3 ",(fitness_1+fitness_2+fitness_3)/3)
    print("total node",(len(id_wisata_1)+len(id_wisata_2)+len(id_wisata_3)))

stop = timeit.default_timer()
print ("running time",stop - start)

for x in range(len(jadwal_1)):
    print(jadwal_1[x])
    if(jadwal_1[x]==jadwal_1[x-1]):
        print(x)
    
## convert to Json
hasil_id = []
hasil_jadwal = []
hasil_firefly = []
hasil_id.append(wisata_1)
hasil_jadwal.append([str(a) for a in jadwal_1])

##c_lat = []
##hasil_lat = []
##hasil_lat_hotel = str(db_lat_hotel[id_hotel-1][0])+','+str(db_lat_hotel[id_hotel-1][1])
##for w in id_wisata_1:
##    hasil_lat.append(str(db_lat_wisata[w][0])+','+str(db_lat_wisata[w][1]))
##c_lat.append(hasil_lat)
##
##if len(wisata_2)!=0:
##    hasil_id.append(wisata_2)
##    hasil_jadwal.append([str(a) for a in jadwal_2])
##    hasil_lat = []
##    for w in id_wisata_2:
##        hasil_lat.append(str(db_lat_wisata[w][0])+','+str(db_lat_wisata[w][1]))
##    c_lat.append(hasil_lat)
####    print(hasil_lat)
##if len(wisata_3)!=0:
##    hasil_id.append(wisata_3)
##    hasil_jadwal.append([str(a) for a in jadwal_3])
##    hasil_lat = []
##    for w in id_wisata_3:
##        hasil_lat.append(str(db_lat_wisata[w][0])+','+str(db_lat_wisata[w][1]))
##    c_lat.append(hasil_lat)
####    print(hasil_lat)
##hasil_firefly.append(hasil_id)
##hasil_firefly.append(hasil_jadwal)
##hasil_firefly.append(c_lat)
##hasil_firefly.append(hasil_lat_hotel)
##data = json.dumps(hasil_firefly)

##print(data)
# print("hello")

# print(data2)

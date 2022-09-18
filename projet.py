import PIL as pil
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import tkinter as tk

def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat

def nbrLig(image):
    return len(image)

def nbrCol(image):
    return len(image[0])

def rotate(qr_code):
    out=[]
    for i in range(nbrCol(qr_code)):
        l=[]
        for j in range(nbrLig(qr_code)):
            l.append(qr_code[j][i])
        l.reverse()
        out.append(l)
    qr_code=out
    return qr_code

def verif_sens(qr_code):
    lig=nbrLig(qr_code)-7
    col=nbrCol(qr_code)-7
    for i in range(4):
        if qr_code[lig][col]==0 and qr_code[lig][col+1]==0 and qr_code[lig][col+2]==0 and qr_code[lig][col+3]==0 and qr_code[lig][col+4]==0 and qr_code[lig][col+5]==0 and qr_code[lig][col+6]==0 and qr_code[lig+1][col]==0 and qr_code[lig+1][col+1]==1 and qr_code[lig+1][col+2]==1 and qr_code[lig+1][col+3]==1 and qr_code[lig+1][col+4]==1 and qr_code[lig+1][col+5]==1 and qr_code[lig+1][col+6]==0 and qr_code[lig+5][col]==0 and qr_code[lig+5][col+1]==1 and qr_code[lig+5][col+2]==1 and qr_code[lig+5][col+3]==1 and qr_code[lig+5][col+4]==1 and qr_code[lig+5][col+5]==1 and qr_code[lig+5][col+6]==0 and qr_code[lig+6][col]==0 and qr_code[lig+6][col+1]==0 and qr_code[lig+6][col+2]==0 and qr_code[lig+6][col+3]==0 and qr_code[lig+6][col+4]==0 and qr_code[lig+6][col+5]==0 and qr_code[lig+6][col+6]==0 and qr_code[lig+2][col]==0 and qr_code[lig+2][col+1]==1 and qr_code[lig+2][col+2]==0 and qr_code[lig+2][col+3]==0 and qr_code[lig+2][col+4]==0 and qr_code[lig+2][col+5]==1 and qr_code[lig+2][col+6]==0 and qr_code[lig+3][col]==0 and qr_code[lig+3][col+1]==1 and qr_code[lig+3][col+2]==0 and qr_code[lig+3][col+3]==0 and qr_code[lig+3][col+4]==0 and qr_code[lig+3][col+5]==1 and qr_code[lig+3][col+6]==0 and qr_code[lig+4][col]==0 and qr_code[lig+4][col+1]==1 and qr_code[lig+4][col+2]==0 and qr_code[lig+4][col+3]==0 and qr_code[lig+4][col+4]==0 and qr_code[lig+4][col+5]==1 and qr_code[lig+4][col+6]==0:
            out=[]
            for i in range(nbrCol(qr_code)):
                l=[]
                for j in range(nbrLig(qr_code)):
                    l.append(qr_code[j][i])
                l.reverse()
                out.append(l)
            qr_code=out
        else : return qr_code
    return False

def verif_line(qr_code):
    lig=nbrLig(qr_code)
    col=nbrCol(qr_code)
    for i in range(7, col-7):
        if i%2!=0 and qr_code[6][i]==1:
            verif=True
        elif i%2==0 and qr_code[6][i]==0:
            verif=True
        else:
            verif=False
            break
    if verif==True:
        for i in range(7, lig-7):
            if i%2!=0 and qr_code[i][6]==1:
                verif=True
            elif i%2==0 and qr_code[i][6]==0:
                verif=True
            else:
                verif=False
                break
    if verif==False:
        return False
    else: 
        return qr_code

def hammings(bits):
    if (bits[0]+bits[1]+bits[3])%2==bits[4]:
        c1=True
    else : c1=False
    if (bits[0]+bits[2]+bits[3])%2==bits[5]:
        c2=True
    else : c2=False
    if (bits[1]+bits[2]+bits[3])%2==bits[6]:
        c3=True
    else : c3=False

    if c1==False and c2==False and c3==True:
        bits[0]=(bits[0]+1)%2
    if c1==False and c2==True and c3==False:
        bits[1]=(bits[1]+1)%2
    if c1==True and c2==False and c3==False:
        bits[2]=(bits[2]+1)%2
    if c1==False and c2==False and c3==False:
        bits[3]=(bits[3]+1)%2
    return [bits[0], bits[1], bits[2], bits[3]]

def read(qr_code):
    global filter
    col=nbrCol(qr_code)-1
    lig=nbrLig(qr_code)-1
    r=[]
    a=0
    for k in range(0,nb_bloc_decrypt(qr_code)):
        r.append([])
        if a==0:
            for i in range(7):
                r[k].append(qr_code[lig][col-i])
                r[k].append(qr_code[lig-1][col-i])
            a=1
        elif a==1:
            for i in range(7, 14):
                r[k].append(qr_code[lig][col-i])
                r[k].append(qr_code[lig-1][col-i])
            lig-=2
            a=2
        elif a==2:
            for i in range(13, 6, -1):
                r[k].append(qr_code[lig][col-i])
                r[k].append(qr_code[lig-1][col-i])
            a=3
        elif a==3:
            for i in range(6, -1, -1):
                r[k].append(qr_code[lig][col-i])
                r[k].append(qr_code[lig-1][col-i])
            lig-=2
            a=0
    return r

def correction(qr_code):
    final=[]
    for i in range(len(qr_code)):
        correct=[]
        correct.append(hammings([qr_code[i][0], qr_code[i][1], qr_code[i][2], qr_code[i][3], qr_code[i][4], qr_code[i][5], qr_code[i][6]]))
        correct.append(hammings([qr_code[i][7], qr_code[i][8], qr_code[i][9], qr_code[i][10], qr_code[i][11], qr_code[i][12], qr_code[i][13]]))
        final.append("")
        for j in range(2):
            for k in correct[j]:
                final[i]+=str(k)
    return final

def decryption(qr_code):
    global hex_or_asc
    decrypt=""
    if hex_or_asc==0:
        for i in range(len(qr_code)):
            hexad=hex(int(qr_code[i], 2))
            decrypt+=hexad[2:5]
        label.config(text=decrypt)
    else:
        for i in range(len(qr_code)):
            decrypt+=chr(int(qr_code[i], 2))
        label.config(text=decrypt)

def nb_bloc_decrypt(qr_code):
    nb_bloc=str(qr_code[13][0])+str(qr_code[14][0])+str(qr_code[15][0])+str(qr_code[16][0])+str(qr_code[17][0])
    return int(nb_bloc, 2)

def appli_filter(qr_code):
    a=0
    bits=str(qr_code[22][8])+str(qr_code[23][8])
    if bits=="00": #aucun filtre
        return qr_code
    elif bits=="01": #damier
        for i in range(9, nbrLig(qr_code)):
            a=0
            for j in range(11, nbrCol(qr_code)):
                if i%2!=0:
                    if a==0:
                        qr_code[i][j]=qr_code[i][j]^0
                        a=1
                    elif a==1:
                        qr_code[i][j]=qr_code[i][j]^1
                        a=0
                elif i%2==0:
                    if a==0:
                        qr_code[i][j]=qr_code[i][j]^1
                        a=1
                    elif a==1:
                        qr_code[i][j]=qr_code[i][j]^0
                        a=0
        return qr_code
    elif bits=="10": #lignes horizontal
        for i in range(9, nbrLig(qr_code)):
            for j in range(11, nbrCol(qr_code)):
                if i%2!=0:
                    qr_code[i][j]=qr_code[i][j]^0
                elif i%2==0:
                    qr_code[i][j]=qr_code[i][j]^1
        return qr_code
    elif bits=="11": #ligne vertical
        for j in range(11, nbrCol(qr_code)):
            for i in range(9, nbrLig(qr_code)):
                if j%2!=0:
                    qr_code[i][j]=qr_code[i][j]^0
                elif j%2==0:
                    qr_code[i][j]=qr_code[i][j]^1
        return qr_code

def charger(widg):
    global filename, qr_code, hex_or_asc, filter
    filename= filedialog.askopenfile(mode='rb', title='Choose a file')
    qr_code=loading(filename)
    if nbrCol(qr_code)>=24 and nbrLig(qr_code)>=24:
        qr_code=verif_sens(qr_code)
        qr_code=verif_line(qr_code)
    else : qr_code=False
    if qr_code!=False :
        hex_or_asc=qr_code[24][8]
        qr_code=appli_filter(qr_code)
        qr_code=read(qr_code)
        qr_code=correction(qr_code)
        decryption(qr_code)
    else: label.config(text="QR code non valide.")

def exit(fenetre):
    fenetre.destroy()

fenetre = tk.Tk()
fenetre.title("QR code")
bouton_charger=tk.Button(fenetre, text="Charger un QR code.", command=lambda:charger(fenetre))
bouton_charger.grid(row=0, column=0, ipadx=10, ipady=0, padx=10, pady=5)
label=tk.Label(fenetre, text="QR code déchiffré ici.", bg="white")
label.grid(row=1, column=0, ipadx=10, ipady=3, padx=10, pady=0)
fenetre.geometry("205x100")
bouton_exit=tk.Button(fenetre, text="Quitter", command=lambda:exit(fenetre))
bouton_exit.grid(row=2, column=0, ipadx=10, ipady=0, padx=10, pady=2)

fenetre.mainloop()
import requests, json #pip install requests
import pandas as pd #pip install pandas
import matplotlib.pyplot as plt #pip install matplotlib
import datetime
import tkinter as tk
import  Monedas
import historial
from tkinter import *
def data(str):
    for i in str:
        if i=="(":
            start=str.index(i)+1
        if i==")":
            end = str.index(i)
    return str[start:end]


def Calculo():

    api_key = "1R2IELBRTU789QZB"
    alpha_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"

    var1 = data(variable1.get())
    var2 = data(variable2.get())

    final_url = alpha_url + "&from_currency=" + var1 + "&to_currency=" + var2 + "&apikey=" + api_key


    req_ob = requests.get(final_url)
    result = req_ob.json()
    Exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    monto = float(montos1.get())
    nuevo_monto = round(monto*Exchange_rate,2)

    Salida_monto.insert(0,str(nuevo_monto))


def limpiar_salida ():

    Salida_monto.delete(0,END)

def limpiar_entrada ():

    ingresar_monto.delete(0,END)
def texto():



    Bienvenido_Texto = Label(ventana_principal,text="Bienvenido al sistema de conversor de divisas",font=("Helvetica",18),)
    Bienvenido_Texto.place(x=67,y=40)

    Monto_Texto = Label(ventana_principal,text="Ingrese el monto:",font=("Helvetica",18),)
    Monto_Texto.place(x=200,y=150)

    #Pais_Origen_Texto = Label(ventana_principal,text="De:",font=("Helvetica",18),)
    #Pais_Origen_Texto.place(x=67,y=250)

    #Pais_Cambio_Texto = Label(ventana_principal,text="Hacia:",font=("Helvetica",18),)
    #Pais_Cambio_Texto.place(x=67,y=250)

    Cambio_Texto = Label(ventana_principal,text="El cambio es de:",font=("Helvetica",18),)
    Cambio_Texto.place(x=210,y=350)


def Entrada():
    global ingresar_monto
    ingresar_monto = Entry(ventana_principal,width=40,textvariable=montos1)
    ingresar_monto.place(x=160,y=200)

    global Salida_monto
    Salida_monto = Entry(ventana_principal,width=40)
    Salida_monto.place(x=160,y=400)

def Menu_Listas():

    global variable1
    global variable2
    variable1 = StringVar()
    variable1.set("De")
    variable2 = StringVar()
    variable2.set("Hacia")
    List_Paises = Monedas_FIsicas.List_Paises

    Origen_menu = OptionMenu(ventana_principal,variable1,*List_Paises)
    Origen_menu.place(x=250,y=250)

    Cambio_menu = OptionMenu(ventana_principal,variable2,*List_Paises)
    Cambio_menu.place(x=240,y=300)

def Botones():
    Boton_Convertir = Button(ventana_principal,width=15,text="Convertir",command=Calculo)
    Boton_Convertir.place(x=67,y=450)

    Boton_Historial = Button(ventana_principal,width=15,text="Historial",command=historial.Historial(ingresar_monto.get(),data(variable1.get()),data(variable2.get()),90))
    Boton_Historial.place(x=240,y=450)

    Boton_Limpiar = Button(ventana_principal,width=15,text="Limpiar",command=limpiar_salida)
    Boton_Limpiar.place(x=400,y=450)

ventana_principal = tk.Tk()
ventana_height = 587
ventana_width = 570

screen_width = ventana_principal.winfo_screenwidth()
screen_height = ventana_principal.winfo_screenheight()

x_cordinate = int((screen_width/2) - (ventana_height/2))
y_cordinate = int((screen_height/2) - (ventana_width/2))

ventana_principal.geometry("{}x{}+{}+{}".format(ventana_height, ventana_width, x_cordinate, y_cordinate))

ventana_principal.title("Convertidor de Divisas")


montos1 = StringVar()
texto()
Entrada()
Menu_Listas()
Botones()

ventana_principal.mainloop()
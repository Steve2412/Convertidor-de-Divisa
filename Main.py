import tkinter

import requests, json  # pip install requests
import pandas as pd  # pip install pandas
import matplotlib.pyplot as plt  # pip install matplotlib
from PIL import ImageTk, Image
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import Monedas
import sys
from tkinter import *

#Diseño de Interfaz

#Diseño Texto
def texto():
    Bienvenido_Texto = Label(ventana_principal, text="Bienvenido al sistema de conversor de divisas",
                             font=("Helvetica", 18), )
    Bienvenido_Texto.place(x=67, y=40)

    Monto_Texto = Label(ventana_principal, text="Ingrese el monto:", font=("Helvetica", 18), )
    Monto_Texto.place(x=200, y=150)

    # Pais_Origen_Texto = Label(ventana_principal,text="De:",font=("Helvetica",18),)
    # Pais_Origen_Texto.place(x=67,y=250)

    # Pais_Cambio_Texto = Label(ventana_principal,text="Hacia:",font=("Helvetica",18),)
    # Pais_Cambio_Texto.place(x=67,y=250)

    Cambio_Texto = Label(ventana_principal, text="El cambio es de:", font=("Helvetica", 18), )
    Cambio_Texto.place(x=210, y=350)

    Transformar_Texto = Label(ventana_principal, text="Convertir", font=("Helvetica", 12), )
    Transformar_Texto.place(x=150, y=535)

    Historial_Texto = Label(ventana_principal, text="Historial", font=("Helvetica", 12), )
    Historial_Texto.place(x=350, y=535)

#Diseño Entrada Datos
def Entrada():
    global ingresar_monto
    ingresar_monto = Entry(ventana_principal, width=40, textvariable=montos1)
    ingresar_monto.place(x=160, y=200)

    global Salida_monto
    Salida_monto = Entry(ventana_principal, width=40)
    Salida_monto.place(x=160, y=400)

#Diseño Menu Monedas Convertibles
def Menu_Listas():
    global variable1
    global variable2
    variable1 = StringVar()
    variable1.set("De")
    variable2 = StringVar()
    variable2.set("Hacia")
    List_Paises = Monedas.List_Paises

    global Origen_menu
    Origen_menu = variable1 = ttk.Combobox(ventana_principal, width=45, state="readonly")
    Origen_menu.set("De")
    Origen_menu['values'] = List_Paises
    Origen_menu.place(x=150, y=250)

    global Cambio_menu
    Cambio_menu = variable2 = ttk.Combobox(ventana_principal, width=45, state="readonly", )
    Cambio_menu.set("Hacia")
    Cambio_menu['values'] = List_Paises
    Cambio_menu.place(x=150, y=300)

#Filtro para recoger las siglas de la divisa
def data(str):
    for i in str:
        if i == "(":
            start = str.index(i) + 1
        if i == ")":
            end = str.index(i)
    return str[start:end]

#Calculos para la conversion de la divisa
def Calculo():
    global Formato
    limpiar_salida()
    if not ingresar_monto.get():
        Mensaje_Error_1()
        return

    if Origen_menu.get() == "De" or Cambio_menu.get() == "Hacia":
        Mensaje_Error_2()
        return

    api_key = "1R2IELBRTU789QZB"
    alpha_url = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"

    var1 = data(Origen_menu.get())
    var2 = data(Cambio_menu.get())
    var3 = "USD"

    final_url = alpha_url + "&from_currency=" + var1 + "&to_currency=" + var2 + "&apikey=" + api_key

    req_ob = requests.get(final_url)
    result = req_ob.json()

    if var1 == "USD" and var2 == "BS":
        monto = float(montos1.get())
        nuevo_monto = round(monto * 4.51, 2)
        Formato = '{:0,.2f}'.format(nuevo_monto)
        Salida_monto.insert(0, str(Formato))
        return
    elif var1 == "BS" and var2 == "USD":
        monto = float(montos1.get())
        nuevo_monto = round(monto / 4.51, 2)
        Formato = '{:0,.2f}'.format(nuevo_monto)
        Salida_monto.insert(0, str(Formato))
        return
    elif var1 == "EUR" and var2 == "BS":
        monto = float(montos1.get())
        nuevo_monto = round(monto * 5.10, 2)
        Salida_monto.insert(0, str(nuevo_monto))
        return
    elif var1 == "BS" and var2 == "EUR":
        monto = float(montos1.get())
        nuevo_monto = round(monto / 5.10, 2)
        Salida_monto.insert(0, str(nuevo_monto))
        return
    elif var1 == "BS" and var2 == "BS":
        monto = float(montos1.get())
        nuevo_monto = monto
        Formato = '{:0,.2f}'.format(nuevo_monto)
        Salida_monto.insert(0, str(Formato))
        return
    elif var2 != "BS" or "USD" or "EUR" and var1 == "BS" :
        Mensaje_Error_4()
        return
    elif var1 != "BS" or "USD" or "EUR" and var2 == "BS":
        pre_url = alpha_url + "&from_currency=" + var1 + "&to_currency=" + var3 + "&apikey=" + api_key
        req_ob = requests.get(pre_url)
        result = req_ob.json()
        Exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        pre_monto = float(montos1.get())
        pre_nuevo_monto = round(pre_monto * Exchange_rate, 2)

        final_url = alpha_url + "&from_currency=" + var3 + "&to_currency=" + var2 + "&apikey=" + api_key
        nuevo_monto = round(pre_nuevo_monto * 4.51, 2)
        Formato = '{:0,.2f}'.format(nuevo_monto)
        Salida_monto.insert(0, str(Formato))
        return

        #En caso de que la moneda tenga convertibilidad directa en el sistema
    try:
     Exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
     monto = float(montos1.get())
     nuevo_monto = round(monto * Exchange_rate, 2)
     Formato = '{:0,.2f}'.format(nuevo_monto)
     Salida_monto.insert(0, str(Formato))
    except KeyError as e:
      #En caso de que la moneda NO tenga convertibilidad directa en el sistema
      pre_url = alpha_url + "&from_currency=" + var1 + "&to_currency=" + var3 + "&apikey=" + api_key
      req_ob = requests.get(pre_url)
      result = req_ob.json()
      Exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
      pre_monto = float(montos1.get())
      pre_nuevo_monto = round(pre_monto * Exchange_rate,2)

      final_url = alpha_url + "&from_currency=" + var3 + "&to_currency=" + var2 + "&apikey=" + api_key
      req_ob = requests.get(final_url)
      result = req_ob.json()
      Exchange_rate = float(result["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
      nuevo_monto = round(pre_nuevo_monto * Exchange_rate, 2)

      Formato = '{:0,.2f}'.format(nuevo_monto)
      Salida_monto.insert(0, str(Formato))
      return

#Limpiar Datos
def limpiar_salida():
    Salida_monto.delete(0, END)

#Obtener grafica del historial de volatilidad de la moneda
def Historial():
    if not ingresar_monto.get() or not Salida_monto.get():
        Mensaje_Error_3()
        return

    if Origen_menu.get() == "De" or Cambio_menu.get() == "Hacia":
        Mensaje_Error_2()
        return

    if Origen_menu.get() or Cambio_menu.get() == "BS":
        Mensaje_Error_4()
        return

    dias = simpledialog.askinteger(title="Dias", prompt="Ingrese cuantos dias desea ver el historial")
    if not dias:
        return

    # Declare variables
    amount = float(montos1.get())
    currency = data(variable1.get())
    converted_currency = data(variable2.get())
    amount_of_days = dias

    # sets the start date
    today_date = datetime.datetime.now()
    date_1year = (today_date - datetime.timedelta(days=1 * amount_of_days))

    # requests
    url = f'https://api.exchangerate.host/timeseries'
    payload = {'base': currency, 'amount': amount, 'start_date': date_1year.date(),
               'end_date': today_date.date()}
    response = requests.get(url, params=payload)
    responder_json = response.json()

    # create a dict to store data
    currency_history = {}
    rate_history_array = []

    for item in responder_json['rates']:
        current_date = item
        currency_rate = responder_json['rates'][item][converted_currency]
        currency_history[current_date] = [currency_rate]
        rate_history_array.append(currency_rate)

    # plot data
    plt.plot(rate_history_array)
    plt.ylabel(f'{amount} {currency} to {converted_currency}')
    plt.xlabel('Days')
    plt.title(f'current rate for {amount} {currency} to {converted_currency} is {Formato}')
    plt.show()

#Mensajes de Error
def Mensaje_Error_1():
    messagebox.showerror("Error de Validacion", "Ingrese algun valor numerico")


def Mensaje_Error_2():
    messagebox.showerror("Error de Validacion", "Ingrese alguna divisa")


def Mensaje_Error_3():
    messagebox.showerror("Error de Validacion", "No has convertido la divisa")

def Mensaje_Error_4():
    messagebox.showerror("Error de Validacion", "No hay informacion historica de esta divisa")



#Creacion Vetana Principal
ventana_principal = tk.Tk()
ventana_height = 587
ventana_width = 570

screen_width = ventana_principal.winfo_screenwidth()
screen_height = ventana_principal.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (ventana_height / 2))
y_cordinate = int((screen_height / 2) - (ventana_width / 2))

ventana_principal.geometry("{}x{}+{}+{}".format(ventana_height, ventana_width, x_cordinate, y_cordinate))

ventana_principal.resizable(width=False, height=False)

ventana_principal.title("Convertidor de Divisas")

#Insertar Imagenes y Botones
img_1 = tkinter.PhotoImage(file="Logo_programa.png")
label_imagen_1 = tkinter.Label(ventana_principal, image=img_1)
label_imagen_1.place(x=255, y=80)

imagen_covertir = PhotoImage(file="cambio.png")
Boton_Convertir = Button(ventana_principal, image=imagen_covertir, text="Convertir", font=("Helvetica", 16),
                         command=Calculo)
Boton_Convertir.place(x=130, y=450, width=100, height=80)

imagen_grafica = PhotoImage(file="grafica.png")
Boton_Historial = Button(ventana_principal, image=imagen_grafica, width=15, text="Historial", font=("Helvetica", 16),
                         command=Historial)
Boton_Historial.place(x=330, y=450, width=100, height=80)

montos1 = StringVar()
texto()
Entrada()
Menu_Listas()
ventana_principal.mainloop()

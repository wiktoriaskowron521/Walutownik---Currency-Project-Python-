import requests
import pandas as pd
from datetime import date
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib as mpl

#funkcja do pobierania danych z internetu o walutach:
def get_historical(base, symbol="PLN", start=None, end=None):
    # def od kiedy f będzie pob, jeśli nie zdefiniowane-od 01.01.br
    start = start or date.today().strftime("%Y-01-01")
    # analogicznie do startu, jesli nie zdef to do dnia obecnego
    end = end or date.today().strftime("%Y-%m-%d")

    respose = requests.get(
        f"https://api.exchangeratesapi.io/history"
        + f"?start_at={start}"
        + f"&end_at={end}"
        + f"&symbols={symbol}"
        + f"&base={base}"
    )  #pobieram dane wybrane przy wywołaniu funkcji

    rates = respose.json()['rates']  # przerabiam dane
    # robię translację "tabeli" żeby wiersze były pooznaczane datami
    df = pd.DataFrame(rates).transpose()
    df.columns = [base]  #definiuje dane z kursem danej waluty jako kolumnę
    return df.sort_index()  #sortuje dane datami, żeby mi się wypisywały chronologicznie

#funkcja do projektowania i rysowania wykresów danej funkcji
def wykres(df):
    symbol = df.columns[0]
    mpl.rcParams['lines.linewidth'] = 1  # oznaczanie grubości wykresu
    mpl.rcParams['lines.linestyle'] = '-'  # oznaczanie linii wykresu (ciągła)
    plt.plot(df.index, df[symbol])  # dane do wykres
    plt.title(f'Kurs waluty {symbol} w podany w PLN')  # opis wykres
    plt.xticks(df.index[::5], rotation=45, fontsize=7)  # uporządkowanie osi x
    plt.xlabel('Data')  # oznaczenie osi x
    plt.ylabel(f'Cena {symbol} w PLN')  # oznaczenie osi y wykresu
    plt.grid()
    plt.savefig(f'Kurs_waluty_{symbol}.jpg')  # zapisuję wykres na dysku
    plt.show()  # wyświetlam wykres

#funkcja korzysta z funkcji pobierającej dane+wykresy, potrzebne do "WYKRES"
def wykresy_waluty(symbol):
    df = pd.concat([get_historical(symbol)], axis=1) #pobieranie danych  
    wykres(df) #rysowanie wykresu

# DO WYKRESÓW (funkcje do przycisków):
def EUR(event):
    wykresy_waluty("EUR")

def USD(event):
    wykresy_waluty("USD")

def CHF(event):
    wykresy_waluty("CHF")

def GBP(event):
    wykresy_waluty("GBP")

def JPY(event):
    wykresy_waluty("JPY")

def NOK(event):
    wykresy_waluty("NOK")

def RUB(event):
    wykresy_waluty("RUB")

def SEK(event):
    wykresy_waluty("SEK")

def HUF(event):
    wykresy_waluty("HUF")

def CZK(event):
    wykresy_waluty("CZK")

def DKK(event):
    wykresy_waluty("DKK")

def TRY(event):
    wykresy_waluty("TRY")

#wprowadzanie jednostek waluty w nowym oknie, do przeliczenia ile jest warta dana ilość w innych walutach
def przelicznik(symbol):
    Label(root, text="Podaj ilość jednostek danej waluty:",background='white', foreground='dark green').grid()
    global liczba_Tf
    liczba_Tf=Entry(root) #wprowadzanie
    liczba_Tf.grid()
    
#podfunckja funkcji "przelicznik", przeliczanie walut i wyświetlanie efektów
    def przelicz_liczba():
        wood = tk.Toplevel(root) #nowe okno do wyświetlania efektów przeliczeń
        wood.title("Przeliczenie")
        wood.geometry("350x300")
        wood.title(f"Przelicznik {symbol}")
        wood.configure(background='Lightgoldenrod3')

        #pobieranie i sprowadzanie wpisanej przez użytkownika liczby do zmiennej typu int/float
        liczba = liczba_Tf.get()
        liczba=eval(liczba)

        #pobieranie danych potrzebnych to przeliczania (tzn kursu walut, gdzie bazą jest waluta "symbol")
        respose = requests.get(f"https://api.exchangeratesapi.io/latest?base={symbol}")
        rates = respose.json()['rates']

        #lista do wyświetlania efektów przeliczeń, jej wygląd, rozmiary,...
        l = ttk.Label(wood, text=f"Przelicznik {symbol}",background='Lightgoldenrod3', foreground='dark green')
        l.config(font=("Courier", 16))
        l.grid(padx=60, pady=10)
        listbox = tk.Listbox(wood, width=45)
        listbox.grid(sticky="news")
        scrollbar = tk.Scrollbar(wood, orient='vertical', command=listbox.yview)
        scrollbar.grid(row=1, column=6, sticky='ns')
        listbox.config(yscrollcommand=scrollbar.set)
        
        #wpisywanie danych do wcześniej utworzonej listy
        #x - symbole walut, rates[x] - wartości przypisane do symboli, 
        for x in rates:
            print(x, rates[x])
            a=liczba*rates[x]
            a=round(a,2)
            listbox.insert('end',str(liczba)+' ' + f"{symbol}" + ' = '+ str(a) + ' ' + x)

        #podfunckja do zapisywania efektów do excela
        def Excel1():
            csv_file = open('Rates_results.csv', "w")
            for x in rates:
                a=liczba*rates[x]   
                csv_file.write(str(x))
                csv_file.write(": ")
                csv_file.write(str(a))
                csv_file.write("\n")
            csv_file.close()
    
        #przycisk do funkcji - zapisywanie do pliku excel
        b=tk.Button(wood, text="Zapisz do Excela", width= 20, bg = "dark green", fg="khaki1", command = Excel1).grid()
        
        wood.mainloop()

    #przycisk do zapisywania wpisanej liczby jednostek waluty przez użytkownika, wywoływanie przelicznika i wypisywanie danych w liście
    Button(root, text="Zatwierdź", width = 12, bg = "dark green", fg="white", command=przelicz_liczba).grid()
    
    
#funkcja do działania KURSY WALUT:
#tworzenie okna 
def okno(symbol):
    boot = tk.Toplevel(root)
    boot.title("New Window")
    boot.geometry("300x300")
    boot.title(f"Kurs {symbol}")
    boot.configure(background='Lightgoldenrod3')

    #tworzenie listy, w której dane będą wypisywane i odpowiednie oznaczanie
    l = ttk.Label(boot, text=f"Kursy {symbol}",background='Lightgoldenrod3', foreground='dark green')
    l.config(font=("Courier", 16))
    l.grid(padx=60, pady=10)
    listbox = tk.Listbox(boot, width=45)
    listbox.grid(sticky="news")
    scrollbar = tk.Scrollbar(boot, orient='vertical', command=listbox.yview)
    scrollbar.grid(row=1, column=6, sticky='ns')
    listbox.config(yscrollcommand=scrollbar.set)

    #pobieranie odpowiednych danych korzystając z wcześniej pisanej funkcji get_historical()
    df = pd.concat([get_historical(symbol)], axis=1)

    #wpisywanie określonych danych do listy
    for i in range(1,31):
        listbox.insert('end',str(df.index[-i])+ ':  ' + str(df.values[-i][0]))

    #podfunkcja do zapisywania danych z listy w pliku Excel
    def Excel():
        csv_file = open('report_results.csv', "w")
        df = pd.concat([get_historical(symbol)], axis=1)
        for i in range(1,31):
            csv_file.write(str(df.index[-i])+ ':  ' + str(df.values[-i][0]))
            csv_file.write("\n")
        csv_file.close()
    
    b=tk.Button(boot, text="Zapisz do Excela", width= 20, bg = "dark green", fg="white", command = Excel)
    b.grid(column = 0, row = 7)

    boot.mainloop()

#DO KURSU WALUT:
def EUR2(event):
    przelicznik("EUR")

def USD2(event):
    przelicznik("USD")

def GBP2(event):
    przelicznik("GBP")

def CHF2(event):
    przelicznik("CHF")

def JPY2(event):
    przelicznik("JPY")

def NOK2(event):
    przelicznik("NOK")

def RUB2(event):
    przelicznik("RUB")

def SEK2(event):
    przelicznik("SEK")

def HUF2(event):
    przelicznik("HUF")

def CZK2(event):
    przelicznik("CZK")

def DKK2(event):
    przelicznik("DKK")

def TRY2(event):
    przelicznik("TRY")

#DO PRZELICZNIKA
def EUR1(event):
    okno("EUR")

def USD1(event):
    okno("USD")

def GBP1(event):
    okno("GBP")

def CHF1(event):
    okno("CHF")

def JPY1(event):
    okno("JPY")

def NOK1(event):
    okno("NOK")

def RUB1(event):
    okno("RUB")

def SEK1(event):
    okno("SEK")

def HUF1(event):
    okno("HUF")

def CZK1(event):
    okno("CZK")

def DKK1(event):
    okno("DKK")

def TRY1(event):
    okno("TRY")

#INTERFEJS GRAFICZNY
#tworzenie okna głównego (początkowego)
root = tk.Tk()
root.geometry("300x300")
root.title("Walutownik")

#pobieranie zdjęcia, które pojawi się w tle
response = requests.get("https://cdn.pixabay.com/photo/2016/04/25/23/53/euro-1353420_1280.jpg")
file = open("money.jpg", "wb")
file.write(response.content)

obrazek = Image.open("money.jpg")
photo = ImageTk.PhotoImage(obrazek)

#wstawianie obrazka jako tło okna początkowego(głównego)
label1 = tk.Label(image=photo)
label1.image = photo
label1.place(relx=0.5,
             rely=0.5,
             anchor='center')

#tworzenie wzorca wyglądu przycisków
s = ttk.Style()
s.map("C.TFrame",
      foreground=[("pressed", "red"), ("active", "pink")],
      background=[("pressed", "!disabled", "black"), ("active", "pink")])

s.map("C.TButton",
      foreground=[("pressed", "red"), ("active", "purple")],
      background=[("pressed", "!disabled", "black"), ("active", "purple")])

frame = ttk.Frame(root, style="C.TFrame")

l = ttk.Label(root, text="WALUTOWNIK",background='gray1', foreground='light yellow')
l.config(font=("Courier", 26))
l.grid(padx=50, pady=30)

#przyciski kierujące do kursu wybranej waluty
def Kursy(event):
    l = ttk.Label(root, text="Wybierz walutę", background='gray1', foreground='cornsilk2')
    l.config(font=("Courier", 14))
    l.grid()

    b1 = ttk.Button(frame, style='C.TButton', text="EUR")
    frame.grid()
    b1.grid(column=0, row=2)
    b1.bind("<Button-1>", EUR1)

    b2 = ttk.Button(frame, style='C.TButton', text="USD")
    frame.grid()
    b2.grid(column=1, row=2)
    b2.bind("<Button-1>", USD1)

    b3 = ttk.Button(frame, style='C.TButton', text="CHF")
    frame.grid()
    b3.grid(column=2, row=2)
    b3.bind("<Button-1>", CHF1)

    b4 = ttk.Button(frame, style='C.TButton', text="GBP")
    frame.grid()
    b4.grid(column=3, row=2)
    b4.bind("<Button-1>", GBP1)

    b5 = ttk.Button(frame, style='C.TButton', text="JPY")
    frame.grid()
    b5.grid(column=0, row=3)
    b5.bind("<Button-1>", JPY1)

    b6 = ttk.Button(frame, style='C.TButton', text="NOK")
    frame.grid()
    b6.grid(column=1, row=3)
    b6.bind("<Button-1>", NOK1)

    b7 = ttk.Button(frame, style='C.TButton', text="RUB")
    frame.grid()
    b7.grid(column=2, row=3)
    b7.bind("<Button-1>", RUB1)

    b8 = ttk.Button(frame, style='C.TButton', text="SEK")
    frame.grid()
    b8.grid(column=3, row=3)
    b8.bind("<Button-1>", SEK1)

    b9 = ttk.Button(frame, style='C.TButton', text="HUF")
    frame.grid()
    b9.grid(column=0, row=4)
    b9.bind("<Button-1>", HUF1)

    b10 = ttk.Button(frame, style='C.TButton', text="CZK")
    frame.grid()
    b10.grid(column=1, row=4)
    b10.bind("<Button-1>", CZK1)

    b11 = ttk.Button(frame, style='C.TButton', text="DKK")
    frame.grid()
    b11.grid(column=2, row=4)
    b11.bind("<Button-1>", DKK1)

    b12 = ttk.Button(frame, style='C.TButton', text="TRY")
    frame.grid()
    b12.grid(column=3, row=4)
    b12.bind("<Button-1>", TRY1)

#przyciski kierujące do przelicznika wybranej waluty
def Przelicznik(event):
    l = ttk.Label(root, text="Wybierz walutę",background='gray1', foreground='cornsilk2')
    l.config(font=("Courier", 14))
    l.grid()

    b1 = ttk.Button(frame, style='C.TButton', text="EUR")
    frame.grid()
    b1.grid(column=0, row=2)
    b1.bind("<Button-1>", EUR2)

    b2 = ttk.Button(frame, style='C.TButton', text="USD")
    frame.grid()
    b2.grid(column=1, row=2)
    b2.bind("<Button-1>", USD2)

    b3 = ttk.Button(frame, style='C.TButton', text="CHF")
    frame.grid()
    b3.grid(column=2, row=2)
    b3.bind("<Button-1>", CHF2)

    b4 = ttk.Button(frame, style='C.TButton', text="GBP")
    frame.grid()
    b4.grid(column=3, row=2)
    b4.bind("<Button-1>", GBP2)

    b5 = ttk.Button(frame, style='C.TButton', text="JPY")
    frame.grid()
    b5.grid(column=0, row=3)
    b5.bind("<Button-1>", JPY2)

    b6 = ttk.Button(frame, style='C.TButton', text="NOK")
    frame.grid()
    b6.grid(column=1, row=3)
    b6.bind("<Button-1>", NOK2)

    b7 = ttk.Button(frame, style='C.TButton', text="RUB")
    frame.grid()
    b7.grid(column=2, row=3)
    b7.bind("<Button-1>", RUB2)

    b8 = ttk.Button(frame, style='C.TButton', text="SEK")
    frame.grid()
    b8.grid(column=3, row=3)
    b8.bind("<Button-1>", SEK2)

    b9 = ttk.Button(frame, style='C.TButton', text="HUF")
    frame.grid()
    b9.grid(column=0, row=4)
    b9.bind("<Button-1>", HUF2)

    b10 = ttk.Button(frame, style='C.TButton', text="CZK")
    frame.grid()
    b10.grid(column=1, row=4)
    b10.bind("<Button-1>", CZK2)

    b11 = ttk.Button(frame, style='C.TButton', text="DKK")
    frame.grid()
    b11.grid(column=2, row=4)
    b11.bind("<Button-1>", DKK2)

    b12 = ttk.Button(frame, style='C.TButton', text="TRY")
    frame.grid()
    b12.grid(column=3, row=4)
    b12.bind("<Button-1>", TRY2)

#przyciski kierujące do wykresu wybranej waluty
def Wykresy(event):
    l = ttk.Label(root, text="Wybierz walutę",background='gray1', foreground='cornsilk2')
    l.config(font=("Courier", 14))
    l.grid(row=4)

    b1 = ttk.Button(frame, style='C.TButton', text="EUR")
    frame.grid()
    b1.grid(column=0, row=2)
    b1.bind("<Button-1>", EUR)

    b2 = ttk.Button(frame, style='C.TButton', text="USD")
    frame.grid()
    b2.grid(column=1, row=2)
    b2.bind("<Button-1>", USD)

    b3 = ttk.Button(frame, style='C.TButton', text="CHF")
    frame.grid()
    b3.grid(column=2, row=2)
    b3.bind("<Button-1>", CHF)

    b4 = ttk.Button(frame, style='C.TButton', text="GBP")
    frame.grid()
    b4.grid(column=3, row=2)
    b4.bind("<Button-1>", GBP)

    b5 = ttk.Button(frame, style='C.TButton', text="JPY")
    frame.grid()
    b5.grid(column=0, row=3)
    b5.bind("<Button-1>", JPY)

    b6 = ttk.Button(frame, style='C.TButton', text="NOK")
    frame.grid()
    b6.grid(column=1, row=3)
    b6.bind("<Button-1>", NOK)

    b7 = ttk.Button(frame, style='C.TButton', text="RUB")
    frame.grid()
    b7.grid(column=2, row=3)
    b7.bind("<Button-1>", RUB)

    b8 = ttk.Button(frame, style='C.TButton', text="SEK")
    frame.grid()
    b8.grid(column=3, row=3)
    b8.bind("<Button-1>", SEK)

    b9 = ttk.Button(frame, style='C.TButton', text="HUF")
    frame.grid()
    b9.grid(column=0, row=4)
    b9.bind("<Button-1>", HUF)

    b10 = ttk.Button(frame, style='C.TButton', text="CZK")
    frame.grid()
    b10.grid(column=1, row=4)
    b10.bind("<Button-1>", CZK)

    b11 = ttk.Button(frame, style='C.TButton', text="DKK")
    frame.grid()
    b11.grid(column=2, row=4)
    b11.bind("<Button-1>", DKK)

    b12 = ttk.Button(frame, style='C.TButton', text="TRY")
    frame.grid()
    b12.grid(column=3, row=4)
    b12.bind("<Button-1>", TRY)


#tworzenie przycisków w głównym oknie przekierowywujących do wybranych funkcji
wk = ttk.Button(frame, style='C.TButton', text="Wykres")
frame.grid()
wk.grid(column=2, row=2)
wk.bind("<Button-1>", Wykresy)

pr = ttk.Button(frame, style='C.TButton', text="Przelicznik")
frame.grid()
pr.grid(column=1, row=2)
pr.bind("<Button-1>", Przelicznik)

kr = ttk.Button(frame, style='C.TButton', text="Kurs walut")
frame.grid()
kr.grid(column=3, row=2)
kr.bind("<Button-1>", Kursy)

root.mainloop()
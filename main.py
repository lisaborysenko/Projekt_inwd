import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns
from palettable.colorbrewer.qualitative import Paired_12 
from matplotlib.colors import ListedColormap

data = pd.read_csv('menu[1].csv', encoding='utf-8')
data

data[data['Category'] == 'Breakfast'].groupby(['Item'])['Calories'].sum().plot(kind='bar', figsize=(10,5), cmap='rainbow')
plt.xlabel('Produkt')
plt.ylabel('Kalorie')
plt.title('Rozkład kalorii według produktu')
plt.show()

data.plot.scatter(x='Calories', y='Total Fat', figsize=(10,5), color='#41ecd4')
plt.xlabel('Kalorie')
plt.ylabel('Całkowita zawartość tłuszczu')
plt.title('Zależność między kaloriami a tłuszczem całkowitym')
plt.show()


data.rename(columns= {'Vitamin A (% Daily Value)':'Vitamin A', 'Vitamin C (% Daily Value)':'Vitamin C', 'Calcium (% Daily Value)':'Calcium', 'Iron (% Daily Value)':'Iron'}, inplace=True)
witaminy = data[['Category','Vitamin A','Vitamin C','Calcium','Iron']]
witaminy = witaminy.groupby(['Category']).mean()
print(witaminy)

plt.figure(figsize=(10,5))
sns.heatmap(witaminy , cmap='rainbow', annot=True, fmt='.1f')
plt.title('Rozkład składników odżywczych w podziału na kategorie')
plt.xlabel('Składniki odżywcze')
plt.ylabel('Kategoria')
plt.show()


kalorie = data[['Category','Calories']]
kalorie = kalorie.groupby(['Category']).mean().rename(columns={'Calories':'Średnia wartość kalorii'})
print(kalorie)


kalorie.plot.pie(y='Średnia wartość kalorii', figsize=(9, 9), cmap='rainbow', autopct='%1.1f%%')
plt.title('Średnia wartość kalorii w danej kategorii')
plt.legend(bbox_to_anchor=(1,1), loc="upper left")    #bbox_to_anchor - krotka współrzędnych x i y dla pozycji legendy. Współrzędne (1,1) ustawiają lewy górny róg legendy poza obszarem wykresu.
plt.ylabel('')
plt.show()


wart_cholesterol = data[['Item','Cholesterol']]
wart_cholesterol = wart_cholesterol.sort_values(by='Cholesterol', ascending=False)
wart_cholesterol.head(10)

def wartosc_cholesterolu(nazwa_item):
    cholesterol = data[data['Item']==nazwa_item]['Cholesterol']
    if cholesterol.empty:
        return 'Nie ma takiego produktu'
    return cholesterol.values[0]

print('Wartość cholesterolu wynosi: ', wartosc_cholesterolu(input("Wpisz nazwę produktu: ")))


def sklad_odzywczy(nazwa_item):
    data_item = data[data['Item']==nazwa_item]
    if data_item.empty:
        return 'Nie ma takiego produktu'
    kalorie = data_item['Calories'].values[0]
    weglowodany = (data_item['Carbohydrates'].values[0] / kalorie) * 100
    bialko = (data_item['Protein'].values[0] / kalorie) * 100
    tluszcz = (data_item['Total Fat'].values[0] / kalorie) * 100
    pie_data = [weglowodany, bialko, tluszcz]
    labels = ['Węglowodany', 'Białko', 'Tłuszcz']
#„%1.1f%%” służy do wyświetlania wartości w procentach z jednym przecinkiem dziesiętnym
    plt.pie(pie_data, labels=labels, autopct='%1.1f%%', colors=["#8000ff", "#00b5eb", "#41ecd4"]) 
    plt.title('Skład odżywczy - ' + nazwa_item)
    plt.show()

print(sklad_odzywczy(input('Wpisz nazwę produktu:')))


def piec_najzdrowszych_produktow():
    dane_produktu = data.groupby(['Item'])[['Vitamin A', 'Vitamin C', 'Iron', 'Calcium']].sum()
    dane_produktu['Poziom zawartości witamin i minerałów'] = (dane_produktu['Vitamin A'] + dane_produktu['Vitamin C'] + dane_produktu['Iron'] + dane_produktu['Calcium'])/4
    dane_produktu = dane_produktu.sort_values(by='Poziom zawartości witamin i minerałów', ascending=False)
    top_5 = dane_produktu.head(5)
    top_5.plot(kind='barh', y='Poziom zawartości witamin i minerałów', legend=False, color = '#81ffb4')
    plt.ylabel("Produkty")
    plt.xlabel("Poziom zawartości witamin i minerałów")
    plt.title("Top 5 Najzdrowszych Produktów")
    plt.show()

print(piec_najzdrowszych_produktow())

def top_produktow_z_najmniejsza_zaw_cukrow():
    cukier = data.sort_values(by='Sugars', ascending=False)
    top_10 = cukier.head(10)
    top_10 = top_10[['Item', 'Sugars']]
    top_10.plot(kind='barh', x='Item', y='Sugars', legend=False, color = "#4062fa")
    plt.xlabel("Cukier")
    plt.ylabel("Produkty")
    plt.title("Top 10 Produktów Z Najmniejszą Zawartością Cukrów")
    plt.show()
print(top_produktow_z_najmniejsza_zaw_cukrow())

def srednia_kalorycznosc(data):
    return np.mean(data['Calories'])
srednia_kalorycznosc(data)




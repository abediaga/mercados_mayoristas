#!/usr/bin/env python
# coding: utf-8

# In[128]:


import json
import urllib.request
import pandas as pd
import datetime
import random
import matplotlib.pyplot as plt


# In[129]:


url_mercabilbao_json = "https://github.com/abediaga/mercados_mayoristas/raw/master/mercabilbao_json/mercabilbao_dict_mercabilbao.json"
url_anosemanas_json = "https://github.com/abediaga/mercados_mayoristas/raw/master/mercabilbao_json/mercabilbao_dict_anosemanas.json"

with urllib.request.urlopen(url_mercabilbao_json) as url:
    mercabilbao_json = json.loads(url.read().decode())

with urllib.request.urlopen(url_anosemanas_json) as url:
    anosemanas_json = json.loads(url.read().decode())
    


# In[130]:


def get_semanas_anos(anos):
    anosemanas = {}
    for ano in anos:
        anosemanas[ano] = anosemanas_json[ano]
    return anosemanas

def get_dataframe_mercabilbao(anos_seleccionados, mercado_seleccionado, informacion_seleccionada, productos_seleccionados, indicador_seleccionado):
    #Obtenemos las semanas de los años señalados
    anosemanas = {}
    for ano in anos_seleccionados:
        anosemanas[ano] = anosemanas_json[ano]
    
    df_producto = pd.DataFrame()
    for ano, semanas in anosemanas.items():
        for semana in semanas:
            fecha = datetime.datetime.strptime(ano +"-"+ semana, '%Y-%m-%d')
            temp = pd.DataFrame()
            for producto in productos_seleccionados:
                if (producto in mercabilbao_json[ano][semana][mercado_seleccionado][informacion_seleccionada].keys()) :
                    df2 = pd.DataFrame([] , columns=[fecha])
                    df2.loc[producto] = [mercabilbao_json[ano][semana][mercado_seleccionado][informacion_seleccionada][producto][indicador_seleccionado]]
                    temp = pd.concat([df2, temp])
            df_producto = pd.concat([temp, df_producto], axis=1)

    df_producto = df_producto.reindex(columns=sorted(df_producto.columns))    
    
    return(df_producto)

def plot_dataframe_mercabilbao(df_mercabilbao):
    ax = plt.gca()

    for producto in df_mercabilbao.index:
        #print(item)
        dff_producto.loc[producto].T.plot(kind='line', color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)), label=producto, ax=ax, figsize=(12,6))

    plt.ylabel('Precio más frecuente por Kg')
    ax.legend()
    plt.show()


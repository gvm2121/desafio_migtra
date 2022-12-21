import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



with open("data1.json","r") as js:
    var_total = []
    var2_total = []
    var1_reg4_total = []
    d = json.loads(js.read())
    for r in d:
        if r["name"]=="Region4":
            for m in r["children"]:
                var1_reg4 = [int(t["values"]["var1"]) for t in m["children"]]
                var1_reg4_total += var1_reg4
        for s in r["children"]:
            var1 = [int(t["values"]["var1"]) for t in s["children"]]
            var_total += var1
            if s["name"]=="Provincia2":
                var2 = [int(t["values"]["var2"]) for t in s["children"]]
                var2_total += var2
    print(f"El valor máximo para la variable var1 en la region 4 es {max(var1_reg4_total)}")
    print(f"El promedio de la variable var_1 es {sum(var_total)/len(var_total)}")
    print(f"La suma de la variable var2 para la provincia 2 es {sum(var2_total)}")


with open("data2.json","r") as js:
    datos = json.load(js)
    
    for dato in datos:
        dato["waiting_time"]=datetime.datetime.fromisoformat(dato["dt_out"])-datetime.datetime.fromisoformat(dato["dt_in"])
    zona_a = list(filter(lambda x:x["zone"]=='A',datos))
    zona_b = list(filter(lambda x:x["zone"]=='B',datos))
    procesos_zona_a = len(zona_a)
    procesos_zona_b = len(zona_b)
    tiempo_espera_zona_a = sum([int(x["waiting_time"].seconds) for x in zona_a])/ procesos_zona_a
    tiempo_espera_zona_b = sum([int(x["waiting_time"].seconds) for x in zona_b])/ procesos_zona_b
    print(f"el timpo de espera para la zona A es de {str(datetime.timedelta(seconds=tiempo_espera_zona_a))}")
    print(f"el timpo de espera para la zona B es de {str(datetime.timedelta(seconds=tiempo_espera_zona_b))}")
    #datos_pd = pd.read_json(dato)
    #print(datos_pd.sample())
    
    #Porcentaje de ciclos de faena que incluyó area de trabajo tipo 2
    
    incluye_zona_2 = list(filter(lambda x:"2" in x["zone"],datos))
    print("El porcentaje de ciclos de faenas que incluyen el ciclo 2 son {}%".format((len(incluye_zona_2)/len(datos))*100))


#Cuál es el camión con más tiempo de espera en total?
datos_pd = pd.read_json("data2.json")
datos_pd["dt_out"] = pd.to_datetime(datos_pd["dt_out"])
datos_pd["dt_in"] = pd.to_datetime(datos_pd["dt_in"])
datos_pd["waiting_time"] = datos_pd["dt_out"] - datos_pd["dt_in"]
datos_pd["day_of_week"] = datos_pd["dt_in"].dt.dayofweek
df3 = datos_pd.groupby("asset")["waiting_time"].sum().sort_values(ascending=False)
print(df3)
print("El camión con más tiempo de espera acumulada total es el camión M11")


#Qué día de la semana se genera la mayor espera?
df4 = datos_pd.groupby("day_of_week")["waiting_time"].mean().sort_values(ascending=False)
print(df4)
print("El dia de la semana que hay más promedio de espera es el dia jueves")

#df5 = datos_pd[["dt_in","waiting_time"]].sort_values("dt_in",ascending=False)
plt.plot(datos_pd["dt_in"].dt.date,datos_pd["waiting_time"].dt.seconds)
plt.axhline(y=np.nanmean(datos_pd["waiting_time"].dt.seconds))

#df5.plot.line(df5)
plt.show()
#se ve que el comportamiento de los tiempos de espera tiene
#un tipo de "diente de sierra" haciendo los máximos en los días jueves según el análisis anterior
#hay que, para profundizar el análisis, hay que hacer un análisis en primerda diferenciación en series de tiempo para 
#poder entender las variaciones de los tiempos de espera de los camiones.
#A simple vista, no se ve un aumento en los tiempos de espera de los camiones
#La media del grafico se mantiene estable, lo que re afirma que el promedio de espera no ha aumentado
#con confundir el promedio de una serie de tiempo con el promedio de una variable en corte transversarl que pueden variar.


    
    
    

    
      
    
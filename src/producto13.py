'''
MIT License

Copyright (c) 2020 Sebastian Cornejo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pandas as pd


def producto13(producto5, producto10):
    print('generating producto13')
    df_recuperados = pd.read_csv(producto5)
    df_producto13 = df_recuperados
    df_fallecidos = pd.read_csv(producto10)
    df_fallecidos_total = pd.Series(df_fallecidos.sum())
    df_fallecidos_total = df_fallecidos_total[1:].transpose()
    df_producto13 = df_producto13.append(df_fallecidos_total, ignore_index=True)
    df_producto13.loc[1, 'Fecha'] = 'Fallecidos'
    return df_producto13

def prod13():
    import glob
    import re

    regions_id = {"Arica y Parinacota": 15, "Tarapacá": 1, "Antofagasta": 2, "Atacama": 3,
                  "Coquimbo": 4, "Valparaíso": 5, "Metropolitana": 13, "O’Higgins": 6,
                  "Maule": 7, "Ñuble": 16, "Biobío": 8, "Araucanía": 9, "Los Ríos": 14,
                  "Los Lagos": 10, "Aysén": 11, "Magallanes": 12
                  }

    regions_pob = {"Arica y Parinacota": 252110, "Tarapacá": 382773, "Antofagasta": 691854, "Atacama": 314709,
                   "Coquimbo": 836096, "Valparaíso": 1960170, "Metropolitana": 8125072, "O’Higgins": 991063,
                   "Maule": 1131939, "Ñuble": 511551, "Biobío": 1663696, "Araucanía": 1014343, "Los Ríos": 405835,
                   "Los Lagos": 891440, "Aysén": 107297, "Magallanes": 178362
                   }

    data = []
    for file in glob.glob("../output/producto4/*.csv"):
        date = re.search("\d{4}-\d{2}-\d{2}", file).group(0)
        df = pd.read_csv(file, sep=",", encoding="utf-8")
        df.columns = df.columns.str.replace(" ", "")

        # Estandarización de nombres de columnas
        if "Casosfallecidos" in list(df):
            df = df.rename(columns={"Casosfallecidos": "Fallecidos"})

        if "Fallecidos" not in list(df):
            df["Fallecidos"] = 0

        if "Región" in list(df):
            df = df.rename(columns={"Región": "Region"})

        df["Fecha"] = date

        df = df.rename(columns={"Casosnuevos": "Nuevos Casos",
                                "Casostotales": "Casos Confirmados"})

        # Elimina la filas "total"
        df = df[df["Region"] != "Total"]

        # Corrige un error de la data
        if date == "2020/03/03":
            df.loc[df["Region"] == "Maule", ["Nuevos Casos"]] = 1
        data.append(df)

    data = pd.concat(data)
    print(data.columns)
    # Borra columnas innecesarias
    data = data.drop(columns={"%Casostotales**", "Casosrecuperados"})

    # Soluciona problemas con los nombres de regiones
    data["Region"] = data.apply(lambda x: " ".join(x["Region"].split()), axis=1)
    data["Region"] = data["Region"].replace(
        {"Tarapaca": "Tarapacá", "Valparaiso": "Valparaíso", "Metropolita": "Metropolitana",
         "O'Higgins": "O’Higgins", "Nuble": "Ñuble", "Biobio": "Biobío", "Los Rios": "Los Ríos",
         "Araucania": "Araucanía", "Aysen": "Aysén", "Arica y Paricota": "Arica y Parinacota"
         })
    # Crea el identificador regional
    data["Region ID"] = data["Region"].replace(regions_id)

    # Crea columna con la población regional
    data["Poblacion"] = data["Region"].replace(regions_pob).astype(int)

    output = data[['Region', 'Fecha', 'Nuevos Casos']]
    return(output)

if __name__ == '__main__':

    #df = producto13('../output/producto5/recuperados.csv', '../output/producto10/FallecidosEtario.csv')
    #df.to_csv('../output/producto13/recuperados_fallecidos.csv', index=False)
    df = prod13()
    #df.to_csv('../output/producto13/casosNuevos.csv', index=False)
    print(df)
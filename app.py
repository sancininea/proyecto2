#################################################################
#
# Importar bibliotecas
#
#################################################################
from flask import Flask, render_template, Markup, request
from p_tools import analysis_func, fetch_data
import pandas as pd
import glob
from sqlalchemy import create_engine

#################################################################
#
# Inicio de aplicación
#
#################################################################
app=Flask(__name__)

#################################################################
#
# Página principal Index.html
#
#################################################################
@app.route("/")
def index():
    graph_data = fetch_data()
    texto = "["
    bubbles = "["
    contador = 0

    for d in graph_data.values.tolist():
        texto = texto + '{ name: "' + d[1] + '",'
        texto = texto + ' water: ' + str(d[2]) + ','
        texto = texto + ' alcohol: ' + str(d[3]) + ','
        texto = texto + ' bmi: ' + str(d[4]) + ','
        texto = texto + ' co2: ' + str(d[5]) + ','
        texto = texto + ' fertilizer: ' + str(d[6]) + ','
        texto = texto + ' population: ' + str(d[7]) + ','
        texto = texto + ' sugar: ' + str(d[8]) + ','
        texto = texto + ' tobacco: ' + str(d[9]) + ','
        texto = texto + ' urban: ' + str(d[10]) + ','
        texto = texto + ' work: ' + str(d[11]) + ','
        texto = texto + ' lat: ' + str(d[12]) + ','
        texto = texto + ' lon: ' + str(d[13]) + ','
        texto = texto + ' contador: ' + str(contador) 
        texto = texto + '},'

        contador +=1
        bubbles = bubbles + '['

        if d[2] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Access to drinking water",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[2]))
            bubbles = bubbles + ' },'
        if d[3] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Alcohol consumption",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[3]))
            bubbles = bubbles + ' },'
        if d[4] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Body Mass Index",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[4]))
            bubbles = bubbles + ' },'
        if d[5] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "CO2 emission",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[5]))
            bubbles = bubbles + ' },'
        if d[6] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Fertilizer application",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[6]))
            bubbles = bubbles + ' },'
        if d[7] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Population growth",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[7]))
            bubbles = bubbles + ' },'
        if d[8] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Sugar consumption",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[8]))
            bubbles = bubbles + ' },'
        if d[9] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Tobacco consumption",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[9]))
            bubbles = bubbles + ' },'
        if d[10] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Urban majority",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[10]))
            bubbles = bubbles + ' },'
        if d[11] > 0:
            bubbles = bubbles + '{'
            bubbles = bubbles + 'country: "' + d[1] + '",' 
            bubbles = bubbles + ' name: "Working hours",' 
            bubbles = bubbles + 'coefficient: ' + str("{0:.4f}".format(d[11]))
            bubbles = bubbles + ' }'

        bubbles = bubbles + '],'

    texto = texto + ']'
    bubbles = bubbles + ']'
    texto = Markup(texto)
    bubbles = Markup(bubbles)

    return render_template("index.html", graph_data=texto, bubbles=bubbles)

#################################################################
#
# Página secundaria
#
#################################################################
@app.route("/rdata")
def rdata():
    return render_template("tabla.html")

#################################################################
#
# Carga de archivos a base de datos
#
#################################################################
@app.route("/load")
def get_data():
    filesList = glob.glob("resources\data\*.csv")
    first = True
    # Loop thru files
    for files in filesList:
        # Set the column name
        colName = files[15:len(files)-4]
        if first:
            df_final = analysis_func(files, "Resources/LE/life_expectancy.csv", "2017", colName.lower()).fillna(0)
            first = False
        else:
            df_file = analysis_func(files, "Resources/LE/life_expectancy.csv", "2017", colName.lower())
            df_final = pd.merge(df_final, df_file, how = "left").fillna(0)
    # Save results in database
    engine = create_engine('postgresql://postgres:sa@localhost:5432/project2')
    df_final.to_sql('countrydata', engine)

    return "Done"

#################################################################
#
# Manejador de error 404
#
#################################################################
@app.errorhandler(404)
def page_not_found(e):
    return "Página no encontrada"

#################################################################
#
# Ejecución de aplicación
#
#################################################################
if __name__=="__main__":
    app.run(debug=True)
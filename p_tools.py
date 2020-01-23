#####################################################################################
#
# Import general
#
#####################################################################################
from sqlalchemy import create_engine
import glob
import pandas as pd
from scipy.stats import pearsonr


#####################################################################################
#                                                                                   #
# Function XXXXXXX                                                                  #
# This function xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.             #
#                                                                                   #
# Parameters:                                                                       #
# filesList - An array of strings that contains the names of the files              #
# retrieve. Use filesList = glob.glob(".\<folder name>\*.xml") to set this list.    #
#                                                                                   #
# Returns: xmls - List of dictionaries with the data to store. The lenght varies,   #
# the files can have different data.                                                #
#                                                                                   #
#####################################################################################
def fetch_data():

    engine = create_engine('postgresql://postgres:sa@localhost:5432/project2')
    conn = engine.connect()

    query = '''
        select countrydata.*, lat, lon 
        from countrydata inner join coord_countries
        on "Country" = coord_countries.country
    '''
    result_qry = pd.read_sql(query, conn)
    
    return result_qry

#####################################################################################
#                                                                                   #
# Function Alan                                                                     #
# Esta función recibe un archivo base y un folder de archivos a utilizar para       #
# determinar si están correlacionados y obtener su coeficiente de correlación       #
#                                                                                   #
# Parameters:                                                                       #
# data_path - folder que contiene los archivos a comparar                           #
# origin - Archivo principal sobre el que se hará la comparación.                   #
# yy - año base con el que se buscará la correlación                                #
# cause - nombre del set de datos con el que se compara el archivo principal        #
#                                                                                   #
# Returns: df - Un dataframe con los datos del coeficiente.                         #
#                                                                                   #
#####################################################################################
def analysis_func(data_path, origin, yy, cause):

    life_expectancy = pd.read_csv(
        origin, encoding="ISO-8859-1")[["Countries", yy]]

    #Change column names for clarity
    life_expectancy = life_expectancy.rename(
        columns={"country": "Countries", yy: "Expectancy 2017"})

    try:
        data = pd.read_csv(data_path)
    except:
        try:
            data = pd.read_csv(data_path, encoding="ISO-8859-1")
        except:
            print("Error: It was not possible to read the CSV file.")
            return


    #Inner join to ensure all the countries are the same in both dataframes
    joint_data = life_expectancy.merge(data, on="Countries", how="inner")

    # Create empty lists to keep track of values
    data_dict = []

    # Get all the years we will be using for our analysis
    years = joint_data.columns[2:].tolist()

    cols_temp = ["Countries"]
    cols_temp += years

    joint_data = joint_data[cols_temp]

    # Get the coefficients and the p-values
    for row in joint_data.iterrows():
        coeffs = []
        p_values = []
        for i in range(1, len(years) - 10):
            coeff, p = pearsonr(row[1].iloc[-5:].to_list(),
                                row[1].iloc[i:i+5].to_list())
            coeffs.append(coeff)
            p_values.append(p)
        data_dict.append({
            "country": row[1].iloc[0],
            cause: abs(sum(coeffs) / len(coeffs))
        })

    df = pd.DataFrame(data_dict)

    return df
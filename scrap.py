import requests #realizar peticiones http
from bs4 import BeautifulSoup #procesar html

import xml.etree.ElementTree as ET #procesar XML


"""
    Este codigo obtiene la información de la cantidad de hombres y mujeres la suma total de personas en un estado y municipio
    de la pagina del Inegi mediante Web Scraping

    Genera 2 archivos csv con la info estados(id_estado,nombre_estado) municipio(id_estado,nombre_municipio) 
    Muestra en consola la informacion de cantidad de hombres y mujeres en cada estado asi como las de cada municipio

    Nota(solo se debe ejecutar 1 vez ya que si se ejecuta 2 se sobrescriben los datos en los archivos.csv)

    Author: Paul Santana
"""

# URL de la página web que deseas scrapear
url = 'https://www.inegi.org.mx/widgets/cpv/2020/poblacion.html'

# Realizar una solicitud GET a la URL
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de respuesta 200)
if response.status_code == 200:
    # Parsear el contenido de la página con BeautifulSoup
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    select_estado = soup.find(id='edo')
    select_municipio = soup.find(id='mun')
    
    if select_estado:#si encontramos el select de de estado entonces podemos recorrer los elementos
        opciones = select_estado.find_all('option')
        for a in opciones:
            #print(a)
            if str(a['value']) != '00' :
                print('----',a['value'],' ',a.text)
                print()
                peticion = requests.get('https://www.inegi.org.mx/widgets/cpv/2020/recursos/INEGIWgEst_cpv2020_'+ a['value'] +'.xml')
                archivo =  open('estados.csv', 'a')
                archivo.write(str(int(a['value'])) + ',' + a.text +"\n")
                archivo.close()

                if peticion.status_code == 200:
                    # Parsear el XML
                    #print(peticion.text)
                    peticion.encoding = 'UTF-8'  # Reemplaza 'utf-8' con la codificación correcta

                    #quitamos la cabecera (que es la que indica la version del xml'ya que con ella no funciona el metodo')
                    lineas = peticion.text.splitlines()[1:]

                    # Unir las líneas nuevamente en un solo string
                    resultado = '\n'.join(lineas)

                    # Parsear el XML desde la cadena
                    root = ET.fromstring(resultado)

                    # Recorrer los elementos
                    for entidad in root.findall('entidad'):
                        nombre_entidad = entidad.get('nombre')
                        total = entidad.get('Total')
                        hombres = entidad.get('Hombres')
                        mujeres = entidad.get('Mujeres')
    
                        print(f'Entidad: {nombre_entidad}, Total: {total}, Hombres: {hombres}, Mujeres: {mujeres}')
    
                        for municipio in entidad.findall('municipio'):
                            nombre_municipio = municipio.get('nombre')
                            total_municipio = municipio.get('Total')
                            hombres_municipio = municipio.get('Hombres')
                            mujeres_municipio = municipio.get('Mujeres')
                            print(f'Municipio: {nombre_municipio}, Total: {total_municipio}, Hombres: {hombres_municipio}, Mujeres: {mujeres_municipio}')
                            archivo2 =  open('municipios.csv', 'a')
                            archivo2.write(str(int(a['value'])) + ',' + nombre_municipio +'\n')
                        
                print('-----------')
else:
    print('La solicitud no fue exitosa. Código de respuesta:', response.status_code)

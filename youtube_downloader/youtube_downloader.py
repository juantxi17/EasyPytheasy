#Script en Python que permite la descarga de vídeos de YouTube así como su conversión a formatos de audio.
#Autor: ea1fsc

#Importación de las librerías necesarias
from pytube import YouTube #Librería para la API de YouTube.
from urllib.parse import urlparse #Librería para la comprobación de URLs.
import requests #Librería para comprobar que la URL proporcionada es accesible.
import platform
import os
import sys

#Definiciones
def introducir_url(): #Función que solicita al usario que introuzca la URL del vídeo y comprueba si esta está vacía o no.
	url=input("\nIntroduzca el URL del vídeo a procesar: ")
	while not bool(url):
		url=input("Introduzca el URL del vídeo a procesar: ")
	return url

def confirmar_url(enlace): #Función que se utiliza para confirmar que la URL es correcta.
	print("\nLa URL es: ", enlace)
	res=input("Por favor, confirme si la URL es correcta (y=yes/sí;n=no): ")
	while not bool(res):
		print("\nLa URL es: ", enlace)
		res=input("Por favor, confirme si la URL es correcta (y=yes/sí;n=no): ")
	if res=='y':
		return True
	elif res=='n':
		return False
	elif res!='y' and res!='n'and res!=None:
		res=None
		print("\nError catastrófico: respuesta no válida\n")

def comprobar_url(enlace): #Función que comprueba si la cadena introducida es una URL de verdad.
	try:
		resultado = urlparse(enlace)
		if resultado.netloc!='www.youtube.com' or not ('/watch' in resultado.path) :
			print("\nERROR: La URL proporcionada no corresponde a un vídeo de youtube.")
			return False
		return all([resultado.scheme, resultado.netloc])
	except ValueError:
		print("\nERROR: La URL proporcionada no es válida")
		return False

def es_url_accesible(enlace, validacion): #Comprueba que la URL proporcionada es accesible.
	try:
		if not  validacion:
			return False
		respuesta=requests.get(enlace)
		return respuesta.status_code==200
	except requests.RequestException:
		print("\nERROR: La URL proporcionada no es accesible.")
		return False

def devuelve_indice(stream_elegido,streams):  #Devuelve el indice del elemento en la lista
	if not bool(stream_elegido):
		return None
	indice=streams.index(stream_elegido)
	return (indice+1)

def obtiene_datos(video):
	if not bool(video):
		return None
	data=[None]*5
	data[0]=video.title
	data[1]=video.author
	data[2]=video.channel_url
	data[3]=video.publish_date
	seg=video.length
	horas=seg//3600
	min=(seg%3600)/60
	if horas> 0:
		data[4]=f"{horas} hora{'s' if horas != 1 else ''}"
	elif min>0:
		data[4]=f" {min} minuto{'s' if min != 1 else ''}"
	else:
		data[4]=f" {seg} segundo{'s' if seg != 1 else ''}"
	return data

def muestra_datos(data):
	if not bool(data):
		print("\nError: El vídeo no es accesible.")
		return False
	print("\nLos datos del vídeo son: ")
	print("Título: ", data[0])
	print("Autor: ", data[1])
	print("URL del autor: ", data[2])
	print("Fecha de publicación: ", data[3])
	print("Duración: ", data[4])
	

def muestra_streams(streams):  #Imprime en pantalla todos los streams disponibles
	print("Características del vídeo: ")
	for i, stream in enumerate(streams, start=1):
		print(f"\nStream {i}: ")
		print(f"Resolución: {stream.resolution}")
		print(f"Formato: {stream.mime_type}")
		print(f"Tamaño: {round(stream.filesize_mb)} MB")
		print(f"Tipo: {'Video+Audio' if stream.includes_audio_track and stream.includes_video_track else 'Audio' if stream.includes_audio_track else 'Video'}")

def muestra_stream(indice,stream):
	if not bool(indice):
		return False
	print("Características del vídeo: ")
	print(f"\nStream : ", indice)
	print(f"Resolución: {stream.resolution}")
	print(f"Formato: {stream.mime_type}")
	print(f"Tamaño: {round(stream.filesize_mb)} MB")
	print(f"Tipo: {'Video+Audio' if stream.includes_audio_track and stream.includes_video_track else 'Audio' if stream.includes_audio_track else 'Video'}")
	return True

def seleccionar_stream(streams): #Función que permite elegir el stream deseado para descargar.
	seleccion=input("\nPor favor, selecciona el vídeo que deseas descargar con el número que aparece en la lista anterior: ")
	try:
		seleccion.isdigit()
		seleccion=int(seleccion)-1
		if 0<=seleccion<len(streams):
			return streams[seleccion]
		else:
			print("\nERROR: El vídeo seleccionado no se encuentra disponible")
			return None
	except:
		print("\nERROR: La selección no es válida")
		return None

def validar_respuesta():
	respuesta=input("Estás seguro de que quieres descargar ese stream? (y=yes/sí;n=no)")
	if respuesta=='y':
		return True
	elif respuesta=='n':
		return False
	elif respuesta !='y' and respuesta!='n':
		print("\nERROR:Respuesta no válida")
		return None

def escribe_nombre(stream):
	nombre=input("Introduce el nombre para el archivo descargado. Dejar en blanco para usar por defecto: " )
	if not bool(nombre):
		return stream.default_filename
	return nombre

def seleccionar_directorio():
	dir=input("Introduce el directorio para descargar el archivo. Dejar en blaco para guardar en Descargas: ")
	OS=platform.system()
	if not bool(dir):
		if OS=="Linux":
			home=os.getenv("HOME")
			dir=carpeta_descargas = os.path.join(home, "Descargas") if os.path.exists(os.path.join(home, "Descargas")) else os.path.join(home, "Downloads")
			return dir
		elif OS=="Windows":
			dir=os.path.join(os.path.expanduser("~"), "Descargas") if os.path.exists(os.path.join(os.path.expanduser("~"), "Descargas")) else os.path.join(os.path.expanduser("~"), "Downloads")
			return dir
		elif OS=="Darwin":
			dir=os.path.join(os.path.expanduser("~"), "Descargas") if os.path.exists(os.path.join(os.path.expanduser("~"), "Descargas")) else os.path.join(os.path.expanduser("~"), "Downloads")
			return dir
		else:
			print("ERROR: Sistema Operativo no soportado.")
			return None

def comprobar_descarga(stream, file_path, directorio):
	dir=directorio
	if os.path.exists(os.path.join(dir, os.path.basename(file_path))):
		return True
	else:
		return False
	
#Solicitamos al usuario que introduzca el url del vídeo y realizamos las comprobaciones oportunas.

url=introducir_url()
val=comprobar_url(url)
acc=es_url_accesible(url,val)
yt=YouTube(url) #Obtenemos el vídeo de Youtube
datos=obtiene_datos(yt)
muestra_datos(datos)
ans=confirmar_url(url)
while not (bool(ans) and val and acc and bool(yt)):
	url=introducir_url()
	val=comprobar_url(url)
	acc=es_url_accesible(url,val)
	yt=YouTube(url) #Obtenemos el vídeo de Youtube
	datos=obtiene_datos(yt)
	muestra_datos(datos)
	ans=confirmar_url(url)

#Procesado de los streams
streams_filtrados=yt.streams.filter().order_by('resolution').desc() #Realizamos un filtrado de los posibles streams que contienen el audio y el vídeo (Progessive=True)
muestra_streams(streams_filtrados)
selec=seleccionar_stream(streams_filtrados)
ind=devuelve_indice(selec,streams_filtrados)
if muestra_stream(ind,selec):
	val=validar_respuesta()
while not (bool(selec) and val):
	selec=seleccionar_stream(streams_filtrados)
	ind=devuelve_indice(selec,streams_filtrados)
	if muestra_stream(ind,selec):
		val=validar_respuesta()

#Descarga del video
nombre=escribe_nombre(selec)
dir=seleccionar_directorio()
selec.download(output_path=dir,filename=nombre)
comprobacion=comprobar_descarga(selec,nombre,dir)
print("Descarga completada -> +20 XP")
while not bool(comprobacion):
	print("Error en la descarga del vídeo. Probando de nuevo...")
	nombre=escribe_nombre(selec)
	dir=seleccionar_directorio()
	selec.download(output_path=dir,filename=nombre)
	comprobacion=comprobar_descarga(selec,nombre,dir)
	contador+=1
	if contador > 3:
		print("No se ha podido descargar el archivo seleccionado. Pruebe con otro.")
		sys.exit(1)
exit(0)

#Instagram Downloader. Allows you to download photos, vídeos and stories from Instagram using a URL
#Author: ea1fsc - 03/03/2024

#Importing libraries
import instaloader
from urllib.parse import urlparse
import requests
import platform
import os
import sys
import re

#Definición de funciones y variables

def introducir_url(): #Función que solicita al usario que introuzca la URL del vídeo y comprueba si esta está vacía o no.
	url=input("\nIntroduzca la URL de la foto o del  vídeo a procesar: ")
	while not bool(url):
		url=input("Introduzca la  URL de la foto o vídeo a procesar: ")
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

patron_shortcode=r"/p/([^/?]+)"

def comprobar_url(enlace): #Función que comprueba si la cadena introducida es una URL de verdad.
	try:
		resultado = urlparse(enlace)
		if resultado.netloc!='www.instagram.com' or not ('/p/' in resultado.path) :
			print("\nERROR: La URL proporcionada no corresponde a un post de Instagram.")
			return False
		codigo=re.search(patron_shortcode,enlace)
		return codigo.group(1)
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

#Código main
url_post=introducir_url()
val=comprobar_url(url_post)
print(val)
loader=instaloader.Instaloader()
loader.download_post(val, target='~/Descargas')

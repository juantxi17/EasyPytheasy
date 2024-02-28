#This script allows you to check if your Python instalation is able to execute the youtube_downloader code

import subprocess

def check_libraries(librerias):
	lib=0
	for libreria in librerias:
		try:
			__import__(libreria)
			print(f"La libreria '{libreria}' se encuenta instalada.")
		except ImportError:
			print(f"\nLa librería '{libreria}' no se encuentra instalada")
			res=input("¿Quiere instalarla automáticamente? (y=yes/sí;n=no) NOTA: Si elige 'no' debería instalarla manualmente: ")
			if res=='y':
				subprocess.check_call(["pip","install",libreria])
				print(f"\nLa libreria {libreria} ha sido instalada")
			elif res=='n':
				print(f"\nDeberá instalarla manualmente mediante 'pip install {libreria}\n'")
			else:
				print("\nERROR:Respuesta no válida")
				res=None
			while res==None:
				res=input("¿Quiere instalarla automáticamente? (y=yes/sí;n=no) NOTA: Si elige 'no' debería instalarla manualmente: ")
				if res=='y':
					subprocess.check_call(["pip","install",libreria])
					print(f"La libreria '{libreria}' ha sido instalada")
				elif res=='n':
					print(f"Deberá instalarla manualmente mediante 'pip install {libreria}\n'")
				else:
					print("\nERROR:Respuesta no válida")
					res=None
	print("Su instalación cumple las dependencias necesarias para ejecutar 'youtube_downloader'")

libraries=["pytube", "urllib.parse","requests"]
check_libraries(libraries)

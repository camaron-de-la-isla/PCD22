import socket
import threading
import sys
import pickle
import os
from os import remove
from os import path

class Servidor():
#El servidor se inicializa y pregunta al usuario por el puerto
	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		self.clientes = []
		print('\nSu IP actual es : ',socket.gethostbyname(host))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port)))
		self.s.listen(128)
		self.s.setblocking(False)
#Se borran los dos ficheros que crea el programa en el caso de que existan
		if path.exists("lista_de_usuarios.txt"):
			remove('lista_de_usuarios.txt')
		open("lista_de_usuarios.txt", "a")

		if path.exists("u22111164Al1.txt"):
			remove('u22111164Al1.txt')
		open("u22111164Al1.txt", "a")
#Se llama a las funciones aceptarC y procesarC
		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()
#La interfaz para introducir comandos
		while True:
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
			if msg == '2':
				self.listaUsuarios()

			else: pass
#Acepta a los clientes que se quieren conectar
	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
				
			except: pass
#Procesa el mensaje que ha introducido un cliente
	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(128)
						if data: self.broadcast(data,c)
					except: pass
#Envia a todos los clientes el mensaje introducido por un cliente
	def broadcast(self, msg, cliente):
		file = open("u22111164Al1.txt", "a")
		file.write(pickle.loads(msg) + os.linesep)
		file.close()
		for c in self.clientes:
			print("Clientes conectados Right now = ", len(self.clientes))
			try:
				if c != cliente: 
					print(pickle.loads(msg))
					c.send(msg)
			except: self.clientes.remove(c)
#Muestra por pantalla los clientes conectados
	def listaUsuarios(self):
		print("Los usuarios actualmente conectados son:\n\n")
		with open('lista_de_usuarios.txt', 'r') as archivo:
			for linea in archivo:
					print(linea)


arrancar = Servidor() 
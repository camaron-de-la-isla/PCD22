import threading
import sys
import socket
import pickle
import os

class Cliente():
#El cliente se inicializa y pregunta al usuario por el puerto y la IP y su nombre de usuario
	def __init__(self, host=input("Intoduzca la IP del servidor ?  "), port=int(input("Intoduzca el PUERTO del servidor ?  ")), nick=input("Introduce un nombre de usuario: ")):
		self.s = socket.socket()
		self.s.connect((host, int(port)))
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		threading.Thread(target=self.recibir, daemon=True).start()
#Añade el nombre de usuario del cliente a la lista de usuarios
		file = open("lista_de_usuarios.txt", "a")
		file.write(nick + os.linesep)
		file.close()
#La interfaz para introducir comandos
		while True:
			msg = nick+": "+input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 1 \n')
			if msg != nick + ": 1" : self.enviar(msg)
			else:
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid())
				self.eliminarUsuario(nick)
				self.s.close()
				sys.exit()
#Recibe los mensajes de otros clientes y los muestra por pantalla
	def recibir(self):
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				data = self.s.recv(128)
				if data: print(pickle.loads(data))
			except: pass
#Envia un mensaje al servidor
	def enviar(self, msg):
		self.s.send(pickle.dumps(msg))
#Elimina el usuario de la lista de usuarios
	def eliminarUsuario(self, nick):
		with open('lista_de_usuarios.txt', 'r') as fr:
			lines = fr.readlines()

			with open('lista_de_usuarios.txt', 'w') as fw:
				for line in lines:
					if line.strip('\n') != nick:
						fw.write(line)
					



arrancar = Cliente()
import time
import csv
import threading
import serial
import matplotlib.pyplot as plt
from matplotlib import ticker

# Captar el input del usuario (enter) para detener el programa
def input_listener():
    global stop_thread
    input()
    stop_thread = True

ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200, parity = serial.PARITY_NONE,
stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1)

#Crear archivo CSV y escribir encabezados
with open('datos.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Velocidad del vehiculo','Velocidad del motor','Marcha', 'Acelerador'])
#bandera para poder controlar el hilo de ejecucion
stop_thread = False

#Listas para almacenar los datos para las graficas
muestra = []
motor_speeds = []
vehicle_speeds = []
ger_values = []
pot_values = []

#Iniciar hilo para escuchar el input del usuario
threading.Thread(target=input_listener).start()

#Graficos en tiempo real
plt.ion()
fig, axs = plt.subplots(2,2, figsize = (12,8))

#Bucle principal
while not stop_thread:
        #Leer datos desde el puerto serial
        data = ser.readline().decode().strip() #Si se recibe una linea completa
        if data: #Checar si data no es un string vacio
            data_list = data.split(',')
            try:
                vehicle_speed = float(data_list[0])
                motor_speed = float(data_list[1])
                ger = int(data_list[2])
                pot = int(data_list[3])
                
                print(f"Muestra {len(muestra) + 1}:")
                print("Velocidad del motor:", motor_speed, "m/s")
                print("Velocidad del vehiculo:", vehicle_speed, "m/s")
                print("Marcha:", ger)
                print("Acelerador:", pot)
                
                #Agregar los datos a las listas para las graficas
                muestra.append(len(muestra) + 1)
                motor_speeds.append(motor_speed)
                vehicle_speeds.append(vehicle_speed)
                ger_values.append(ger)
                pot_values.append(pot)
                
                #Escribir datos en el CSV
                with open('datos.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([motor_speed, vehicle_speed, ger, pot])
                    
                #Actualizar y trazar la grafica
                for ax in axs.flat:
                    ax.clear()
                    
                axs[1,0].plot(muestra, motor_speeds, color = 'skyblue', marker = 'o', markersize = 5, label = 'Velocidad del motor')
                axs[1,0].set_title('Velocidad del motor', fontsize = 12, fontweight = 'bold')
                axs[1,0].set_xlabel('Muestra', fontsize = 10)
                axs[1,0].set_ylabel('Velocidad del motor (m/s)', fontsize = 10)
                axs[1,0].legend()
                axs[1,0].grid(True, linestyle='--', linewidth = 0.5)
                
                axs[1,1].plot(muestra, vehicle_speeds, color = 'salmon', marker = 's', markersize = 5, label = 'Velocidad del vehiculo')
                axs[1,1].set_title('Velocidad del vehiculo', fontsize = 12, fontweight = 'bold')
                axs[1,1].set_xlabel('Muestra', fontsize = 10)
                axs[1,1].set_ylabel('Velocidad del vehiculo (m/s)', fontsize = 10)
                axs[1,1].legend()
                axs[1,1].grid(True, linestyle='--', linewidth = 0.5)
                
                axs[0,0].plot(muestra, ger_values, color = 'mediumorchid', marker = '^', markersize = 5, label = 'Marcha')
                axs[0,0].set_title('Marcha', fontsize = 12, fontweight = 'bold')
                axs[0,0].set_xlabel('Muestra', fontsize = 10)
                axs[0,0].set_ylabel('Marcha', fontsize = 10)
                axs[0,0].legend()
                axs[0,0].grid(True, linestyle='--', linewidth = 0.5)
                
                axs[0,1].plot(muestra, pot_values, color = 'green', marker = '^', markersize = 5, label = 'Acelerador')
                axs[0,1].set_title('Acelerador', fontsize = 12, fontweight = 'bold')
                axs[0,1].set_xlabel('Muestra', fontsize = 10)
                axs[0,1].set_ylabel('Acelerador', fontsize = 10)
                axs[0,1].legend()
                axs[0,1].grid(True, linestyle='--', linewidth = 0.5)
                
                plt.tight_layout()
                plt.draw()
                plt.pause(0.01)
                
                #Esperar 0.3 segundos antes del siguiente ciclo
                time.sleep(0.1)
                
            except ValueError:
                print(f"Error: could not convert string to float. Received data: {data_list}")
        else:
            print("No data received from the serial port")
#Cerrar el puerto serial
ser.close()

#Detener los graficos en tiempo real
plt.ioff()
plt.show()
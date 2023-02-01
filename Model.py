# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Se importa MultiGrid pues pueden existir varias entidades en una celda
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation

# Vamos a hacer uso de `DataCollector` para obtener el grid completo cada paso (o generación) y lo usaremos para graficarlo.
from mesa.datacollection import DataCollector

# Definimos los siguientes paquetes para manejar valores númericos.
import numpy as np
import pandas as pd

# Definimos otros paquetes que vamos a usar para medir el tiempo de ejecución de nuestro algoritmo.
import time
import datetime
import math
from random import randrange
import random

start = (2,2,2,2)
comms = list(start)
def get_grid(model):
  #Se obtiene grid del modelo, se itera sobre la misma, se leen sus valores y se asigna un valor a cada celda para representación gráfica
  grid = np.zeros((model.grid.width, model.grid.height))
  for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    for content in cell_content:
      if isinstance(content,Road):
        grid[x][y] = 100
      elif isinstance(content,Car):
        grid[x][y] =  content.color
      elif isinstance(content,Traffic):
        grid[x][y] = content.light
      else:
        grid[x][y] = 0

          

  return grid


class Road(Agent):
  def __init__(self,unique_id,road_id,model):
    super().__init__(unique_id,model)
    self.tipo = "Road"
    self.road = road_id
    

class Car(Agent):
  def __init__(self,unique_id,road_id,pos,model):
    super().__init__(unique_id,model)
    self.color = randrange(9)*10
    self.road = road_id
    self.pos = pos
    self.position = [self.pos[0], .085, self.pos[1]]
    self.origin = pos
    self.reference_pos = (0,0)
    self.light_pos = (0,0)
    self.wait = 0
    self.movimientos = 0
    self.get_reference_loc()
    self.tipo = "Carro"    


  def get_reference_loc(self):
    if self.road == 2:
      self.reference_pos = (10,9)
      self.light_pos = (10,10)

    elif self.road == 1:
      self.reference_pos = (9,7)
      self.light_pos = (10,7)

    elif self.road == -2:
      self.reference_pos = (7,8)
      self.light_pos = (7,7)

    elif self.road == -1:
      self.reference_pos = (8,10)
      self.light_pos = (7,10)
      
  def direction(self):
    if self.road == 2:
      return (self.pos[0]-1,self.pos[1])
    elif self.road == 1:
      return(self.pos[0],self.pos[1]+1)
    elif self.road == -2:
      return (self.pos[0]+1,self.pos[1])
    elif self.road == -1:
      return (self.pos[0],self.pos[1]-1)
  
  def move(self,next_pos):
    if self.pos != next_pos:
      self.movimientos += 1
    self.model.grid.move_agent(self, next_pos)
    self.pos = next_pos
    self.position =  [self.pos[0], .085, self.pos[1]]
  
  def step(self):
    #posible siguiente dirección
    if self.wait > 0 :
      self.wait -=1
      
    next_pos = self.direction()
    x,y = next_pos 

    # Si siguiente posición fuera de límites: regresa coche a origen.
    if x < 0 or x >19 or y < 0 or y > 19:
      next_pos = self.origin
      #self.position = [self.pos[0], -5, self.pos[1]]
      
    #Obtiene Contenidos de celda frontal
    front = self.model.grid.get_cell_list_contents([next_pos])
   
    collision = False
    for car in front:
      if isinstance(car,Car):
        collision = True
    
   
    #si no hay colisión
    if collision != True:
      #si llegó junto al semáforo
      if self.pos == self.reference_pos:
        #obtiene datos de semáforo
        light_content = self.model.grid.get_cell_list_contents([self.light_pos])
        traffic_light = [l for l in light_content if isinstance(l,Traffic)]
        #verifica estado de semáforo.
        if traffic_light[0].light == 50 :
          self.move(next_pos)
      else:
        self.move(next_pos)
    elif collision == True:
      self.wait = 2



class Traffic(Agent):
  # ligt; 90 = red, 70 = yellow, 50 = green
  #comms; 1  = red,  2 = yellow,  3 = green
  def __init__(self,unique_id,comms_id,pos,model):
    super().__init__(unique_id,model)
    self.light = 70
    self.pos = pos
    self.position = [self.pos[0], 1, self.pos[1]]
    self.comms_id = comms_id
    self.wait = 0
    self.boundary,self.boundary2,self.counter_id = self.findBoundary()
    self.tipo = "Semaforo"
    
  
  def change(self,value,comm):
    self.light = value
    comms[self.comms_id] = comm
  
  def findBoundary(self):
    if self.comms_id == 0:
      boundary = ((self.pos[0],self.pos[1]+1), (self.pos[0]-1,self.pos[1]+1), (3,1))

      return boundary
    elif self.comms_id == 1:
      boundary = ((self.pos[0]+1,self.pos[1]),(self.pos[0]+1,self.pos[1]+1),(0,2))
      return boundary
    elif self.comms_id == 2:
      boundary = ((self.pos[0],self.pos[1]-1),(self.pos[0]+1,self.pos[1]-1),(3,1))
      return boundary
    elif self.comms_id == 3:
      boundary = ((self.pos[0]-1,self.pos[1]),(self.pos[0]-1,self.pos[1]-1),(0,2))
      return boundary
  
  def step(self):
    if self.wait > 0:
      self.wait -= 1
    boundary_Content = self.model.grid.get_cell_list_contents([self.boundary])
    boundary_Content2 = self.model.grid.get_cell_list_contents([self.boundary2])
    carAproaches = False
    carAproaches2 = False
    counter_green = False

    for car in boundary_Content:
      if isinstance(car,Car):
        carAproaches = True

    for car in boundary_Content2:
      if isinstance(car,Car):
        carAproaches2 = True

    if comms[self.counter_id[0]] == 3 or comms[self.counter_id[1]] == 3:
      counter_green = True
      
    if self.light == 50:
      if self.wait == 0:
        self.change(70,2)
    elif self.light == 70:
      if carAproaches == True or carAproaches2 == True:
        if counter_green ==True:
          self.change(90,1)
        elif counter_green == False:
          self.change(50,3)
          self.wait = 6
    elif self.light == 90:
      if carAproaches == False or carAproaches2== False or counter_green == False:
        self.change(70,2)

    
  

class TrafficModel(Model):
  def __init__ (self,W,H,nCars):
    self.left = nCars
    self.generations = 0
    self.nCars = nCars
    self.grid = MultiGrid(W,H,False)
    self.schedule = SimultaneousActivation(self)
    
    #Intersection road
    for i in range(1):
      for j in range(1):
        newRoad =Road( (1000+j), 10, self)
        self.schedule.add(newRoad)
        #Pavimenta en pos
        paveLocation = (8+i,8+j)
        self.grid.place_agent(newRoad,paveLocation) 

    #Road 1.
    for j in range(20):
      if (j != 8) or (j != 9):
        newRoad =Road( (100+j), 1, self)
        self.schedule.add(newRoad)
        #Pavimenta en pos
        paveLocation = (9,j)
        self.grid.place_agent(newRoad,paveLocation)  
    #Road 2.
    for j in range(20):
      if (j != 8) or (j != 9):
        newRoad =Road( (200+j), 2, self)
        self.schedule.add(newRoad)
        #Pavimenta en pos
        paveLocation = (j,9)
        self.grid.place_agent(newRoad,paveLocation)  
    #Road -1.
    for j in range(20):
      if (j != 8) or (j != 9):
        newRoad =Road( (-100-j), -1, self)
        self.schedule.add(newRoad)
        #Pavimenta en pos
        paveLocation = (8,j)
        self.grid.place_agent(newRoad,paveLocation)  
    #Road -2.
    for j in range(20):
      if (j != 8) or (j != 9):
        newRoad =Road( (-200-j), -2, self)
        self.schedule.add(newRoad)
        #Pavimenta en pos
        paveLocation = (j,8)
        self.grid.place_agent(newRoad,paveLocation) 
    
    
    newTraffic = Traffic((90+1),0,(7,7),self)
    self.schedule.add(newTraffic)
    self.grid.place_agent(newTraffic,(7,7))
    
    newTraffic = Traffic((90+2),1,(7,10),self)
    self.schedule.add(newTraffic)
    self.grid.place_agent(newTraffic,(7,10))
    
    newTraffic = Traffic((90+3),2,(10,10),self)
    self.schedule.add(newTraffic)
    self.grid.place_agent(newTraffic,(10,10))

    newTraffic = Traffic((90+4),3,(10,7),self)
    self.schedule.add(newTraffic)
    self.grid.place_agent(newTraffic,(10,7))

    #Se posicionan los carros
    newPos = (0,8)
    newCar = Car(1,-2,newPos,self)
    self.schedule.add(newCar)
    self.grid.place_agent(newCar,newPos)

    newPos = (1,8)
    newCar = Car(2,-2,newPos,self)
    self.schedule.add(newCar)
    self.grid.place_agent(newCar,newPos)

    newPos = (19,9)
    newCar = Car(3 ,2,newPos,self)
    self.schedule.add(newCar)
    self.grid.place_agent(newCar,newPos)

    newPos = (9,0)
    newCar = Car(4 ,1,newPos,self)
    self.schedule.add(newCar)
    self.grid.place_agent(newCar,newPos)

    newPos = (8,19)
    newCar = Car(5,-1,newPos,self)
    self.schedule.add(newCar)
    self.grid.place_agent(newCar,newPos)

    newPos = (8,18)
    newCar = Car(6,-1,newPos,self)
    self.schedule.add(newCar)
    self.grid.place_agent(newCar,newPos)
    

    self.datacollector = DataCollector(
    model_reporters={"Grid": get_grid},
    agent_reporters = {'Movimientos' : lambda a: getattr(a, 'movimientos', None),
                        "Posicion" : lambda a: getattr(a, 'position', None),
                        'DirID': lambda a: getattr (a, 'road', None), 
                        'ColorSemaforo' : lambda a: getattr(a, 'light', None),
                        'Tipo' : lambda a: getattr(a, 'tipo', None)}                             
    )

  def step(self):
    self.datacollector.collect(self)
    self.schedule.step()
    self.generations +=1

# Install pyngrok to propagate the http server


# Load the required packages
from pyngrok import ngrok
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os
import numpy as np

# MAS module, for example, MESA

# Start ngrok
ngrok.install_ngrok()

# Terminate open tunnels if exist
ngrok.kill()

# Open an HTTPs tunnel on port 8585 for http://localhost:8585
port = os.environ.get("PORT", 8585)
server_address = ("", port)

public_url = ngrok.connect(port="8585", proto="http", options={"bind_tls": True})
print("\n" + "#" * 94)
print(f"## Tracking URL: {public_url} ##")
print("#" * 94, end="\n\n")


ngrok.kill()

##########
W = 20
H = 20
nCars = 5
EXEC_MAX_TIME = 0.02
model = TrafficModel(W,H,nCars)
TIME_START = time.time() 

##########

# The way how agents are updated (per step/iteration)
def updateFeatures():
    global flock
    features = []

    # For each agent...
    if True:
      model.step()
      #print(model.datacollector.get_agent_vars_dataframe().to_string())
      features = model.datacollector.get_agent_vars_dataframe()
    else:
      features = None

    return features

# Post the information in `features` for each iteration
def featuresToJSON(info_list):
  featureDICT = []
  #import pdb; pdb.set_trace()
  cont = 10
  for _, row in info_list.iterrows():
    if not row.Tipo == "Road":
      if cont >= model.generations*10:
        feature = {
          "position" : {"x":row.Posicion[0], "y":row.Posicion[1], "z":row.Posicion[2]},  #f'\{"x":{row.Posicion[0]}, "y":{row.Posicion[0]}, "z":{row.Posicion[0]}\}', #row.Posicion, # position
          "move" : row.Movimientos, # movimiento
          "colour" : row.ColorSemaforo, # colour
          "dirID" : row.DirID,
          "tipo" : row.Tipo 
        }
        featureDICT.append(feature)
      cont+=1
  return json.dumps(featureDICT)
  

# This is the server. It controls the simulation.
# Server run (do not change it)
class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", 
                     str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        #post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        
        # If you have issues with the encoder, toggle the following lines: 
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     #str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))

        # Here, magick happens 
        # --------------------       
        features = updateFeatures()
        #print(features)

        self._set_response()
        resp = "{\"data\":" + featuresToJSON(features) + "}"
        #print(resp)

        self.wfile.write(resp.encode('utf-8'))

# Server run (do not change it)
def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    public_url = ngrok.connect(port).public_url
    logging.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(
        public_url, port))

    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL + C stops the server
        pass

    httpd.server_close()
    logging.info("Stopping httpd...\n")

run(HTTPServer, Server)



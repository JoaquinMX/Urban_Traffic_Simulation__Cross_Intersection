# Urban Traffic Simulation: Cross Intersection with smart Traffic Lights.

The use of automobiles in Mexico has grown alarmingly in recent years, with negative consequences in several areas, such as increased smog, accidents, diseases, and vehicular congestion. With this in mind, this project seeks to solve this problem by developing a simulation where automobiles interact with each other in an urban environment, as well as a 3D system to visualize the motion data of the cars that result from the simulation.

Agents involved:
- Automobile
- Traffic light
First, the automobile is related to the traffic light as it is the activator that changes state and modifies the state of the automobile to stop or move. Depending on the presence of a car at the height of the traffic light to cross the street, the state of the traffic light will be modified. The traffic light agent also depends on the automobile to be activated.
In the initial proposal, integrating a third agent, the pedestrian, gave greater complexity and realism to the simulation. However, during the development and considering the times, we concluded that it was not viable for this delivery. Only the interactions between automobiles and traffic lights were implemented.

### Class diagram
Three main classes are presented; a Traffic class, which is the one corresponding to the state machines "Traffic Lights"; a Car class, whose instances are the vehicles in the traffic model; and finally, a TrafficModel class from which the previous classes inherit specific attributes and methods, this encompasses the entire simulation, and within its execution agents (classes) Car and Traffic are created.
![Imagen3](https://user-images.githubusercontent.com/67206790/215955046-64218689-af86-42e0-9839-031d5090e9d8.png)

### State machines
The traffic light is a vital part of the model. This state machine regulates the flow of traffic, and its decisions depend on those of the vehicles. It consists of 3 states; yellow, by default; red, as a stop; and green, as a signal to advance. Its state diagram is shown as follows.
![Imagen4](https://user-images.githubusercontent.com/67206790/215955061-8da04edb-d535-4433-846e-45f0c18776e1.png)

The vehicles as state machines directly depend on the decisions of other agents. In addition, the absence or presence of these influences the change of state of the traffic lights.
![Imagen5](https://user-images.githubusercontent.com/67206790/215955100-2c72888c-494c-4f2e-929f-297626509b2f.png)

### Protocol diagram
![Imagen6](https://user-images.githubusercontent.com/67206790/215955125-7ba8bf54-887a-4d12-b168-86a2eb4c9def.png)

## Installation, Configuration, and Execution Process Description for the Simulation
To run the simulation, a series of steps must be followed that involve installation and configuration on the client (Unity) and server (Google Colab).

### Server
To run the server, the following steps must be taken:
1. Open the Google Colab link.
2. Select the "Runtime" tab.
  a. Select the "Run All" option.
3. Wait a few moments. Below the penultimate block, a series of information will be displayed. Save the link, similar to the following image, as it will be used in the client configuration:
![Imagen1](https://user-images.githubusercontent.com/67206790/215951848-79853841-b9ec-4974-8db1-f8c96d16b0d4.png)


### Client
To correctly install and configure the client, the following steps must be taken:
1. Download the .unitypackage file from the documentation.
2. Create a new project in Unity.
3. Once the project has concluded creating, select the "Window" tab. 
  a. Select the drop-down option "Package Manager."
4. A window will be displayed. In this window, select the "Unity Registry" drop-down menu option in the "Packages" menu.
5. Type "Probuilder" in the search bar.
6. Install the only existing package.
7. Once the package is finished installing, select the "Assets" tab.
8. From the drop-down menu, select the option "Import Package" and choose the option "Custom Package."
9. The file explorer will open. Select the .unitypackage file.
10. Having done this, navigate to the Unity folder called "Scripts" and open the file "AgentController."
11. In line 77 of the file, change the "URL" variable, so its value is the URL obtained in point 3 of the server configuration.
12. Select the play button to run the simulation.

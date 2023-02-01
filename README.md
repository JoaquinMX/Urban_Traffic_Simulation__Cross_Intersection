# Installation, Configuration, and Execution Process Description for the Simulation
To run the simulation, a series of steps must be followed that involve both installation and configuration on the client (Unity) and server (Google Colab).

## Server
To run the server, the following steps must be taken:
1. Open the Google Colab link.
2. Select the "Runtime" tab.
  a. Select the "Run All" option.
3. Wait a few moments. Below the penultimate block, a series of information will be displayed. Save the link, similar to the following image, as it will be used in the client configuration:
![Imagen1](https://user-images.githubusercontent.com/67206790/215951848-79853841-b9ec-4974-8db1-f8c96d16b0d4.png)


## Client
To correctly install and configure the client, the following steps must be taken:
1. Download the .unitypackage file from the documentation.
2. Create a new project in Unity.
3. Once the project is finished creating, select the "Window" tab.
  a. Select the drop-down option "Package Manager".
4. A window will be displayed, in this window select the drop-down menu option "Unity Registry" in the "Packages" menu.
5. Type "Probuilder" in the search bar.
6. Install the only existing package.
7. Once the package is finished installing, select the "Assets" tab.
8. From the drop-down menu select the option "Import Package" and select the option "Custom Package".
9. The file explorer will open, select the .unitypackage file.
10. Having done this, navigate to the Unity folder called "Scripts" and open the file "AgentController".
11. In line 77 of the file, change the "url" variable so that its value is the url obtained in point 3 of the server configuration.
12. Select the play button to run the simulation.

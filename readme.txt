Project Description:

Youtube link: https://youtu.be/cYy__yCupnI

My project is 'The Beginners Guide to Schematics and Breadboards'. Many beginners learning circuits
have trouble understanding the breadboard layout and what its equivalent electronic schematic looks
like. This tool helps users do exactly that. Just build the breadboard on this program and an 
equivalent schematic design will be displayed. The program can also aid in debugging your breadboard.
Just create your breadboard using this program and check for any error messages or check the schematic
equivalent to see if it was your desired circuit. Additional tools include displaying the
voltage and current through each device.



Using the program properly:

To start the program, run the RunApplication.py file

For both Schematic and Breadboard Modes:
 - Press 'c' for the circuit analysis of each device
 - Press 'r' for creating a new resistor
 - Press 'w' for creating a new wire
 - Press 'Delete' to delete the most recent device you inputted
 - Press 'R' to restart that specific mode
 - Press 'S' to switch between modes

Moving Devices in Schematic Mode
 - Click and drag a node to move the device
 - Just like an electronic schematic, move the node close to another device's node to connect
    the devices together
 - To remove a connection, simply drag the node of the device away

Moving Devices in Breadboard Mode
 - Click and drag a node to move the device
 - Just like a breadboard, move the node to any of the holes on the breadboard. 
    It should automatically clip onto a hole that is nearby, denoting successful
    connection.
 - To remove a connection, simply drag the node of the device away
 - Devices are not allowed to be connected at the same hole just like a real breadboard

Converting Breadboard design to Schematic design
 1. Build a breadboard circuit
 2. Press "S", if the circuit is not viable, a pop-up message will appear, redo step 1
 3. Once in the schematic mode window, press "R" to convert 



Libraries needed to be installed:
 - PIL
 - cmu 112 graphics



Shortcut commands (works for both modes)
 - Press 's' to see the prints of the connections of each device to one another
     - Each node contains itself and the devices connected to it
     - The best way to see the connections is using resistors all with different resistances
     - The shown tuple is the cx, cy of the device
 - Press 'c' to see the prints of the Device conversion


# Satellite-Command-System-Programming-Exercise
## Problem Statement
Develop a Satellite Command System that simulates controlling a satellite in orbit. Satellite starts in a default initial state and can accept a series of commands to change its orientation, solar panel status, and data collection.


## Objective
Develop a Satellite Command System for simulating satellite control in orbit.

## Requirements
Initialize satellite
Rotate
Activate/Deactivate Solar Panels
Collect Data

## Initial State
Orientation: "North"
Solar Panels: "Inactive"
Data Collected: 0

## Additional discussion points
1.What if the satellite is already in desired position?
	Avoid unnecessary rotations we can add a check in ‘collectDatacommand’ to verify if current orientation is desired one.
	If not in desired position rotate it and check if panel is active 
	else check the panel status and proceed with the further commands.
2.What if command fail temporarily due to external factors?
	Defensive programming: If an exception occurs during the execution of the command, the system will attempt to retry the operation for a certain number of times before giving up.
 

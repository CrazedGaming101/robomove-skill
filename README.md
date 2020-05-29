# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#FF7400" width="50" height="50" style="vertical-align:bottom"/> Fleming Bot Project - 2020

## About
Makes bb8 look-a-like move by sending motor controls via udp from one Raspberry PI to another Raspberry PI based on the input of a t-shirt color that someone is wearing. 

One Raspberry PI is located in the head of the robot, acquiring input via Picamera to determine the area of color captured. The other Raspberry pi is located in the main chassis, providing an output in the form of motor controls. 

This works using the Linux Distribution 'MyCroft' which is an Open-Source voice assistant that supports the ability to create custom "skills" which are Python class files that interact with MyCroft to perform various commands. By using MyCroft's intent parser, I can then create custom voice commands that when performed after saying "Hey MyCroft", will perform the commands outlined below:

## Examples These are some of the keywords used to get the robot moving using MyCroft
* "Lets roll"
* "Motors on"
* "Lets move it"
## Phrase that changes the color the robot 
* "Change color to <chosen color>"
  
## Keywords that stop motor controls
* "stop the bot"
* "stop rolling"
* "turn motors off"
* "stop moving"



## Credits
Kirk

## Category
**IoT**
Robots



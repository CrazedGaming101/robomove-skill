#######################################################################
#Name: Kirk Patrick		Project BB8 Bot
#Description: This project is programmed to send UDP bits to another pi
#for motor control. This output is acquired by using picamera and CV2 to
#find our selected color based on a HSV value and return an output based
#on the area of the color found in the camera lens. It will use the
#Mycroft library to ask and receive a color. Some of the logic of this code
#is credited to "Learn Robotics with Raspberry Pi" by Matt Timmons-Brown
#for the code logic behind a "Color following robot" The code has been built
#upon to suit our needs of the project. You can find some of the code from the website
#https://automaticaddison.com/tag/raspberry-pi/
#######################################################################

from mycroft import MycroftSkill, intent_file_handler
#from gpiozero import LED, Button
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import socket
from pijuice import PiJuice

#UDP of destination
udp_ip = "192.168.100.120"
udp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Start the class of functions for BB8
class Robomove(MycroftSkill):
    #Initialize starting variables
    def __init__(self):
        MycroftSkill.__init__(self)
        color = 'blue'
        self.valid_color = ['blue', 'yellow', 'red', 'green', 'pink', 'purple', 'orange']
        #This needs to be here to prevent error codes from initializing too many cameras
        self.camera = PiCamera()
        self.color = color
        self.color_picker()
        self.initiator = 0
    #If we say the key words for this program, Jarvis responds and makes BB8 move
    @intent_file_handler('robomove.intent')
    def handle_bbot(self, message):
        #this turns the motors on and sends UDP messages to the motor controller
        self.speak_dialog('robomove')
        self.initiator = 1
        self.bb8_move()

    #If key color from valid_color is said, choose the color for BB8 to follow
    @intent_file_handler('color.intent')
    def color_intent(self, message):
        picked_color = message.data.get('type')
        if picked_color is not None:
            if picked_color in self.valid_color:
                self.speak('Setting color to ' + picked_color)
                self.color = picked_color
                self.color_picker()
            else:
                self.speak('color ' + picked_color + ' not found, try a different color.')
        else:
            self.speak('did not set color')
            pass


    #This will handle if we tell the robot to stop moving
    @intent_file_handler('stop.intent')
    def stop_the_bot(self, message):
        self.initiator = 0
        self.speak('Stopping the bot now')

    #This will set the color's Low and high hue, low saturation and low value for all colors involved
    def color_picker(self):
        if self.color == 'yellow':
            self.chosen_color(25, 35, 50, 50)
            self.respond()
        elif self.color == 'red':
            self.chosen_color(158, 180, 70, 70)
            self.respond()
        elif self.color == 'blue':
            self.chosen_color(94, 126, 80, 2)
            self.respond()
        elif self.color == 'green':
            self.chosen_color(38, 75, 80, 80)
            self.respond()
        elif self.color == 'orange':
            self.chosen_color(10, 20, 120, 120)
            self.respond()
        elif self.color == 'purple':
            self.chosen_color(135, 150, 50, 50)
            self.respond()
        elif self.color == 'pink':
            self.chosen_color(150, 170, 50, 50)
            self.respond()
        else:
            self.speak('Invalid color, try colors red, yellow, green, orange, purple, blue, or pink')

    #This will set up the values for camera detecting color
    def chosen_color(self, low_hue_value, high_hue_value, low_sat, low_val):
        self.low_hue_value = low_hue_value
        self.high_hue_value = high_hue_value
        self.low_sat = low_sat
        self.low_val = low_val


    def respond(self):
        #self.speak('You have chosen' + self.color + '.')
        pass

#This will control the movement of the robot based on the color
    def bb8_move(self):
        #Set up camera
        image_width = 640
        image_height = 480
        self.camera.resolution = (image_width, image_height)
        self.camera.framerate = 32
        rawCapture = PiRGBArray(self.camera, size=(image_width, image_height))
        #Find the center of the image
        center_image_x = image_width / 2
        center_image_y = image_height / 2
        #Get minimum and maximum area based on pixels. 640 * 480 pixels = 307,200 total pixels
        #adjust these numbers until BB8 no longer hits you
        minimum_area = 250
        maximum_area = 100000

        # Constantly capture the camera
        for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # Convert the color from BGR default to HSV
            image = frame.array
            # The Hue color used in the HUV wheel
            # The range of color Hue, Saturation,Value determined
            lower_color = np.array([self.low_hue_value, self.low_sat, self.low_val])
            upper_color = np.array([self.high_hue_value, 255, 255])
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            color_mask = cv2.inRange(hsv, lower_color, upper_color)
            # Apply green theorem with the specified color and return areas of the shape
            image2, countours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            object_area = 0
            object_x = 0
            object_y = 0
            # Find the area of the specified object color
            for contour in countours:
                x, y, width, height = cv2.boundingRect(contour)
                found_area = width * height
                center_x = x + (width / 2)
                center_y = y + (height / 2)
                if object_area < found_area:
                    object_area = found_area
                    object_x = center_x
                    object_y = center_y
            # If we found the area of the object specified, set the location for it
            if object_area > 0:
                color_location = [object_area, object_x, object_y]
            else:
                color_location = None
            # If we acquired a location of the color, determine where its located and control the motors accordingly
            #juice = PiJuice(1, 0x14)
            #status = juice.status.GetStatus()['data']['battery']
            if color_location:
                if (color_location[0] > minimum_area) and (color_location[0] < maximum_area):
                    #print(status)
                    #if status == 'CHARGING_FROM_5V_IO':
                        #sock.sendto(b'CHARGING', (udp_ip, udp_port))
                        #print('charging')
                    if color_location[1] > (center_image_x + (image_width / 3)):
                        sock.sendto(b'RIGHT', (udp_ip, udp_port))
                        #print('right')
                    elif color_location[1] < (center_image_x - (image_width / 3)):
                        sock.sendto(b'LEFT', (udp_ip, udp_port))
                        #print('left')
                    else:
                        sock.sendto(b'FORWARD', (udp_ip, udp_port))
                        #print('forward')
                elif (color_location[0] < minimum_area):
                    sock.sendto(b'TOO SMALL', (udp_ip, udp_port))
                    #print('too small')
                else:
                    sock.sendto(b'STOP', (udp_ip, udp_port))
                    #print('stop')
            else:
                sock.sendto(b'MISSING TARGET', (udp_ip, udp_port))
                #print('MIA')

            rawCapture.truncate(0)
            #print(self.low_hue_value + self.high_hue_value + self.low_sat + self.low_val)
            if self.initiator==0:
                sock.sendto(b'STOP',(udp_ip, udp_port))
                break
            else:
                continue
#This is used by Mycroft to generate the skill so it can be used. 
def create_skill():
    return Robomove()




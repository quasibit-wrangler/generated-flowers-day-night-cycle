#############################
###Author: Conner Maddalozzo
#date: 3/26/18
#desc: computing many  flowers it a garden and simulating the suns cycle
#around the wildlife


#into a parseble language
# than displaying the comouted coordinates inti an animation
#than later using those pre assebmled coordinates to simulate the flower
#in motion.
###
from visual import *
from copy import copy
from copy import deepcopy
from time import sleep
import random
from math import pi

random.seed()
def rand_float(a,b):
    return random.uniform(a,b)

def rand_int(start,end):    #returns a random integere
    return random.randint(start,end)





#inputs... arrray of objects?
class Flower_parser:
    def __init__ (self,flowers):

        return
    archive = [ [ [] ] ]
#flower
# desc: 
#variables:
#has its current and past life
#   CurrentState: an array of points, that resembles its current state
#   past: [ [] ] an array of past points. at the tend, [0] = t:0, [n] = t:f;
#
#has manfiest specific load details
#   like speeds and size...
class flower:    
######################
### variables
    CurrentState = [] #the array of tuples to be used    
    past = [ ] #the previous points. secretely a 2D array...
                ###3D array if you count the tuples
#### objects
    manifest = {} # the manifest of the flower objects
    stem = {}
    bud = {}

#### actually constants to the class
    stempath = [ (0,0,0), (-0.02,-1,0), (-0.1,-2.5,0),(-0.15,-3.2,0),(-.17,-3.9,0),(-.2,-4.20,0)]
    NUM_FLOWER_PIECES = 0
    AmpWidth = 0 # ; how often does it grow or shrink or not
    RotFreq = 0 #how fast does it rotate
    radius = 0 # how big the flower is
    leaves = 0
    colour = (0,0,0)
############################
###
    offset = vector(0,0,0) #all the points reflect off of this point
    SetParams = [None] * 6# this will hold all my params for easy go to

    
    #non defuat constructos
    # big O IS REQUIRED.. others are not
    # params ={ bigO:
    #   rotFreq:
    #... if one it omitted it has a default value
#def __init__(self, bigO, Amp = 0, Rotate = 0.5, Rad = 0.5, col = (0,0,0) ):
    def __init__(self, params, col = color.red ):
        ###OFFSET ############
        try:
            if(params["Offset"]):
                self.offset = params["Offset"]
                self.stempath = [ (0,0,0), (-0.02,-2,0), (-0.1,-3.5,0),(-0.15,-4.2,0),(-.17,-4.9,0),(-.2,-5.20,0)]

                for i in range(len(self.stempath) ):
                    self.stempath[i]=(self.stempath[i][0] + self.offset.x ,self.stempath[i][1]+ self.offset.y,self.offset.z)
        except KeyError:
            self.offset = vector(0,0,0) #defualt
            pass
            
        #complexity#############
        try:
            if(params["bigO"]):
                self.NUM_FLOWER_PIECES = params["bigO"]
                self.CurrentState = [None] * params["bigO"]
        except KeyError:
            self.NUM_FLOWER_PIECES = 10 #defualt
            self.CurrentState = [None]*10
            pass
        ##leavs################    
        try:
            if(params["Leaves"]):
                self.leaves = params["Leaves"] ### [ delta size, speed ] it flexes adn changes size]
                self.SetParams[1] = params["Leaves"]
                
        except KeyError:
            self.leaves = 5 #defualt
            self.SetParams[1] = 5
            pass
        ##expand################    
        try:
            if(params["Amp"]):
                self.AmpWidth = params["Amp"] ### [ delta size, speed ] it flexes adn changes size]
                self.SetParams[0] = params["Amp"]
        except KeyError:
            self.SetParams[0] = 2
            self.AmpWidth = 2 #defualt
            pass
        
        ###rotate ########################
        try:
            if(params["Rotate"]):
                self.RotFreq = params["Rotate"]
                self.SetParams[3] = params["Rotate"]
                
        except KeyError:
            self.RotFreq = 10.0 #defualt
            self.SetParams[3] = 5.0
            pass
        
        ###size#####################
        try:
            if(params["Radius"]):
                self.radius = params["Radius"]
                self.SetParams[5] = params["Radius"]
        except KeyError:
            self.radius = 0.75 #defualt
            self.SetParams[5] = 0.75
            
            pass
        
     ################# 00            11         22              33                   44                     55
        #params = [Amplitude Range, numLeafs , theta, phase shift rate(omega) , phase shift (time),  initial radius]
        
        self.colour = col
        return

   
######################
## member functions
  

##################################
###################
    # only on the time used, it will math that shit up, does this for
    # the whole flower every DT slice.
    # and then store it will the other helper functino.
    def calc_Store (self, time, NightTime = False):
        pointCalc = [None] * 3
        pointSend = (0,0,0)
        
        ###time to put together
        #calculate the next state of the flower for iterating 0 to 2pi with
        #    flower calculator.
        #
        #f(theta, t) :: so we set t, and iterate all of thetas.
        
         
        self.SetParams[4] = time # this is the only parameter that changes,

        
        #every time we calculate a new flower or its shape, we
        #go in range 0 to (2*pi - dTheta) , that is one period. a 360.
        for piece in range(self.NUM_FLOWER_PIECES):
            theta = (2*pi)/(self.NUM_FLOWER_PIECES-1) * piece # ranges from 0 to 2Pi in num pieces complextity
            self.SetParams[2] = theta # set the current theta

            #first we calculate the points without the offset, mind you they will be in polar
            pointCalc[0] = theta
            pointCalc[1] = calcFlower( copy(self.SetParams) ) # pass a shallow copy, only references. 

            #convert that to rectangular...
            pointSend = ptor(pointCalc)

            #then we need to modify it based off the offset
            pointSend = ( pointSend[0] + self.offset.x, pointSend[1] + self.offset.y, self.offset.z)
            
            #then finally..
            self.CurrentState[piece]= pointSend  # add it so the collection .. the size of the array always varies from 0 to number

        return
        
                         
###############################
####
    #turns on the manifest and turns it off in one funtion.
    #deletes stuff as well.
    def ToggleManifest(self):
        if( not self.manifest):
            #basically create all the shapes into the display windo.
            self.manifest = curve ( color= self.colour , radius = self.radius/5)
            self.stem = curve( color=color.green, radius = 0.12, pos = self.stempath )
            circ = shapes.circle( pos= (0,0), radius= self.radius ) #TEMP 2d shape
            self.bud= extrusion ( pos= self.offset, shape = circ, color= self.colour)
            
        else:
            self.manifest.visible = False
            self.bud.visible = False
            self.stem.visible = False
            del self.bud
            del self.stem
            del self.manifest                              
            
        return
    def setManifest(self):
        if(len(self.CurrentState)):
            self.manifest.pos = deepcopy(self.CurrentState) # set the current stuff to the newly added stuff
        return

    ## appends for storing or doesnt.
    ## always deletes the array and starts it again
    def CleanandStore (self):
        #self.past.append( deepcopy(self.CurrentState) )
        return

#############################################
#### no more flower class #



################################
#global variables

#converts polar to rectangular
#polar = [theta, R]
#a = [x, y, NULL], z equals z constant?
def ptor (polar): #polar to rectangular
    return (polar[1]*cos(polar[0]),polar[1]*sin(polar[0]))


#params = [Amplitude Range, numLeafs , theta, phase shift rate(omega) , phase shift (time),  initial radius]
# f(theta,t) = ChangeAmplitude * sin( numleafs * theta + phi*t ) +initial radius
def calcFlower(params):
    return ( abs( params[0] * cos( params[1]*params[2] + params[3]*params[4] ) )+ params[5])    
   
      

class sun:

    def __init__(self):
        self.globe = sphere (radius = 1.5, material=materials.emissive, pos=vector(0,-30,0) )
        self.lampz={}
        for let in range(3):
           self.lampz[ str(let) ]  = local_light(pos=(0,-30,let*50 - 50 ), color= color.white)
        return

    def moveSun(self,time):
        for key, value in self.lampz.items():
            value.pos = vector(100*sin(t),-30*cos(t),value.pos.z)

        self.globe.pos = vector(100*sin(t),-30*cos(t),self.globe.pos.z)
        return

    




universe = display (fullscreen= True, x=500,y=0, width=500, height = 300, autoscale = True )
#reset all the lights on the stage.
universe.ambient = (0,0,0)
universe.lights= []

#my flowers
### init those useful variables.
#my_flowers = []
my_flowers = {}
t= 0
dt= 0.02
grass= box (width =100, length=100,height=0.5, pos=vector(0,-2.5,0) , color=(0,100.0/255.0,0))
soil = box (width =100, length=100,height=1, pos=vector(0,-3,0) , color=(139.0/255,69.0/255,19.0/255.0) )

lightSun = sun()

num_flowers =  30

##    { "bigO" :0,
##      "Amp": 0,
##      "Rotate": 0,
##      "Radius": 0,
##      "Leaves":0
##      "Offset": vector(x,y,z)
##      }\
for i in range (num_flowers):
    params =  { "bigO" : 35,
                "Offset": vector (rand_float(-50,50),4 ,rand_float(-50,50)),
                "Leaves": 3
                #"Leaves": (2*rand_int(1,2) + 1)
                }
    my_flowers[ str(i**3)] =  flower(params,(rand_float(0,1),rand_float(0,1),rand_float(0,1) )  )


### now all of our flowers exsit. time to wake them up.

#for flow in my_flowers[:]:
for key,flow in my_flowers.items():

    flow.ToggleManifest()
                       

#moving animation loop.   

while ( t < 20 ):
    rate(1/dt)

    #stage one. calculate all the new flowers
    for key,flow in my_flowers.items():
        flow.calc_Store( t*0.5 )
        
    #complete, stage two, put that stuff on the screen
    for key,flow in my_flowers.items():
        flow.setManifest()

    #now store that data and clean up to calculate it again.
    for key,flow in my_flowers.items():
        flow.CleanandStore()

    lightSun.moveSun(t)
        
    t = t + dt


        
     



#time to clean up my spheres
#for flow in my_flowers[:]:
for key,flow in my_flowers.items():
    flow.ToggleManifest()









    

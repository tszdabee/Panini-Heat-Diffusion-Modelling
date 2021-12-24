# DE Coursework
# Shahmeer Hassan & Tsz Yin Yung

# This code takes a square chicken panini and heats it in a sandwich grill

# The loading bar in this code only works in Jupyter
# Use Panini_Model.py if NOT running in Jupyter


#import libraries
import numpy as np
import sys # Used for a clean exit
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# This imports the library to create a laoding bar
from tqdm.auto import tqdm

# This is to open an image at the end
from PIL import Image

# This is to open an mp4 animation at the end
from os import startfile


# This function asks the user for a mesh size
def get_h():
    # Ask for a step size
    h = input("Enter the mesh size in millimetres (numerical value only): ")
    h = float(h) # Convert to a float number
    h = h/1000 # convert to metres
    return h


def get_k(h, alpha_bread, alpha_chicken):
    
    # Find largest possible time step for both bread and chicken
    k_maxbread = 0.25*(h**2)/alpha_bread
    k_maxchicken = 0.25*(h**2)/alpha_chicken
    
    # Select lowest of the two
    k_max = min([k_maxbread, k_maxchicken])
    
    print()
    print("The maximum time step that will give a stable model is "+str(k_max)+" seconds") 
    
    # Ask user what they want as a time step
    k = input("Please enter a time step in seconds (numerical value only): ")
    k = float(k) # convert to a number
    
    return k
    

# This function recieves a boolean variable, execute
    # and asks the user if they want to continue with an unstable system
def get_input(execute):
    
    # If the Courant condition is satisfied
    if execute == True:
        print("Proceeding with calculation...")
        return execute
    
    # If the Courant condition is not satisfied
    elif execute == False:
        ask_user = input("Do you wish to continue? (y/n):") #Ask the user
        if ask_user == 'y' or ask_user=='Y' or ask_user=='yes':
            #Set the boolean variable to True
            execute = True
            print("Proceeding with calculation...")
            return execute
            
        elif ask_user == 'n' or ask_user=='N' or ask_user=='no':
            #End the program
            sys.exit("The user terminated the program")
            
        else:
            #The user mistyped. Ask again.
            print("Invalid response")
            execute = get_input(execute)
            

# This function opens an image
def open_image(filename):
    image = Image.open(filename)
    image.show()


#~~~~~~~~~~~~~~~~~~~~ Define the inputs ~~~~~~~~~~~~~~~~~~~~#

# Thickness of bread
bread_thickness = 0.003 # [m]

#Thickness of filling
filling_thickness = 0.01 # [m]

# Dimensions of square sandwich
XL = 0.1 # side length of sandwich [m]
YL = (2*bread_thickness) + filling_thickness # height of sandwich [m]

#set initial temperature of sandwich
initial_temperature = 0 # degC

# Time forecast
ttl_time = input("How long do you want to put the panini in the press for in seconds? ")
ttl_time = float(ttl_time)

# Define thermal properties
# Define heat transfer coefficient between sandwich and air
h_conv = 10 # [W/m^2 K]

# Define conductivity
k_bread = 0.068 # [W/m K]
k_chicken = 1.6 # [W/m K]

#Define density
rho_bread = 200 # [kg/m^3]
rho_chicken = 1068 # [kg/m^3]

#Define specfic heat capacity
cp_bread = 2800 # [J/kg K]
cp_chicken = 3220 # [J/kg K]

# Define Thermal Diffusivity
alpha_bread = k_bread/(rho_bread*cp_bread)
alpha_chicken = k_chicken/(rho_chicken * cp_chicken)

# Weighted thermal diffusivity for use in chicken-filling boundaries
alpha_breadbc = (3*alpha_bread + alpha_chicken)/4
alpha_chickenbc = (3*alpha_chicken + alpha_bread)/4

#Define ambient temperature
T_amb = 21 # degC

#Define hotplate temperature
T_plate = 150 # degC

#step in space
h = get_h() # units: [m]

#step in time
k = get_k(h, alpha_bread, alpha_chicken) # units: [s]

#~~~~~~~~~~~~Initialise the Temperatures 3D matrix~~~~~~~~~~~~~~~~~~~~#

#First initialise the 2D Matrix at t=0
xdim = int(XL/h)+1
ydim = int(YL/h)+1
T0 = np.zeros((ydim,xdim))

#Then intialise the 3D temperatures matrix
tdim = int(ttl_time/k)+1
T = np.zeros((tdim,ydim,xdim))

# Apply this initial temperature of sandwich to the initial temperature matrix
for i in range(0, len(T0)):
    for j in range(0,len(T0[0])):
        T0[i,j]=initial_temperature

# Add the temp matrix of t=0 to the temperatures 3D matrix
T[0]=T0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Define indices for sandwich
breaddim = int(bread_thickness/h)
filldim = ydim - 2 * breaddim

#~~~~~~~~~~~~~~~~~Check for Convergence~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Calculate Courant values for bread and chicken
courant_bread=alpha_bread*k/(h**2)
courant_chicken=alpha_chicken*k/(h**2)

# Calculate weighted Courant values for later use
courant_3b1c = (3*courant_bread + courant_chicken)/4
courant_1b3c = (3*courant_chicken + courant_bread)/4

print() # Blank line

if courant_bread <= 0.25 and courant_chicken <= 0.25:
    #Courant satisfied, stable
    print('Stable, Courant condition satisfied')
    execute = True
    
elif courant_bread <= 0.25 and courant_chicken > 0.25:
    #Courant not satisfied, unstable
    print('Potentially unstable, Courant condition not satisfied for sandwich filling')
    execute = False
    
elif courant_bread > 0.25 and courant_chicken <= 0.25:
    print('Potentially unstable, Courant condition not satisfied for bread')
    execute = False
    
else:
    print('Potentially unstable, Courant condition not satisfied for bread or sandwich filling')
    execute = False

# Tell user what the courant values are
print("Bread: alpha dt / (dx)^2 =",courant_bread)
print("Filling: alpha dt / (dx)^2 =", courant_chicken)

#Ask the user whether to continue to run the program
execute = get_input(execute)

#~~~~~~~~~~~~~~~~~~~~ Solve problem ~~~~~~~~~~~~~~~~~~~~#

for t in tqdm(range(1,len(T))): #for every instance in time, starting at t=0+k

    #Define boundary conditions

    #Top and bottom
    for j in range(0,len(T[0,0])): # for each column in the matrix

        # Top of food: Dirichlet
        T[t,0,j] = T_plate    #top of food = T_plate

        # Bottom of food: Dirichlet
        T[t,ydim-1,j]= T_plate #bottom of food = T_plate
        
        
    # Boundary conditions on sides - convection to environment
    for i in range(1,ydim-1):
        
        #For bread
        if i <= breaddim-1 or i >= filldim + breaddim:
            
            # Left side
            T[t,i,0] =(h/(k_bread+h_conv*h))*(h_conv*T_amb+T[t-1,i,1]*k_bread/h)

            #Right side
            T[t,i,xdim-1] =(h/(k_bread+h_conv*h))*(h_conv*T_amb+T[t-1,i,xdim-2]*k_bread/h)
        
        #For filling
        elif i>=breaddim and i < breaddim+filldim:
            
            # Left side
            T[t,i,0] =(h/(k_chicken+h_conv*h))*(h_conv*T_amb+T[t-1,i,1]*k_chicken/h)

            #Right side
            T[t,i,xdim-1] =(h/(k_chicken+h_conv*h))*(h_conv*T_amb+T[t-1,i,xdim-2]*k_chicken/h)
    

    #Centre of sandwich
    for i in range(1,ydim-1): # For every row in the matrix
        for j in range(1,xdim-1): # For every column in the matrix
            
            #if inside bread region and inside bread boundaries
            if i < breaddim-1 or i > breaddim + filldim:
                T[t,i,j]=T[t-1,i,j]+courant_bread*(T[t-1,i+1,j]+T[t-1,i-1,j]+T[t-1,i,j+1]+T[t-1,i,j-1]-4*T[t-1,i,j])
                #equivalent statement would be:
                '''T[t,i,j]= (k*alpha_bread/(h**2)) * (T[t-1,i+1,j] - 2*T[t-1,i,j] + T[t-1,i-1,j] + \
                 T[t-1,i,j+1] - 2*T[t-1,i,j] + T[t-1,i,j-1]) + T[t-1,i,j]'''
                
            # if inside filling region and inside filling boundaries
            if i > breaddim and i < breaddim+filldim-1:
                T[t,i,j]=T[t-1,i,j]+courant_chicken*(T[t-1,i+1,j]+T[t-1,i-1,j]+T[t-1,i,j+1]+T[t-1,i,j-1]-4*T[t-1,i,j])
                
            # For undefined bread boundaries
            if i==breaddim-1 or i==breaddim+filldim:
                T[t,i,j]= (k*alpha_breadbc/(h**2)) * (T[t-1,i+1,j] - 2*T[t-1,i,j] + T[t-1,i-1,j] + \
                 T[t-1,i,j+1] - 2*T[t-1,i,j] + T[t-1,i,j-1]) + T[t-1,i,j]
            
            # For undefined filling boundaries
            if i==breaddim or i==breaddim+filldim-1:
                T[t,i,j]= (k*alpha_chickenbc/(h**2)) * (T[t-1,i+1,j] - 2*T[t-1,i,j] + T[t-1,i-1,j] + \
                 T[t-1,i,j+1] - 2*T[t-1,i,j] + T[t-1,i,j-1]) + T[t-1,i,j]
    
    #Update loading bar (only works in Jupyter)
    print(" ", end='\r')

print("Calculation completed successfully!")
print()

#~~~~~~~~~~~~~~~~~~~~~~~~Generate Contour Plot~~~~~~~~~~~~~~~~~~~~~~~~~~~#

plt.style.use('ggplot')

print("Generating colour plot...")

H=1000*h
# This step is required to reduce the effects of floating point error

#create x and y arrays for plotting in millimetres
x=np.arange(0, XL*1000+H, H)
y=np.arange(0, YL*1000+H, H)
# The multiplication by 1000 caused problems due to floating point error
# (YL+h)*1000 multiplies floating point error more than YL*1000*H

print("Final Temperature Distribtuion:")

# Plot x, y, final temperature matrix with the inferno colour scheme
plt.contourf(x,y,T[-1,:,:], cmap='inferno')

# Plot lines to indicate where bread and filling meet
plt.plot([0, XL*1000],[bread_thickness*1000,bread_thickness*1000], color='gray', linestyle='dotted')
plt.plot([0,XL*1000],[(bread_thickness+filling_thickness)*1000,(bread_thickness+filling_thickness)*1000], color='gray', linestyle='dotted')

# Generate a colour bar
plt.colorbar()

plt.title("Temperature Distribution in Panini after "+str(ttl_time)+" seconds", pad=15)

# Define axes labels
plt.xlabel("Length of panini [mm]")
plt.ylabel("Height of panini [mm]")

# Save then show figure
plt.savefig('panini.png', dpi=300, bbox_inches='tight')
plt.show()
print() # Blank line

#~~~~~~~~~~~~~~~~~~~~~~~~Generate Animation~~~~~~~~~~~~~~~~~~~~~~~~~~~#

print("Generating animation...")

# Set up the figure and axes by calling plt.subplots
# Also defining the figure size
fig, ax = plt.subplots(figsize=(10,6))

#Set the axes range so that they do not auto scale during the animation
ax.set(xlim=(0,(XL)*1000),ylim=(0,(YL)*1000))

#Label the axes
ax.set_xlabel("Length of panini [mm]")
ax.set_ylabel("Height of panini [mm]")

#Initialise the heatmap
heatmap = ax.pcolormesh(x,y,T[0,:-1,:-1], vmin=initial_temperature, vmax=T_plate+10, cmap='inferno')
# use a colourmesh, defining length, height and intial temperature matrix
# Set the minimum & maximum temperature value on the colourscale
# Use the colourscheme 'inferno' (because it looks coolest)

#Generate the colourbar for the heatmap
fig.colorbar(heatmap)


# define a function that will be called later
def animate(i):
    heatmap.set_array(T[i,:-1,:-1].flatten())
    #.flatten() will collapse a matrix into a 1D array
    ax.set_title("Temperature Distribution in Panini at Time = "+str(round(i*k,1))+" s")
    # Apply a dynamic title, which will show the time to one decimal place
    
    # This plots lines indicating where bread and filling meet
    ax.plot([0, XL*1000],[bread_thickness*1000,bread_thickness*1000], color='gray', linestyle='dotted')
    ax.plot([0,XL*1000],[(bread_thickness+filling_thickness)*1000,(bread_thickness+filling_thickness)*1000], color='gray', linestyle='dotted')
    
    
#Speed of video relative to real time
# E.g. speed_factor = 5 delivers video x5 faster than realtime
speed_factor = 2

anim = FuncAnimation(fig, animate, interval=(k*1000/speed_factor), frames=len(T))
# Use the predefined FuncAnimation
# input the 'fig' defined in line 244
# and input the animate func defined in line 263
# this interval gives x5 faster video (argument is in milliseconds)
print("Animation generated successfully!", end='\n')

# This code will generate an mp4 file
print("Generating mp4...")
anim.save('panini.mp4', dpi=150) # save as mp4
print("Successfully saved as panini.mp4", end='\n')

print() # Blank line

# This code will generate a gif
#print("Generating gif...")
#anim.save('panini.gif', writer='imagemagick', dpi=150) # save as gif
#print("Successfully saved as panini.gif")
#print()

#~~~~~~~~~~~~~~~~Deliver summary of info to user~~~~~~~~~~~~~~~~~#

print("The panini was cooked for "+str(ttl_time)+" seconds at "+str(T_plate)+" degC")

# Calculate minimum temperature in final panini
min_temp = np.min(T[-1])
min_temp = round(min_temp, 2) # round the value

# Calculate maximum temperature in the final panini
flat_temps = T[-1,:,:].flatten()
max_temp = initial_temperature
for i in range(0,len(flat_temps)):
    if flat_temps[i] > max_temp and flat_temps[i] != T_plate:
        max_temp = flat_temps[i]

print("The minimum temperature in the panini is "+str(min_temp)+" degC")
print("The maximum temperature in the panini is "+str(round(max_temp,2))+" degC")

# Deliver warnings to user:
hotwarning = False
coldwarning = True

if max_temp > 50:
    hotwarning = True

if min_temp > 20:
    coldwarning = False
    
if hotwarning == True and coldwarning == True:
    print("Warning! The panini is really badly cooked. Risk of a terrible food experience.")

if hotwarning == False and coldwarning == True:
    print("Warning! The panini is cold")

if hotwarning == True and coldwarning == False:
    print("Warning! The panini is hot!")

#~~~~~~~~~~~~~~~~~~~~Celebrate~~~~~~~~~~~~~~~~~~#
    
print()

open_image("panini.png")

startfile("panini.mp4")

open_image('Dont-Open-Surprise-Inside.jpg')

print("Here's your panini. Enjoy!")
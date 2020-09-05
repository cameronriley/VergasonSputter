# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 00:13:04 2020

@author: Cameron Riley
"""

from tkinter import *
from math import *
import numpy as np
import matplotlib.pyplot as plt


class testwindow:
    def __init__(self, master):
        self.master = master
        master.title('Window')
        
        #Variables which are adjusted by entries
        self.disc1_rotation = 0     #total amount disc 1 has been rotated
                                    #initially 0, set by user
        self.disc2_rotation = 0     #total amount disc 2 has been rotated
                                    #initially 0, set by user
        self.arm1_rotation = 0      #total amount arm1 has been rotated
                                    #initially 0, set by user
        self.disc1rad = 2   #radius of larger disc, disc1
                            #set here, fixed throughout
        self.rad1 = 1   #distance between disc1 center, disc2 center
                        #set here, fixed throughout
        self.rad2 = 1   #distance between disc2 center, arm base
                        #set here, fixed throughout
        
        self.table_rotation = 0 #total amount turntable (platen) has been rotated
                                #initially 0, set by user
        
        self.arm1_insert = 0    #length from arm base to knuckle (extension out of discs)
                                #initially 0, set by user
        self.arm1_finger = 1    #length from knuckle to nozzle
                                #set here, fixed throughout
        self.arm1_knuckle_angleout = 0  #angle relative to horizontal of arm finger
                                        #straight out is 0, positive is clockwise, neg is ccw
                                        #initially 0, set by user
        
        #internal variables to track: 
        #locations in space of: disc1 center, disc2 center, arm base,
        #arm knuckle, arm nozzle, nozzle target
        #NOTE: coordinates are in cartesian because to make plots I have to have 
            #2d viewpoints from front, side, top
            #can easily convert to polar/cylindrical, or spherical if desired w formulae
            
            #disc1 location
        self.disc1_centerx = 0
        self.disc1_centery = -3
        self.disc1_centerz = 2
            #disc2 location
        self.disc2_centerx = 1
        self.disc2_centery = 0
        self.disc2_centerz = 0
            #arm1 base location
        self.arm1x = 0
        self.arm1y = 0
        self.arm1z = 0
            #arm1 knuckle 
        self.arm1_knucklex = 0
        self.arm1_knuckley = 0
        self.arm1_knucklez = 0
            #arm1 nozzle
        self.arm1_nozzlex = 0
        self.arm1_nozzley = 0
        self.arm1_nozzlez = 0
            #arm1 target
        self.arm1_targetx = 0
        self.arm1_targety = 0
        self.arm1_targetz = 0

                
        #Visual setup of the window with which user interacts
        #General naming scheme: 
            #1. self: means that for this instance of a setup, the value is consistent
            #throughout all calculations performed. We fix the value until changed manually
            #2. name. eg disc1rotateby is concerned with how much the user rotates disc1
            #3. type of widget (Tkinter name for window item)
            #examples include: label, button, entry (text entry)
        #On the next line, .grid places the widget on the window, with specified row, col
        #Anything that says 'master' refers to the fact that it is being placed
            #on the master window aka the main one. You could make other windows if wanted
            
        #other things to know: 
            #str is the command for converting something to a string
                #python can't add strings with other data types
            #for buttons, there is a 'command = lambda : ' 
                #this just means that when the button is pressed, the command is executed
                #commands in these cases are methods which do tasks,
                #such as find values given certain inputs, or draw diagrams based on values
                #all methods are listed below the window setup definition
            
        #Row 0: Disc1 rotation
        #method rotatedisc1 : rotate disc1 by user input value
        self.disc1rotateby_label = Label(master, text = "Rotate Disc1 by: (rad)")
        self.disc1rotateby_label.grid(row = 0, column = 0)
        self.disc1rotateby_entry = Entry(master)
        self.disc1rotateby_entry.grid(row = 0, column = 1)
        self.disc1rotate_button = Button(master, text = 'Rotate Disc1', 
                                         command = lambda : self.rotatedisc1())
        self.disc1rotate_button.grid(row = 0, column = 2)
        self.disc1rotatetotal_label1 = Label(master, text = "Total Disc1 Rotation = ")
        self.disc1rotatetotal_label1.grid(row = 0, column = 3)
        self.disc1rotatetotal_label2 = Label(master, text = str(round(self.disc1_rotation, 4))
                                            + " radians")
        self.disc1rotatetotal_label2.grid(row = 0, column = 4)
        
        #Row 1: Disc2 rotation
        #method rotatedisc2 : rotate disc2 by user input value
        self.disc2rotateby_label = Label(master, text = "Rotate Disc2 by: (rad)")
        self.disc2rotateby_label.grid(row = 1, column = 0)
        self.disc2rotateby_entry = Entry(master)
        self.disc2rotateby_entry.grid(row = 1, column = 1)
        self.disc2rotate_button = Button(master, text = 'Rotate Disc2', 
                                         command = lambda : self.rotatedisc2())
        self.disc2rotate_button.grid(row = 1, column = 2)
        self.disc2rotatetotal_label1 = Label(master, text = "Total Disc2 Rotation = ")
        self.disc2rotatetotal_label1.grid(row = 1, column = 3)
        self.disc2rotatetotal_label2 = Label(master, text = str(round(self.disc2_rotation, 4))
                                             + " radians")
        self.disc2rotatetotal_label2.grid(row = 1, column = 4)
        
        #Row 2: finger length (fixed above)
        self.arm1fingerlength = Label(master, text = "Arm Finger Length = " 
                                      + str(self.arm1_finger))
        self.arm1fingerlength.grid(row = 2, column = 0)
        
        #Row 3: Arm1 Insert
        #method armsidediagram : show side diagram of setup, including arm
        self.arm1insert_label = Label(master, text = "Arm1 Insert Length: ")
        self.arm1insert_label.grid(row = 3, column = 0)
        self.arm1insert_entry = Entry(master)
        self.arm1insert_entry.grid(row = 3, column = 1)
        self.arm1insert_button = Button(master, text = "Extend Insert", 
                                       command = lambda : self.arm1extendinsert())
        self.arm1insert_button.grid(row = 3, column = 2)
        self.arm1inserttotal_label1 = Label(master, text = "Total Insert Length = ")
        self.arm1inserttotal_label1.grid(row = 3, column = 3)
        self.arm1inserttotal_label2 = Label(master, text = str(round(self.arm1_insert, 4))
                                            + " (UNITS)")
        self.arm1inserttotal_label2.grid(row = 3, column = 4)
        
        #Row 4: Arm1 extension/elevation
        #method arm1bendknuck : bend arm knuckle by user input value
        self.arm1knuckangle_label = Label(master, text = "Arm1 Knuckle Angle (up/down)")
        self.arm1knuckangle_label.grid(row = 4, column = 0)
        self.arm1knuckangle_entry = Entry(master)
        self.arm1knuckangle_entry.grid(row = 4, column = 1)
        self.arm1knuckangle_button = Button(master, text = 'Bend Arm1 Finger', 
                                      command = lambda : self.arm1bendknuck())
        self.arm1knuckangle_button.grid(row = 4, column = 2)
        self.arm1knuckangletotal_label1 = Label(master, text = "Total Knuckle Angle = ")
        self.arm1knuckangletotal_label1.grid(row = 4, column = 3)
        self.arm1knuckangletotal_label2 = Label(master, 
                            text = str(round(self.arm1_knuckle_angleout, 4)) + " radians")
        self.arm1knuckangletotal_label2.grid(row = 4, column = 4)

        
        #Row 5: Arm Rotation 
        #method rotatearm1 : rotate arm1 by user input value
        self.arm1rotateby_label = Label(master, text = "Rotate Arm 1 by: ")
        self.arm1rotateby_label.grid(row = 5, column = 0)
        self.arm1rotateby_entry = Entry(master)
        self.arm1rotateby_entry.grid(row = 5, column = 1)
        self.arm1rotateby_button = Button(master, text = 'Rotate Arm1', 
                                           command = lambda : self.rotatearm1())
        self.arm1rotateby_button.grid(row = 5, column = 2)
        self.arm1rotatetotal_label1 = Label(master, text = "Total Arm1 Rotation = ")
        self.arm1rotatetotal_label1.grid(row = 5, column = 3)
        self.arm1rotatetotal_label2 = Label(master, text = str(round(self.arm1_rotation, 4))
                                            + " radians")
        self.arm1rotatetotal_label2.grid(row = 5, column = 4)
        
        #Row 6: Buffer : blank line to make window less crowded
        self.row6buffer = Label(master, text = "")
        self.row6buffer.grid(row = 6, column = 0)
        
        #Row 7: Base diagram
        #method armbasediagram : front view diagram, looking head on at discs
        self.armbase_button = Button(master, text = "Arm Base Diagram", 
                                     command = lambda : self.armbasediagram())
        self.armbase_button.grid(row = 7, column = 0)
        #method sideviewdiagram : side view diagram, looking at arm from side
        self.sideview_button = Button(master, text = "Full Side Diagram", 
                                      command = lambda : self.sideviewdiagram())
        self.sideview_button.grid(row = 7, column = 2)
        #method topviewdiagram : top view diagram, looking from overhead at arm, table (platen)
        self.topview_button = Button(master, text = 'Top View Diagram', 
                                     command = lambda : self.topviewdiagram())
        self.topview_button.grid(row = 7, column = 4)
        
        #Row 8: Buffer : balnk line to make window less crowded
        self.row8buffer = Label(master, text = "")
        self.row8buffer.grid(row = 8, column = 0)

        #Row 9 : turntable rotation labels + entry
        #method rotateby : rotate table (platen) by user input value
        #disc1, disc2, and all arms stay fixed when table rotated
        self.tablerotate_label1 = Label(master, text = "Rotate Turntable by: (rad)")
        self.tablerotate_label1.grid(row = 9, column = 0)
        self.tablerotate_entry = Entry(master)
        self.tablerotate_entry.grid(row = 9, column = 1)
        self.tablerotate_button = Button(master, text = "Press to Rotate:", 
                                      command = lambda : self.rotatetable())
        self.tablerotate_button.grid(row = 9, column = 2)
        self.tablerotate_label2 = Label(master, text = "Total Table Rotation =  " )
        self.tablerotate_label2.grid(row = 9, column = 3)
        self.tablerotatetotal_label = Label(master, text = str(self.table_rotation) + " Radians")
        self.tablerotatetotal_label.grid(row = 9, column = 4)
        
        #Row 10: Spray, reset
        #method spray: simulate spray from nozzle aimed at target. Find associated 
        #spray values at locations determined below (arrrows, arrcols is first line)
        #for now, spray values are relative, and some assumptions have been made
        #if updating calculation of spray values is desired, edit method spray
        #for instance currently spray is emitted from one point. desired configuration
        #is for spray to be emitted from a ring, centered at current nozzle location, 
        #along some circle at some distance from current nozzle location
        self.spray_button = Button(master, text = "Spray: ", 
                                   command = lambda : self.spray())
        self.spray_button.grid(row = 10, column = 0)
        self.sprayreset_button = Button(master, text = "Reset", 
                                   command = lambda : self.resetspray())
        self.sprayreset_button.grid(row = 10, column = 2)
        
        #indexing 3d array is array(sheet, row, column)
        #For python's indexing, 
        #plane 0 is radius, plane 1 is angle/theta, plane 2 is z, plane 3 is spray thickness
        
        #We set up a 3d array
        #The 3d array has 4 2d arrays:
            #plane 0 is radius
            #plane 1 is angle/theta
            #plane 2 is z
            #plane 3 is spray thickness
        #each entry in a particular 2d array corresponds to a location on the table (platen), 
        #and the values at that index in different planes correspond to different values
        #for that physical location
        
        #EXAMPLE: Say we take the top left entry: row 0, column 0
        #That row 0, column 0 entry corresponds to the top left hand corner of the platen
        #On plane 0, row 0, column 0, the value tells us the current raidus of 
            #the top left hand corner of the platen
        #On plane 1, row 0, column 0, the value tells us the current theta of 
            #the top left hand corner of the platen
        #On plane 2, row 0, column 0, the value tells us the current z of
            #the top left hand corner of the platen
        #On plane 3, row 0, column 0, the value tells us the current spray thickness of
            #the top left hand corner of the platen
            
        #Think of the 3d array like a rectangular prism
        #Each 2d array within the 3d array is a horizontal slice
        #A given horizontal slice tells us something about certain locations on the platen
            #either radius, theta, z, or spray thickness
            
        #We have two 3d arrays: obarr and spacearr
        #obarr keeps track of the points on the object relative to the platen
            #(object is just whatever is being sprayed)
        #spacearr keeps track of the points on the object in space, 
            #relative to the origin of the system
            
        #one way to think about this:
        #Say we have a cup on a table
        #obarr keeps track of where the cup is on the table
            #For instance: Say we paint the top left hand corner of the table blue
            #Now say we put a cup in this blue region, in the top left hand corner
            #Regardless of how we rotate or translate the table, 
            #the cup is still in the region painted blue, even if the table is oriented
            #in such a way that the blue region is no longer the top left hand corner
            #This is what obarr keeps track of 
        #spacearr keeps track of where the cup is in space
            #For instance: Say we have the same setup as above:
            #a cup in the top left hand corner of the table, which is painted blue
            #If we rotate or translate the table, spacearr tells us where in the room the cup is
            
            #Example: If we translate the table upward, the obarr coordinates will stay the same
            #This is because the cup is still on the surface of the table, 
                #in the region painted blue
            #BUT, the spacearr coordinates will change, because now we have a translation in z
            #The cup is further away from the floor than it was originally
        
        #So essentially how these work:
            #We keep track of how far the platen has been rotated in either direction
            #(Translation could come in the future but not right now)
            #Using the initial coordinates stored in obarr, plus the overall rotation(s)
            #We find the new spatial coordinates, and put them in spacearr
            #Then we find the thickness of spray @ that location in space using spacearr
            
        #NOTE: regardless of the location in space, similar entries correspond to 
            #the same location on the platen
        #Example: say, as above, we paint the top left hand corner of the platen blue
        #This would correspond to row 0, column 0, the top left hand corner of our 2d arrays
        #Every time we rotate the platen, regardless of its location in space,
        #The entry in row 0, column 0, corresponds to that blue painted region
            #that was originally the top left hand corner
        #So if we rotated the platen 90 degrees ccw, the blue region would physically be
        #in the third quadrant (bottom left, instead of original top left)
        #But, the blue region still corresponds to row 0, column 0, the top left array entry
        
        #This is how we are able to keep track of spots on the platen, even when rotated
            
        #NOTE: r, theta, z are defined relative to origin of system
        #NOTE: origin of system is assumed to be at center of table (platen)
        
        arrrows = 13    #odd # of rows, columns, so middle row is y=0, middle column is x=0
        arrcols = 11    #probably easiest to make square
                        #currently setup to only work with odd arrrows, arrcols
                        
        #obarr, spacearr arrays, as described above
        self.obarr = np.zeros((4, arrrows, arrcols))
        self.spacearr = np.zeros((3, arrrows, arrcols))
        
        #we split in half so that origin is in middle exactly
        self.halfrow = floor(arrrows/2)  
        self.halfcol = floor(arrcols/2)  #variables used to save time doing math repeatedly
        
        #run through coordinates, assign initial values for r, t, z
        #spray value initally 0 by default
        for x in range(-1 * self.halfcol, self.halfcol + 1):
            for y in range(-1 * self.halfrow, self.halfrow + 1):
                z = 0 #assume flat object on table for testing purposes
                #convert cartesian coordinates to polar coordinates, put into arrays
                temp = cart2polar(x,y,z)
                
                self.obarr[0, int(self.halfrow-y), int(self.halfcol+x)] = temp[0]
                self.obarr[1, int(self.halfrow-y), int(self.halfcol+x)] = temp[1]
                self.obarr[2, int(self.halfrow-y), int(self.halfcol+x)] = temp[2]
                
                self.spacearr[0, int(self.halfrow-y), int(self.halfcol+x)] = temp[0]
                self.spacearr[1, int(self.halfrow-y), int(self.halfcol+x)] = temp[1]
                self.spacearr[2, int(self.halfrow-y), int(self.halfcol+x)] = temp[2]
        
        '''
        #Print statements if you want to check validity of array initialization
        #plane 0 is r, plane 1 is t, plane 2 is z, plane 3 is spray thickness
        print(self.obarr[1])
        print(self.spacearr[1])
        '''
        
    #METHOD 1: rotatetable
    #Given user input, change total rotation value of table (self.table_rotation)
    #Adjust coordinates in obarr, spacearr, according to new value of self.table_rotation
    def rotatetable(self):
        print("Rotate button works")
        rot_added = float(self.tablerotate_entry.get())
        self.table_rotation += rot_added    #add new rotation to old rotation
        self.tablerotatetotal_label['text'] = str(round(self.table_rotation, 4)) + " Radians"
        
        #once we know amount rotated in space, update spatial coords to reflect that
        for i in range(-1 * self.halfcol, self.halfcol + 1):
            for j in range(-1 * self.halfrow, self.halfrow + 1):
                if i!=0 or j != 0:
                    self.spacearr[1, int(self.halfrow-j), int(self.halfcol+i)] += rot_added
         
    #METHOD 2: spray
    #Given all other values have been set (coordinates of disc centers, arm bases,
        #knuckles, nozzles, targets), use spray formula to calculate thickenss at 
        #certain spatial coordinates, which correspond to certain locations on the platen
    #Add new spray thickness to original spray thickness (prior to this spray) in spacearr
    def spray(self):
        #create nozzle, target objects based on input entries (convert from cart to polar)
        nozzler = sqrt(self.arm1_nozzlex ** 2 + self.arm1_nozzley ** 2)
        nozzlet = atan2(self.arm1_nozzley, self.arm1_nozzlex)
        #define nozzle object
        noz = nozzle(nozzler, nozzlet, self.arm1_nozzlez)
        
        targetr = sqrt(self.arm1_targetx ** 2 + self.arm1_targety ** 2)
        targett = atan2(self.arm1_targety, self.arm1_targetx)
        #define target object
        tar = target(targetr, targett, self.arm1_targetz)
        
        for i in range(-1 * self.halfcol, self.halfcol + 1):
            for j in range (-1 * self.halfrow, self.halfrow + 1):
                #define location object
                loc = location(self.spacearr[0, int(self.halfrow-j), int(self.halfcol+i)], 
                               self.spacearr[1, int(self.halfrow-j), int(self.halfcol+i)], 
                               self.spacearr[2, int(self.halfrow-j), int(self.halfcol+i)])
                #call sprayval method, which determines spray thickenss at location
                #given nozzle coords, target coords, location coords
                sprayval = noz.aim_at(tar, loc)
                #update obarr values to add new spray thickness to old spray thickness
                self.obarr[3, int(self.halfrow-j), int(self.halfcol+i)] += sprayval
                
        #create color map of relative spray values
        #NOTE: color map axes currently display incorrect values
        #I have not had time to figure out how to change them
        #Documentation is in matplotlib
        #Want: middle row = 0, below negative, above positive
        #Want: middle column = 0, left negative, right positive
        #Want these because middle entry (middle row, middle column)
            #corresponds to origin of our coordinate system
        get_ipython().run_line_magic('matplotlib', 'qt')
        plt.pcolormesh(self.obarr[3], cmap = 'jet')
        
        
         
    #METHOD 3: resetspray
    #Reset everything to zero: table rotation, spray values at every point on table
    #NOTE: resetspray does not reset rotations, locations of discs, arms, nozzles, etc
    def resetspray(self):
        for i in range(-1 * self.halfcol, self.halfcol + 1):
            for j in range(-1 * self.halfrow, self.halfrow + 1):
                #reset spray values to zero for everywhere on object
                self.obarr[3, int(self.halfrow-j), int(self.halfcol+i)] = 0
                #backslash at end of next line means continued onto next line
                #reset spacecoords to initial object coords
                self.spacearr[1, int(self.halfrow-j), int(self.halfcol+i)] \
                    = self.obarr[1, int(self.halfrow-j), int(self.halfcol+i)]
        
        #reset table rotation, corresponding label
        self.table_rotation = 0
        self.tablerotatetotal_label["text"] = 0
        
        #uniform color map to show reset
        get_ipython().run_line_magic('matplotlib', 'qt')
        plt.pcolormesh(self.obarr[3], cmap = 'jet')
        
    #METHOD 4: rotatedisc1
    #rotate disc1 by input value from disc1 entry box
    #update arm coordinates to reflect disc rotation
    def rotatedisc1(self):
        self.disc1_rotation += float(self.disc1rotateby_entry.get())
        self.disc1rotatetotal_label2['text'] = str(round(self.disc1_rotation, 4)) + " radians"
        #after rotating disc1, find new arm base location
        self.locatearmbase()
        #given new arm base location, find new knuckle, nozzle, target locations
        self.knucknoztar()
        
    #METHOD 5: rotatedisc2
    #rotate disc2 by input value from disc2 entry box 
    #update arm coordinates to reflect disc rotation
    def rotatedisc2(self):
        self.disc2_rotation += float(self.disc2rotateby_entry.get())
        self.disc2rotatetotal_label2['text'] = str(round(self.disc2_rotation, 4)) + " radians"
        #after rotating disc2, find new arm base location
        self.locatearmbase()
        #given new arm base location, find new knuckle, nozzle, target locations
        self.knucknoztar()
        
    #METHOD 6: rotatearm1
    #rotate arm1 by input value from arm1 entry box
    #update arm coordinates to reflect arm rotation
    def rotatearm1(self):
        self.arm1_rotation += float(self.arm1rotateby_entry.get())
        self.arm1rotatetotal_label2['text'] = str(round(self.arm1_rotation, 4)) + " radians"
        #after rotating arm1, find arm1 knuckle, nozzle, target
        self.knucknoztar()
        
    #METHOD 7: arm1extendinsert
    #adjust arm1 insert length by input value from insert entry box
    #update arm coordinates to relflect insert extention/retraction
    def arm1extendinsert(self):
        self.arm1_insert += float(self.arm1insert_entry.get())
        self.arm1inserttotal_label2['text'] = str(round(self.arm1_insert, 4)) + " (UNITS)"
        #after adjusting insert length or knuckle angle, find arm1 knuckle, nozzle, target
        self.knucknoztar()
        
    #METHOD 8: arm1bendknuck
    #rotate arm1 knuckle from knuckle entry box
    #update arm coordinates to reflect finger bend (knuckle angle change)
    def arm1bendknuck(self):
        self.arm1_knuckle_angleout += float(self.arm1knuckangle_entry.get())
        self.arm1knuckangletotal_label2['text'] = str(round(self.arm1_knuckle_angleout, 4)) + " radians"
        #after adjusting insert length or knuckle angle, find arm1 knuckle, nozzle, target
        self.knucknoztar()
        

    #METHOD 9: locatearmbase 
    #given rotations of discs, sizes of discs, (non concentric)
    #locate arm base, a point on the smaller disc
    #NOTE: If the math is unclear in this section, it can help to draw a sample setup
    #Of disc1, disc2, and arm1 base to better visualize
    def locatearmbase(self):
        #relevant parameters: assign to temp variables to reduce memory, time
        disc1_rotation = self.disc1_rotation   #disc1 total rotation
        disc2_rotation = self.disc2_rotation    #disc2 total rotation
        rad1 = self.rad1    #rad1 = distance between disc1 center, disc2 center
        rad2 = self.rad2    #rad2 = distance between disc2 center, arm base
        disc1rad = self.disc1rad    #radius of larger disc, disc1
        
        #disc1 center coordinates
        disc1_centerx = self.disc1_centerx  
        disc1_centery = self.disc1_centery
        disc1_centerz = self.disc1_centerz
        
        #disc2 center coordinates
        disc2_centerx = disc1_centerx + rad1 * cos(disc1_rotation)
        disc2_centery = disc1_centery #both discs are coplanar
        disc2_centerz = disc1_centerz + rad1 * sin(disc1_rotation)
        
        #update values
        self.disc2_centerx = disc2_centerx
        self.disc2_centery = disc2_centery
        self.disc2_centerz = disc2_centerz
        
        #use law of cosines to find distance between disc1 center, arm1
        #armd2d1 angle is from arm base --> disc2 center --> disc1 center
        armd2d1_angle = abs(pi - disc2_rotation) #angle c: pi radians - disc2 rotation
        arm1_center_dist = sqrt(rad1**2 + rad2**2 - 2 * rad1 * rad2 * cos(armd2d1_angle))
        #using all 3 side lengths, find polar angle from disc1 center to arm1
        hold = arm1_center_dist**2 + rad1**2 - rad2**2 #hold = temp variable
        hold /= (2 * arm1_center_dist * rad1)
        #armd1d2 angle is from arm base --> disc1 center --> disc2 center
        armd1d2_angle = acos(hold) 
        
        #armd1vert_angle is angle of right triangle
        #arm1_center_dist is hypotenuse of right triangel
        if disc2_rotation % (2*pi) < pi and disc2_rotation % (2*pi) > 0:
            armd1vert_angle = disc1_rotation + armd1d2_angle
        else:
            armd1vert_angle = disc1_rotation - armd1d2_angle
        
        #given distances relative to disc1 center, find coordinates in space
        arm1x = disc1_centerx + arm1_center_dist * cos(armd1vert_angle)
        arm1y = disc1_centery
        arm1z = disc1_centerz + arm1_center_dist * sin(armd1vert_angle)
        
        #update
        self.arm1x = arm1x
        self.arm1y = arm1y
        self.arm1z = arm1z        
       
    #METHOD 10: knucknoztar
    #Assuming already found arm base, find location of arm knuckle, arm nozzle, nozzle target
    #Nozzle target is where nozzle is pointed
    #Assume intersection at z=0 plane. If pointed straight out or up, stop before infinity
    def knucknoztar(self):
        #relevant values
        insert1 = self.arm1_insert
        finger1 = self.arm1_finger
        disc1_rotation = self.disc1_rotation
        disc2_rotation = self.disc2_rotation
        
        #find knuckle pixels
        arm1_knucklex = self.arm1x           #arm1 knuckle has same x, z since it extends straight out
        arm1_knuckley = self.arm1y + insert1 #arm1 knuckle has y offset by fixed insert length    
        arm1_knucklez = self.arm1z
        
        #NOTE: user_rotation and arm1_knuckleangle are both user entry inputs. for now fixed
        user_rotation = self.arm1_rotation
        arm1_knuckleangle = self.arm1_knuckle_angleout
        
        arm1_finger_xzangle = -pi/2 + disc1_rotation + disc2_rotation + user_rotation
        
        arm1_nozzley = arm1_knuckley + finger1 * cos(arm1_knuckleangle)
        arm1_nozzlex = arm1_knucklex + finger1 * sin(arm1_knuckleangle) * cos(arm1_finger_xzangle)
        arm1_nozzlez = arm1_knucklez + finger1 * sin(arm1_knuckleangle) * sin(arm1_finger_xzangle)
        
        #Given the knuckle and nozzle, extend the line (if applicable) to find the target
        #use parametric equation. values x0, y0, etc. are placeholders
        x0 = arm1_knucklex
        y0 = arm1_knuckley
        z0 = arm1_knucklez
        x1 = arm1_nozzlex
        y1 = arm1_nozzley
        z1 = arm1_nozzlez
        
        #NOTE: technically the length that the line from the nozzle is extended is irrelevant
        #This is because we care about 3 things when finding the spray value:
            #1. distance from nozzle to location @ which we measure spray thickness (s)
            #2. angle from target --> nozzle --> location (eta)
            #3. angle from nozzle --> location --> vertical (alpha)
        #None of these depend on the distance between the nozzle and the target.
        #However, using simple values like z=0 makes it easier to debug
        
        #if pointed down, find intersection w z=0 plane
        if arm1_nozzlez < arm1_knucklez:
            t = z0 / (z0 - z1)
            arm1_targetz = 0
            arm1_targetx = x0 + (x1 - x0) * t
            arm1_targety = y0 + (y1 - y0) * t
        #if pointed straight out or up, stop before infinity
        else:
            arm1_targetx = (2 * x1) - x0
            arm1_targety = (2 * y1) - y0
            arm1_targetz = (2 * z1) - z0
            
        #update values  
        self.arm1_knucklex = arm1_knucklex
        self.arm1_knuckley = arm1_knuckley
        self.arm1_knucklez = arm1_knucklez
        
        self.arm1_nozzlex = arm1_nozzlex
        self.arm1_nozzley = arm1_nozzley
        self.arm1_nozzlez = arm1_nozzlez
        
        self.arm1_targetx = arm1_targetx
        self.arm1_targety = arm1_targety
        self.arm1_targetz = arm1_targetz
        
    #METHOD 11: armbasediagram
    #given rotation of discs, location of disc centers, location of arm, make diagram
    #(x-z plane, y fixed)
    #Front view diagram, looking directly at two discs which contain arms
    #Diagram aligned so that center of window is center of disc1, not origin of system
    
    #NOTE: tkinter expression formatting
        #here, w is a window. We could easily have named it anything else, but
            #w is self explanatory and simple
        #to create a line: w.create_line(x0, y0, x1, y1)
        #to create an oval: w.createline(top left x, top left y, bottom left x, bottom left y)
        #to put text somewhere: w.create_text(text center x, text center y, text = 'words')
        
    def armbasediagram(self):
        #define window
        width_total = 600
        height_total = 600
        
        master = Tk()
        w = Canvas(master, width = width_total, height = height_total)
        w.pack()
        
        #define drawing bounds
        bound_left = width_total * 0.05
        bound_right = width_total * 0.95
        bound_top = height_total * 0.05
        bound_bot = height_total * 0.95
        
        #borders
        w.create_line(bound_left, bound_bot, bound_left, bound_top)
        w.create_line(bound_left, bound_top, bound_right, bound_top)
        w.create_line(bound_right, bound_top, bound_right, bound_bot)
        w.create_line(bound_right, bound_bot, bound_left, bound_bot)
        
        #LEGEND
        halfborder = 0.05 * width_total / 2 #text halfway down border
        #disc1
        w.create_oval(width_total / 12 - 5, bound_top - halfborder - 5,
                      width_total / 12 + 5, bound_top - halfborder + 5, fill = 'red')
        w.create_text(width_total * 2 / 12, bound_top - halfborder, text = 'Disc1 Center')
        #disc2
        w.create_oval(width_total * 3 / 12 - 5, bound_top - halfborder - 5,
                      width_total * 3 / 12 + 5, bound_top - halfborder + 5, fill = 'blue')
        w.create_text(width_total * 4 / 12, bound_top - halfborder, text = 'Disc2 Center')
        #arm1
        w.create_oval(width_total * 5 / 12 - 5, bound_top - halfborder - 5,
                      width_total * 5 / 12 + 5, bound_top - halfborder + 5, fill = 'orange')
        w.create_text(width_total * 6 / 12, bound_top - halfborder, text = 'Arm1 Base')
        #nozzle
        w.create_oval(width_total * 7 / 12 - 5, bound_top - halfborder - 5,
                      width_total * 7 / 12 + 5, bound_top - halfborder + 5, fill = 'green')
        w.create_text(width_total * 8 / 12, bound_top - halfborder, text = 'Arm1 Nozzle')
        #target
        w.create_oval(width_total * 9 / 12 - 5, bound_top - halfborder - 5,
                      width_total * 9 / 12 + 5, bound_top - halfborder + 5, fill = 'yellow')
        w.create_text(width_total * 10 / 12, bound_top - halfborder, text = 'Nozzle Target')
        
        #relevant values for pixel calculations
        disc1_rotation = self.disc1_rotation
        disc2_rotation = self.disc2_rotation
        
        rad1 = self.rad1
        rad2 = self.rad2
        
        disc1_centerx = self.disc1_centerx
        disc1_centery = self.disc1_centery
        disc1_centerz = self.disc1_centerz
        
        disc2_centerx = self.disc2_centerx
        disc2_centery = self.disc2_centery
        disc2_centerz = self.disc2_centerz
        
        arm1x = self.arm1x
        arm1y = self.arm1y
        arm1z = self.arm1z
        
        arm1_nozzlex = self.arm1_nozzlex
        arm1_nozzley = self.arm1_nozzley
        arm1_nozzlez = self.arm1_nozzlez
        
        arm1_targetx = self.arm1_targetx
        arm1_targety = self.arm1_targety
        arm1_targetz = self.arm1_targetz
        
        #NOTE: If rad1 + rad2 > disc1rad, then define scale using (rad1 + rad2) instead
        #use radius of larger disc to define scale for diagram
        disc1rad = self.disc1rad
        finger1 = self.arm1_finger
        #pixels in a unit square
        #given coordinates, just multiply by #pixels in a unit square, translate if necessary
        #here is where you would replace disc1rad with (rad1 + rad2), if necessary
        unit_pixels = (bound_right - bound_left) / (2 * (disc1rad + finger1))   
        
        #pixel coords of disc1 center (center of window), origin
        disc1_centerx_pixels = (bound_left + bound_right) / 2
        disc1_centerz_pixels = (bound_top + bound_bot) / 2
        originx_pixels = disc1_centerx_pixels - disc1_centerx * unit_pixels
        originz_pixels = disc1_centerz_pixels + disc1_centerz * unit_pixels
        
        #indicate origin, draw axes
        w.create_oval(originx_pixels - 5, originz_pixels - 5, 
                      originx_pixels + 5, originz_pixels + 5, fill = 'black')
        w.create_line(bound_left, originz_pixels, bound_right, originz_pixels, width = 3)
        w.create_line(originx_pixels, bound_bot, originx_pixels, bound_top, width = 3)
        #indicate disc1 center
        w.create_oval(disc1_centerx_pixels - 5, disc1_centerz_pixels - 5, 
                      disc1_centerx_pixels + 5, disc1_centerz_pixels + 5, fill = 'red')
        #draw disc1 outline
        w.create_oval(disc1_centerx_pixels - disc1rad * unit_pixels, 
                      disc1_centerz_pixels - disc1rad * unit_pixels, 
                      disc1_centerx_pixels + disc1rad * unit_pixels,
                      disc1_centerz_pixels + disc1rad * unit_pixels, dash = (3,5))
        
        #find pixel coords of disc2
        disc2_centerx_pixels = originx_pixels + disc2_centerx * unit_pixels
        disc2_centerz_pixels = originz_pixels - disc2_centerz * unit_pixels
        
        #draw disc2 center
        w.create_oval(disc2_centerx_pixels - 5, disc2_centerz_pixels - 5, 
                      disc2_centerx_pixels + 5, disc2_centerz_pixels + 5, 
                      fill = 'blue')
        #draw disc2 outline
        w.create_oval(disc2_centerx_pixels - rad1 * unit_pixels, 
                      disc2_centerz_pixels - rad1 * unit_pixels,
                      disc2_centerx_pixels + rad1 * unit_pixels, 
                      disc2_centerz_pixels + rad1 * unit_pixels)
        #draw arm base 
        arm1x_pixels = originx_pixels + arm1x * unit_pixels
        arm1z_pixels = originz_pixels - arm1z * unit_pixels

        w.create_oval(arm1x_pixels - 5, arm1z_pixels - 5, 
                      arm1x_pixels + 5, arm1z_pixels + 5, fill = 'orange')
        
        #arm knuckle perpendicular to arm base, such that from front they overlap
        #draw arm nozzle
        arm1_nozzlex_pixels = originx_pixels + arm1_nozzlex * unit_pixels
        arm1_nozzlez_pixels = originz_pixels - arm1_nozzlez * unit_pixels
        w.create_oval(arm1_nozzlex_pixels - 5, arm1_nozzlez_pixels - 5,
                      arm1_nozzlex_pixels + 5, arm1_nozzlez_pixels + 5, fill = 'green')
        w.create_line(arm1_nozzlex_pixels, arm1_nozzlez_pixels, arm1x_pixels, arm1z_pixels)
        
        #draw nozzle target
        arm1_targetx_pixels = originx_pixels + arm1_targetx * unit_pixels
        arm1_targetz_pixels = originz_pixels - arm1_targetz * unit_pixels
        w.create_oval(arm1_targetx_pixels - 5, arm1_targetz_pixels - 5,
                      arm1_targetx_pixels + 5, arm1_targetz_pixels + 5, fill = 'yellow')
        w.create_line(arm1_targetx_pixels, arm1_targetz_pixels, 
                      arm1_nozzlex_pixels, arm1_nozzlez_pixels, dash = (3,5))
        
        
    #METHOD 12: topviewdiagram
    #given location of arm, knuckle, nozzle, target, make diagram (x-y plane, z fixed)
    #Top view diagram, looking from overhead, down at platen
    #See METHOD 11 note for tkinter expression formatting if necessary
    def topviewdiagram(self):
        #define window
        width_total = 600
        height_total = 600
        
        master = Tk()
        w = Canvas(master, width = width_total, height = height_total)
        w.pack()
        
        #define drawing bounds
        bound_left = width_total * 0.05
        bound_right = width_total * 0.95
        bound_top = height_total * 0.05
        bound_bot = height_total * 0.95
        
        #relevant values: coordinates of arm, knuckle, nozzle, target
        #plus knuckle angle
        armbasex = self.arm1x
        armbasey = self.arm1y
        armbasez = self.arm1z
        knucklex = self.arm1_knucklex
        knuckley = self.arm1_knuckley
        knucklez = self.arm1_knucklez
        knuckleangle = self.arm1_knuckle_angleout
        nozzlex = self.arm1_nozzlex
        nozzley = self.arm1_nozzley
        nozzlez = self.arm1_nozzlez
        
        targetx = self.arm1_targetx
        targety = self.arm1_targety
        targetz = self.arm1_targetz
        
        #Define graph scale to make sure everything fits in window
        #find x vals, difference between x vals, whichever is largest defines graph scale
        diffx1 = abs(armbasex - targetx)
        diffx2 = abs(armbasex + targetx)
        diffx = max(diffx1, diffx2)
        maxy = 0
        if (diffx > abs(armbasex)) and (diffx > abs(targetx)):
            maxx = diffx
        else: 
            maxx = max(abs(armbasex), abs(targetx))
        #do same w y vals
        diffy = abs(armbasey - targety)
        maxz = 0
        if (diffy > armbasey) and (diffy > targety):
            maxy = diffy
        else: 
            maxy = max(abs(armbasey), abs(targety))
            
        #define unit square size
        unit_squares = max(abs(maxx), abs(maxy))  #number of unit squares in grid
        unit_pixels = (bound_right - bound_left) / (2* unit_squares) #pixel size of unit square
        
        #since top view, make origin center of window
        originx_pixels = (bound_left + bound_right) / 2
        originy_pixels = (bound_top + bound_bot) / 2
        
        #convert spatial coordinates to pixels
        armbasex_pixels = originx_pixels + armbasex * unit_pixels
        armbasey_pixels = originy_pixels - armbasey * unit_pixels
        knucklex_pixels = originx_pixels + knucklex * unit_pixels
        knuckley_pixels = originy_pixels - knuckley * unit_pixels
        nozzlex_pixels = originx_pixels + nozzlex * unit_pixels
        nozzley_pixels = originy_pixels - nozzley * unit_pixels
        targetx_pixels = originx_pixels + targetx * unit_pixels
        targety_pixels = originy_pixels - targety * unit_pixels
        
        #LEGEND
        halfborder = 0.05 * width_total / 2
        #arm1 base
        w.create_oval(width_total / 10 - 5, bound_top - halfborder - 5,
                      width_total / 10 + 5, bound_top - halfborder + 5, fill = 'red')
        w.create_text(width_total * 2 / 10, bound_top - halfborder, text = 'Arm1 base')
        #arm1 knuckle
        w.create_oval(width_total * 3 / 10 - 5, bound_top - halfborder - 5,
                      width_total * 3 / 10 + 5, bound_top - halfborder + 5, fill = 'orange')
        w.create_text(width_total * 4 / 10, bound_top - halfborder, text = 'Arm1 Knuckle')
        #arm1 nozzle
        w.create_oval(width_total * 5 / 10 - 5, bound_top - halfborder - 5,
                      width_total * 5 / 10 + 5, bound_top - halfborder + 5, fill = 'yellow')
        w.create_text(width_total * 6 / 10, bound_top - halfborder, text = 'Arm1 Nozzle')
        #arm1 target
        w.create_oval(width_total * 7 / 10 - 5, bound_top - halfborder - 5,
                      width_total * 7 / 10 + 5, bound_top - halfborder + 5, fill = 'green')
        w.create_text(width_total * 8 / 10, bound_top - halfborder, text = 'Arm1 Target')
        
        #axes
        w.create_line(bound_left, height_total/2, bound_right, height_total/2)
        w.create_line(width_total/2, bound_bot, width_total/2, bound_top)
        
        #show radii. Possibly replace with cartesian grid lines, or use both
        #if want to use cartesian grid lines, run through (-1 * unit_squares, unit_squares + 1)
        #do that in a double for loop
        #for each x, y, draw a line from top-bottom and left-right
        #add the dash command at the end: w.create_line( (coords...) , dash = (3,5))
            #that makes a dash of 3 pixels with a gap of 5, or vice versa I forget
        #would look something like with the tick marks in METHOD 13: sideviewdiagram
        
        #grid line code starts: comment below here
        for i in range(-1 * int(unit_squares), int(unit_squares) + 1):
            w.create_line(bound_left, originy_pixels + i*unit_pixels, 
                          bound_right, originy_pixels + i*unit_pixels, dash = (3,5))
            w.create_line(originx_pixels + i*unit_pixels, bound_bot, 
                          originx_pixels + i*unit_pixels, bound_top, dash = (3,5))
        #grid line code ends: comment above here  
        #NOTE: If you only want one of the grid lines or radii, just comment it out
        
        #radii code starts: comment below here
        #make rings at radii of nozzle, target, so find radius from x,y                      
        targetr = sqrt(targetx**2 + targety**2)
        nozzler = sqrt(nozzlex**2 + nozzley**2)
        w.create_line(0, bound_bot, width_total, bound_bot, width = 3)
        w.create_oval(originx_pixels - targetr * unit_pixels, 
                      originy_pixels - targetr * unit_pixels,
                      originx_pixels + targetr * unit_pixels,
                      originy_pixels + targetr * unit_pixels, dash = (3,5))
        w.create_oval(originx_pixels - nozzler * unit_pixels,
                      originy_pixels - nozzler * unit_pixels,
                      originx_pixels + nozzler * unit_pixels,
                      originy_pixels + nozzler * unit_pixels, dash = (3,5))
        #radii code ends: comment above here
        
        #arm base, knuckle, nozzle, target, origin
        w.create_line(armbasex_pixels, armbasey_pixels, knucklex_pixels, knuckley_pixels, width = 3)
        w.create_line(knucklex_pixels, knuckley_pixels, nozzlex_pixels, nozzley_pixels, width = 3)
        w.create_line(nozzlex_pixels, nozzley_pixels, targetx_pixels, targety_pixels, dash = (3,5))
        
        #draw circle indicators
        w.create_oval(originx_pixels - 5, originy_pixels - 5, 
                      originx_pixels + 5, originy_pixels + 5, fill = 'black')
        w.create_oval(armbasex_pixels - 5, armbasey_pixels - 5, 
                        armbasex_pixels + 5, armbasey_pixels + 5, fill = 'red')
        w.create_oval(knucklex_pixels - 5, knuckley_pixels - 5,
                      knucklex_pixels + 5, knuckley_pixels + 5, fill = 'orange')
        w.create_oval(nozzlex_pixels - 5, nozzley_pixels - 5, 
                      nozzlex_pixels + 5, nozzley_pixels + 5, fill = 'yellow')
        w.create_oval(targetx_pixels - 5, targety_pixels - 5,
                      targetx_pixels + 5, targety_pixels + 5, fill = 'green')
        
        
        
        
        
    #METHOD 13: sideviewdiagram
    #Makes side view (y-z plane, x fixed) diagram, showing arm and target
    def sideviewdiagram(self):
        #define window
        width_total = 600
        height_total = 600
        
        master = Tk()
        w = Canvas(master, width = width_total, height = height_total)
        w.pack()
        
        #define drawing bounds
        bound_left = width_total * 0.05
        bound_right = width_total * 0.95
        bound_top = height_total * 0.05
        bound_bot = height_total * 0.95
        
        #label bottom surface
        w.create_line(0, bound_bot, width_total, bound_bot)
        w.create_text( (bound_left + bound_right)/2, (height_total + bound_bot)/2 + 5, 
                      text = "Discs")
        
        #relevant values: arm base, knuckle, knuckle angle, nozzle, target
        armbasey = self.arm1y
        armbasez = self.arm1z
        armknucky = self.arm1_knuckley
        armknuckz = self.arm1_knucklez
        armknuck_angle = self.arm1_knuckle_angleout
        nozzley = self.arm1_nozzley
        nozzlez = self.arm1_nozzlez
        
        targety = self.arm1_targety
        targetz = self.arm1_targetz
                                
        #find y vals, difference between y vals, whichever is largest defines graph scale
        #we want everything to fit, so either the larger of the difference, or the larger
        #of the sum
        diffy1 = abs(armbasey - targety)
        diffy2 = abs(armbasey + targety)
        diffy = max(diffy1, diffy2)
        maxy = 0
        
        #if difference > either value, make scale based off difference
        #else, use max of either one
        if (diffy > abs(armbasey)) and (diffy > abs(targety)):
            maxy = diffy
        else: 
            maxy = max(abs(armbasey), abs(targety))
        
        diffz = abs(nozzlez - targetz)
        maxz = 0
        
        if (diffz > nozzlez) and (diffz > targetz):
            maxz = diffz
        else: 
            maxz = max(abs(nozzlez), abs(targetz))
            
        #define unit square size
        unit_squares = max(abs(maxy), abs(maxz))  #number of unit squares in grid
        unit_dist = (bound_right - bound_left) / unit_squares #pixel size of unit square
        
        #determine location of origin in window (left justified, right justified, middle)
        if armbasey <= 0 and targety <= 0 :
            originy_pixels = bound_right
        elif armbasey >= 0 and targety >= 0:
            originy_pixels = bound_left
        else:
            originy_pixels = bound_left - armbasey * unit_dist
            
        basey_pixels = originy_pixels + armbasey * unit_dist
        basez_pixels = bound_bot - armbasez * unit_dist
        knuckley_pixels = originy_pixels + armknucky * unit_dist
        knucklez_pixels = bound_bot - armknuckz * unit_dist
        nozzley_pixels = originy_pixels + nozzley * unit_dist
        nozzlez_pixels = bound_bot - nozzlez * unit_dist
        targety_pixels = originy_pixels + targety * unit_dist
        targetz_pixels = bound_bot - targetz * unit_dist
        
        
        w.create_line(originy_pixels, bound_bot, originy_pixels, bound_top)
        w.create_line(basey_pixels, bound_bot, basey_pixels, bound_top, width = 5)
        w.create_line(basey_pixels, basez_pixels, knuckley_pixels, knucklez_pixels, width = 3)
        w.create_line(knuckley_pixels, knucklez_pixels, nozzley_pixels, nozzlez_pixels, width = 3)
        w.create_line(nozzley_pixels, nozzlez_pixels, targety_pixels, targetz_pixels, dash = (3,5))
        
        #tick marks on x, y axes
        #run through all x, make marks if not on x, y axis
        for x in range(-1*abs(int(maxy)), abs(int(maxy)) + 1):
            if x != 0:
                #vertical lines
                w.create_line(originy_pixels + x * unit_dist, bound_bot, 
                              originy_pixels + x * unit_dist, bound_top, dash = (1, 5))
                w.create_text(originy_pixels + x * unit_dist + 10, bound_bot + 10, 
                              text = str(x))
                
                #horizontal lines
                w.create_line(bound_left, bound_bot - x * unit_dist, 
                              bound_right, bound_bot - x * unit_dist, dash = (1, 5))
                w.create_text(originy_pixels + 10, bound_bot - x * unit_dist - 10, 
                              text = str(round(x, 2)))
                
        #base, knuckle, nozzle, target, origin
        w.create_oval(basey_pixels - 5, basez_pixels - 5, basey_pixels + 5, basez_pixels + 5,
                      fill = 'red') 
        w.create_oval(knuckley_pixels - 5, knucklez_pixels - 5,
                      knuckley_pixels + 5, knucklez_pixels + 5, fill = 'orange')
        w.create_oval(nozzley_pixels - 5, nozzlez_pixels - 5,
                      nozzley_pixels + 5, nozzlez_pixels + 5, fill = 'yellow')
        w.create_oval(targety_pixels - 5, targetz_pixels - 5,
                      targety_pixels + 5, targetz_pixels + 5, fill = 'green')
        w.create_oval(originy_pixels - 5, bound_bot - 5, originy_pixels + 5, bound_bot + 5,
                      fill = 'black')
            
        
        
        #w.mainloop actually instantiates (makes) the window and shows it
        #if nothing is showing up, make sure you have this,
        #and also make sure you have the parentheses at the end.
        #messed that up numerous times
        w.mainloop()
        
        
        
#NOTE: The following methods are not part of class testwindow.
#They are their own methods and are separate from anything else
#I guess you could do them inside but restructuring would be required
    #because they would need to inherit values
#In this way, I can all the method without any self references (ie use temp variables)
#As far as I'm aware, this is easier on memory, and takes less time
 

#method which converts input cartesian coordinates to output polar coordinates
#returns array because we need three values, not just one
def cart2polar(location_x, location_y, location_z):
    table_x = float(location_x)
    table_y = float(location_y)
    table_z = float(location_z)
    
    table_r = sqrt(table_x**2 + table_y**2)
    table_t = atan2(table_y, table_x) #angle in rad
    #table_t *= 180 / pi #uncomment to convert from rad to deg, likely not necessary
    
    return [table_r, table_t, table_z]


#creates nozzle object, with mehtod aim_at, telling how much to spray
#nozzle class contains method aim_at, which points a nozzle at a target,
#with a specified third location, where we are measuring the spray thickness
#note that the target is just where the nozzle is aimed, not where we are measuring
class nozzle:
    def __init__(self, nozzle_r, nozzle_theta, nozzle_z):
        self.nozzle_r = nozzle_r
        self.nozzle_theta = nozzle_theta #input radians
        self.nozzle_z = nozzle_z
        
    
    #nozzle is aimed at a target
    #Given positions of nozzle, target, location,
    #calculate intensity of spray at location
    def aim_at(self, target, location):
        # n = c * cos(alpha) * cos(eta)^epsilon / s^2
            # assume c = 1, epsilon = 1, therefore
        # n = cos(alpha) * cos(eta) / s^2
        
        #first find distance between nozzle (self) and target
        #d^2 = r1^2 + r2^2 -2r1r2cos(phi1-phi2) + (z1-z2)^2
        
        r1 = self.nozzle_r
        r2 = target.target_r
        r3 = location.loc_r
        phi1 = self.nozzle_theta
        phi2 = target.target_theta
        phi3 = location.loc_theta
        z1 = self.nozzle_z
        z2 = target.target_z
        z3 = location.loc_z
        
    
        #next find alpha, the nozzle-target-plane angle
        
        #leg 1
        plane_dist_noz_tar = sqrt(r1**2 + r2**2 - 2*r1*r2*cos(phi1-phi2))
        z_diff_noz_tar = z1-z2
        
        #print("Nozzle-Target plane distance = " + str(plane_dist_noz_tar))
        #print("Nozzle-Target z distance = " + str(z_diff_noz_tar))
        
        total_dist_noz_tar = sqrt(plane_dist_noz_tar**2 + z_diff_noz_tar**2)
        #s = total_dist_noz_tar
        angle_noz_tar = atan2(z_diff_noz_tar, plane_dist_noz_tar)    
        
        #cos(alpha) = sin(90 - alpha)
        #since we only need cos(alpha), not alpha itself, this is fewer steps
            #than doing alpha = acos(sin(angle_surface))
        cos_alpha = sin(angle_noz_tar)
        
        
        #now find eta, the angle from location-nozzle-target
        #use law of cosines (loc here means location not that)
        #we already have one leg
        
        #leg 2
        plane_dist_noz_loc = sqrt(r1**2 + r3**2 -2*r1*r3*cos(phi1-phi3))
        z_diff_noz_loc = z1-z3
        total_dist_noz_loc = sqrt(plane_dist_noz_loc**2 + z_diff_noz_loc**2)
        
        #leg 3
        plane_dist_tar_loc = sqrt(r2**2 + r3**2 - 2*r2*r3*cos(phi2-phi3))
        z_diff_tar_loc = z2-z3
        total_dist_tar_loc = sqrt(plane_dist_tar_loc**2 + z_diff_tar_loc)

        leg1 = total_dist_noz_tar
        leg2 = total_dist_noz_loc
        leg3 = total_dist_tar_loc
        
        #print("Nozzle-Target distance = " + str(leg1))
        #print("Nozzle-Location distance = " + str(leg2))
        #print("Target-Location distance = " + str(leg3))

        cos_eta = (leg1**2 + leg2**2 - leg3**2) / (2 * leg1 * leg2)
        #print("cos(alpha) = " + str(cos_alpha))
        #print("cos(eta) = " + str(cos_eta))
        #print("s = " + str(leg2))
        #s = leg1 : nozzle-location distance
        n = cos_eta * cos_alpha / (leg1**2)
        #print("Spray portion = " + str(n))
        return n


#target class, with properties r, theta, z
class target:
    def __init__(self, target_r, target_theta, target_z):
        self.target_r = target_r
        self.target_theta = target_theta #* pi / 180 #if degrees entered
        self.target_z = target_z
#location class, with properties r, theta z
class location:
    def __init__(self, loc_r, loc_theta, loc_z):
        self.loc_r = loc_r
        self.loc_theta = loc_theta #* pi / 180 #if degrees entered
        self.loc_z = loc_z
    
 
    
 
    

#this is how you run everything
#root = Tk() makes a Tk object and names it root
#my_gui = testwindow(root) takes the Tk object , feeds it as an argument to class testwindow
#this makes roo the parent window for testwindow, or 'master', as it is written way up there
#root.mainloop() is the same as w.mainloop() at the end of the testwindow class
#once everything is put together, mainloop() is what actually displays it


root = Tk()
my_gui = testwindow(root)
root.mainloop()















































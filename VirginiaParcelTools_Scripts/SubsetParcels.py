# ----------------------------------------------------------------------------------------
# SubsetParcels.py
# Version:  Python 2.7.5
# Creation Date: 2017-06-21
# Last Edit: 2017-10-16
# Creator:  Roy Gilb and DJ Helkowski
# Edited by Kirsten Hazler
#
#  Notes:

# ----------------------------------------------------------------------------------------

# Import required modules
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import os # provides access to operating system functionality such as file and directory paths
import sys # provides access to Python system functions
import traceback # used for error handling
import gc # garbage collection
from datetime import datetime # for time-stamping


# Script arguments to be input by user
inParcels = arcpy.GetParameterAsText(0)    #Input parcels layer
inLocalGDB = arcpy.GetParameterAsText(1)   #Input geodatabase containing the locality tables 
outGDB = arcpy.GetParameterAsText(2)       #GDB to store the output feature classes

arcpy.env.workspace = inLocalGDB
tables = arcpy.ListTables()

#Make a feature layer
arcpy.MakeFeatureLayer_management (inParcels, "lyrParcels")

for locTable in tables: 
   try: 
      #Set up some variables
      locName = os.path.basename(locTable)[4:]
      arcpy.AddMessage("Working on %s..." %locName)
      
      #Join the current table to the parcels layer
      arcpy.AddMessage("Joining attributes")
      arcpy.AddJoin_management ("lyrParcels", "VGIN_QPID", locTable, "VGIN_QPID", "KEEP_COMMON")
      
      #Copy the features to a new feature class
      arcpy.AddMessage("Copying features")
      arcpy.CopyFeatures_management("lyrParcels", outGDB + os.sep + locName)
      
      #Remove the current join
      arcpy.AddMessage("Removing join")
      arcpy.RemoveJoin_management("lyrParcels")
      
      arcpy.AddMessage("Completed %s" %locName)
   except:
      arcpy.AddWarning('Failed to process table %s.' % locTable)
      
      #Error Handling code swiped from "A Python Primer for ArcGIS"
      tb = sys.exc_info()[2]
      
      tbinfo = traceback.format_tb(tb)[0]
      pymsg = "Python Errors:\nTraceback Info:\n" + tbinfo + "\nError Info:\n" +str(sys.exc_info()[1])
      msgs = "ARCPY ERRORS:\n" + arcpy.GetMessages(2) + "\n"
      
      arcpy.AddWarning(msgs)
      arcpy.AddWarning(pymsg)
      arcpy.AddMessage(arcpy.GetMessages(1))





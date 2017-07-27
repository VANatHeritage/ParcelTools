# ----------------------------------------------------------------------------------------
# SubsetParcels.py
# Version:  Python 2.7.5
# Creation Date: 2017-06-21
# Last Edit: 2017-06-28
# Creator:  Roy Gilb and DJ Helkowski
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


for locTable in tables: 
	try: 
		#set up some variables
		locName = os.path.basename(locTable)[4:-9]
		arcpy.AddMessage(locName)
		
		#Join the current table to the parcels layer
		arcpy.AddJoin_management (inParcels, "VGIN_QPID", locTable, "VGIN_QPID", "KEEP_COMMON")
		
		#Copy the features to a new feature class
		arcpy.CopyFeatures_management(inParcels, outGDB + os.sep + locName)
		
		#Remove the current join
		arcpy.RemoveJoin_management(inParcels)
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



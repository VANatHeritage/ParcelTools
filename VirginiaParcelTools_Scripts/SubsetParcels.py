# ----------------------------------------------------------------------------------------
# SubsetParcels.py
# Version:  Python 3.x
# Creation Date: 2017-06-21
# Last Edit: 2023-11-09
# Creators:  Roy Gilb, DJ Helkowski, Kirsten Hazler, David Bucklin

# ----------------------------------------------------------------------------------------

# Import required modules
import arcpy
import os # provides access to operating system functionality such as file and directory paths
import time

def unique_values(table, field):
   ''' Gets list of unique values in a field.
   Thanks, ArcPy Cafe! https://arcpy.wordpress.com/2012/02/01/create-a-list-of-unique-field-values/'''
   with arcpy.da.SearchCursor(table, [field]) as cursor:
      return sorted({row[0] for row in cursor})

def getFlds(table):
   flds = [a.name for a in arcpy.ListFields(table)]
   return flds

arcpy.env.workspace = "in_memory"
arcpy.env.overwriteOutput = True

# headsup: For interactive use.
# base_dir = r"C:\David\proc"
# new_dir = base_dir + os.sep + "VA_Parcels_2023Q2"
# if not os.path.exists(new_dir):
#    os.makedirs(new_dir)
# new_gdb = new_dir + os.sep + 'VA_Parcels3.gdb'
# # 
# # Set paths to GDBs from VGIN
# va_parcels_gdb = r'C:\David\proc\Virginia_Parcel_Dataset_2023Q2.gdb'
# parcels = va_parcels_gdb + os.sep + "VA_parcels"
# va_tables_gdb = r'C:\David\proc\Virginia_Parcel_Dataset_LocalSchemas_2023Q2.gdb'

# Script arguments to be input by user
parcels = arcpy.GetParameterAsText(0)    #Input parcels layer
va_tables_gdb = arcpy.GetParameterAsText(1)   #Input geodatabase containing the locality tables 
new_gdb = arcpy.GetParameterAsText(2)       #GDB to store the output feature classes

# Make sure field names are correct
# getFlds(parcels)
# Set field name variables
locFld = "LOCALITY"
idFld = "VGIN_QPID"

# Create new GDB
if not arcpy.Exists(new_gdb):
   arcpy.AddMessage("Creating " + new_gdb + "...")
   arcpy.CreateFileGDB_management(os.path.dirname(new_gdb), os.path.basename(new_gdb))

# Get list of localities
loc_ls = unique_values(parcels, locFld)
arcpy.SetProgressor("step", "Creating parcel subsets by locality...", 0, len(loc_ls), 1)
n = 0

# Loop over localities
for l in loc_ls:
   # arcpy.AddMessage(l)
   # Headsup: not using error handling, so user can cancel process.
   arcpy.SetProgressorLabel("Processing " + l + "...")
   fc_out = new_gdb + os.sep + l.replace(" ", "_")
   nm = "TBL_" + l.replace(" ", "_")
   join_tab = va_tables_gdb + os.sep + nm
   if arcpy.Exists(fc_out):
      arcpy.AddMessage(l + " already exists.")
      continue
   t0 = time.time()
   lyr = arcpy.MakeFeatureLayer_management(parcels, where_clause=locFld + " = '" + l + "'")
   if not arcpy.Exists(join_tab):
      arcpy.AddMessage(join_tab + " does not exist.")
   else:
      arcpy.AddJoin_management(lyr, idFld, join_tab, idFld, "KEEP_ALL")
   arcpy.ExportFeatures_conversion(lyr, fc_out)
   t1 = time.time()
   arcpy.AddMessage("Completed processing for " + l + " in " + str(round(t1 - t0)) + " seconds.")
   n += 1
   arcpy.SetProgressorPosition(n)
arcpy.AddMessage("Compacting geodatabase...")
arcpy.Compact_management(new_gdb)
arcpy.AddMessage("Done.")

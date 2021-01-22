# Realtime-Sentinel1-Flood-Mapping
A Realtime Flood Mapping Approach ( Change Thresholding) Using Sentinel 1 Synthetic Aperture Radar Data with Open Source Python libraries.

# Objective 
This script will give the user access to process Sentinel 1 (Synthetic Aperture Radar) data to detect water areas after a disaster, especially a flood, typhoon, or storm.

# Functionality
This flood mapping approach gives the user a real-time flood (Water Area Detection) mapping using Sentinel 1 data based on threshold technique.
Open SAR Toolkit (OST), SNAP toolbox, WhiteboxTools, and Orfeo toolbox were used in this script.

Link to Open SAR Toolkit (OST)
https://github.com/ESA-PhiLab/OpenSarToolkit 

Link to WhiteboxTools
https://jblindsay.github.io/ghrg/WhiteboxTools/index.html

# Steps
1. Install anaconda
https://docs.anaconda.com/anaconda/install/



2. Install OST
You can find the installation instruction from this Link to Open SAR Toolkit (OST)
https://github.com/ESA-PhiLab/OpenSarToolkit 



3. Install SNAP
Install SNAP into the standard directory to OST to find the SNAP command-line executable. 



"""C:\Users\Chatumal\Anaconda3\Lib"""

Flood OST

for windows

    pip install glob2 DateTime GDAL numpy whitebox







functions

change
thresholding
maj_filtering
ras2poly


from pathlib
from pprint
Scheduler, rasterio

#Importing Flood Processing Module
from Flood_OST_S1 import Sentinel1Flood

# Methodology
<img src="https://github.com/chathumal93/Realtime-Sentinel1-Flood-Mapping/blob/master/Images/Method.png" width="400" height="400" />

# Output
The results will include the following;

* Processed pre-event and post-event tif files. (In Flood_Result Folder)
* Threshold and majority filtered tif files. 
* Detected Flood water shp file.

![](Images/Output_Structure.png)






![](Images/Flood_Result_QGIS.png)


























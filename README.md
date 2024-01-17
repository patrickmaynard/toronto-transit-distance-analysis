# Toronto transit distance analysis
A setup for ranking properties by distance to rail transit in Toronto

Based heavily on my previous project analyzing Berlin subway distances. See https://github.com/patrickmaynard/playing-with-qgis-python/blob/master/test-eight.py for the script I used in that project.

To make this script work, you will need the shapefiles from the following two URLs:

https://ckan0.cf.opendata.inter.prod-toronto.ca/ne/dataset/ttc-subway-shapefiles/resource/7c3b662a-1b42-4247-ba80-f1fd537e1c4a (rapid transit stations)

https://ckan0.cf.opendata.inter.prod-toronto.ca/ne/dataset/address-points-municipal-toronto-one-address-repository (points for property parcels)

EDIT: Another source for transit data if the link above goes dead is https://www.thetransportpolitic.com/transit-explorer/download/

Update the file paths in the Python script, along with the limit on the number of properties to analyze on the last line, which is set to an absurdly low number for testing. (If you set it to a million or so, you should be OK.) Then remove all existing layers from your project and paste that script into your QGIS Python editor, then run it. It will take some significant time, but it will run. Presto! You've got your ranking.

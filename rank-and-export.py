import math
import csv
from pathlib import Path

# This script ranks properties in Toronto by distance to the nearest rail transit station.
# It relies on shapefiles from the following sources:
# https://ckan0.cf.opendata.inter.prod-toronto.ca/ne/dataset/ttc-subway-shapefiles/resource/7c3b662a-1b42-4247-ba80-f1fd537e1c4a 
# https://ckan0.cf.opendata.inter.prod-toronto.ca/ne/dataset/address-points-municipal-toronto-one-address-repository

class Ranker(object): 
    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        km = 6367 * c
        return km

    @staticmethod
    def calculateDistance(featureProperty, layerStationEntrances):
        if featureProperty.geometry() is None:
            print("Null property geometry! Returning -1!")
            return -1
        shortestDistance = 1000
        featuresStationEntrances = layerStationEntrances.getFeatures()
        for featureStationEntrance in featuresStationEntrances:
            if featureStationEntrance.geometry() is None:
                print("Null station entrance geometry! Skipping!")
                continue
            latStationEntrance = featureStationEntrance.geometry().centroid().asPoint().y()
            lonStationEntrance = featureStationEntrance.geometry().centroid().asPoint().x()
            latProperty = featureProperty.geometry().centroid().asPoint().y()
            lonProperty = featureProperty.geometry().centroid().asPoint().x()
            currentDistance = Ranker.haversine(lonStationEntrance, latStationEntrance, lonProperty, latProperty)
            if currentDistance < shortestDistance:
                shortestDistance = currentDistance
        return shortestDistance

    @staticmethod
    def importAndAnalyze(rowLimit = 3):
        layerProperties = iface.addVectorLayer("/Users/patrickmaynard/Downloads/municipal-address-points-wgs84-latitude-longitude/ADDRESS_POINT_WGS84.shp", "Toronto_Addresses", "ogr")
        if not layerProperties:
            print("layerProperties failed to load!")
        layerStationEntrances = iface.addVectorLayer("/Users/patrickmaynard/Downloads/ttc-subway-shapefile-wgs84/TTC_SUBWAY_LINES_WGS84.shp", "Subway_Stations", "ogr")
        if not layerStationEntrances:
            print("layerStationEntrances failed to load!")
        features = layerProperties.getFeatures()
        counter = 0
        featuresSelected = []
        Path('/Users/patrickmaynard/Desktop/toronto-property-rankings.csv').touch()
        with open('/Users/patrickmaynard/Desktop/toronto-property-rankings.csv', 'a') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csvWriter.writerow(['ID', 'Lat','Lon', 'Distance'])
            for feature in features:
                if counter < rowLimit and feature.geometry().centroid() is not None:
                    try:
                        distance = Ranker.calculateDistance(feature, layerStationEntrances)
                        csvWriter.writerow([feature['ID'], feature.geometry().centroid().asPoint().y(),feature.geometry().centroid().asPoint().x(), distance])
                        if counter % 50 == 0:
                            csvFile.flush()
                    except ValueError:
                        print("Property could not be converted to point.")
                else:
                    break
                counter += 1
            csvFile.flush()

Ranker.importAndAnalyze(5)

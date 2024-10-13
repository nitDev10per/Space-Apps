Hello folks!

This download folder consists of the following files:

mtl.txt : Metadata file of the latest Landsat 8/9 imagery of the input location and the specified cloud cover

wrs2_extent.geojson : Vector file showing the extent of the WRS-2 tile corresponding to the Landsat image under which the specified location falls

Landsat_SR_band_values.csv : CSV file with Landsat band values for the pixel corresponding to the input location

output_image_wpsg4326.tif : Tif multiband Landsat 8/9 raster image with a 0.05 degree extent (north-south, east-west) from the specified location projected at standard EPSG:4326 Coordinate Reference System

clipped_3x3_polygon.geojson : Vector file showing the extent of the 3x3 pixels around the specified location

clipped_3x3_image.tif = Tif multiband Landsat 8/9 raster image with 3x3 pixels around the specified location. (This is output_image_wpsg4326.tif clipped by clipped_3x3_polygon.geojson layer)
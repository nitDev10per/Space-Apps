import pystac_client
import planetary_computer
import odc.stac
import matplotlib.pyplot as plt
from pystac.extensions.eo import EOExtension as eo
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from flask_cors import CORS
import json
import os

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

## INPUTS : coordinate, start_date, end_date, cloud_cover 
app = Flask(__name__)
CORS(app)

@app.route('/request/',methods=['POST','GET'])
def index():
    coordinates = json.loads(request.form['coordinates']);
    start_date = request.form.get('start_date');
    end_date = request.form.get('end_date');
    cloud_cover = json.loads(request.form['cloud_cover'])*100;
    
    print('Coordinates: ',coordinates)
    print('Cloud_cover request:',cloud_cover)
    print('Start date: ',start_date)
    print('Date type: ', type(start_date))
    print('CC type:',type(cloud_cover))
    
    def create_bounding_box(coordinates, width=0.05, height=0.05):
        lat, lon = coordinates
        
        # Calculate the bounding box
        # bbox = [
        #     lon - width / 2,  # Min longitude
        #     lat - height / 2,  # Min latitude
        #     lon + width / 2,  # Max longitude
        #     lat + height / 2   # Max latitude
        # ]
        bbox = [
            lon - width / 2,  # Min longitude
            lat - height / 2,  # Min latitude
            lon + width / 2,  # Max longitude
            lat + height / 2   # Max latitude
        ]
        return bbox

    # Define the coordinate
    #coordinates = [47.43405, -123.390455]  # [latitude, longitude]

    # Create the bounding box
    bounding_box = create_bounding_box(coordinates)
    print(bounding_box)

    bbox_of_interest = bounding_box # [-122.2751, 47.5469, -121.9613, 47.7458]
   # bbox_of_interest =[-122.2751, 47.5469, -121.9613, 47.7458]
    time_of_interest = f"{start_date}/{end_date}" #"2021-01-01/2023-12-31"

    search = catalog.search(
        collections=["landsat-c2-l2"],
        bbox=bbox_of_interest,
        datetime=time_of_interest,
        query={"eo:cloud_cover": {"lt": cloud_cover},
              "platform":{"eq":"landsat-8"}},
    )

    items = search.item_collection()
    if len(items)==0:
        print("No elements present within the given criteria")
        
    selected_item = max(items, key=lambda item: item.datetime) # Select item with maximum datetime

    print(
        f"Choosing {selected_item.id} from {selected_item.datetime.date()}"
        + f" with {selected_item.properties['eo:cloud_cover']}% cloud cover"
    )

    import requests
    # Download the file
    response = requests.get(selected_item.assets['mtl.xml'].href)
    
    # Define the relative path (e.g., "static/images/your_image.tiff")
    relative_path = "static/Metadata/"
    
    # Get the absolute path by joining Flask's root directory and the relative path
    absolute_path = os.path.join(app.root_path, relative_path)
    
    # Ensure the directory exists
    os.makedirs(absolute_path, exist_ok=True)
    
    file_name = 'mtl.xml'
    
    file_path = os.path.join(absolute_path, file_name)
    
    if response.status_code == 200:
        # Save the file locally
        output_path = file_path  # Specify your desired output path
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print("Metadata file saved")
    else:
        print('Error saving metadata file')
        
    polygon_coords = selected_item.geometry['coordinates']
    polygon_coords

    import geopandas as gpd
    from shapely.geometry import Polygon

    # Create the polygon
    polygon = Polygon(polygon_coords[0])  # Access the first (and only) set of coordinates

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame({'geometry': [polygon]})
    
    # Define the relative path (e.g., "static/images/your_image.tiff")
    relative_path = "static/Footprint/"
    
    # Get the absolute path by joining Flask's root directory and the relative path
    absolute_path = os.path.join(app.root_path, relative_path)
    
    # Ensure the directory exists
    os.makedirs(absolute_path, exist_ok=True)
    
    file_name = 'polygon.geojson'
    
    file_path = os.path.join(absolute_path, file_name)
    
    # Save the GeoDataFrame as a GeoJSON file
    gdf.to_file(file_path, driver='GeoJSON')

    print("Polygon saved as polygon.geojson.")

    ## Tiles url

    response = requests.get(selected_item.assets['tilejson'].href)

    decoded_response = response.content.decode('utf-8')

    response_dict = json.loads(decoded_response)
    tile_url = response_dict['tiles'][0] # For Tile layer of the Landsat scene

    ## Getting the image and downloading it 

    bands_of_interest = ["red", "green", "blue", "nir08", "lwir11", "swir16", "swir22"]

    data = odc.stac.stac_load(
        [selected_item], bands=bands_of_interest, bbox=bbox_of_interest
    ).isel(time=0)

    # xarray_data = data[["red", "green", "blue"]].to_array()
    xarray_data = data[bands_of_interest].to_array()

    import xarray as xr
    import rioxarray

    #xarray_data.rio.write_crs("EPSG:32610", inplace=True)
    
    # Define the relative path (e.g., "static/images/your_image.tiff")
    relative_path = "static/Image/"
    
    # Get the absolute path by joining Flask's root directory and the relative path
    absolute_path = os.path.join(app.root_path, relative_path)
    
    # Ensure the directory exists
    os.makedirs(absolute_path, exist_ok=True)
    
    file_name = 'output_image.tif'
    
    file_path = os.path.join(absolute_path, file_name)

    # Save the DataArray as a GeoTIFF
    xarray_data.rio.to_raster(file_path)
    print("Raster data saved")
    
    return "Works Well!"
    
app.run(port=7000)
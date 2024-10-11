-# Update: Our app is now deployed at : [Orbital Yatra](https://shark-app-rk86g.ondigitalocean.app/)@@

# **Landsat Reflectance Data: On the Fly and at Your Fingertips**

Our challenge was to create an easy to use web based application to obtain LANDSAT Surface Reflectance data for the selected location on the map, along with the Landsat pass dates and times over the region, metadata file for the scene, WRS-2 scene extent and the image with the 3X3 pixel grid.

## **Our App**
Our app was made using Python-Flask that sends requests to the Microsoft Planetary Computer STAC API for obtaining the image data for the selected region. 

To use the app follow these steps: 
1. **Clone the repository to your local system**: Checkout this link to understand how to clone a repository - [Cloning Git Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. **Download and install Python**: [Download Python](https://www.python.org/downloads/)
3. **Create and activate virtual environment**: Creating a virtual environment is recommended as it removes possibilities of conflicts between dependencies for python packages. Follow this link - [Creating and activating virtual environment](https://python.land/virtual-environments/virtualenv)
4. **Install the required python packages**: The required python packages can be installed using the requirements.txt file provided in the repo. Open terminal and navigate to the project directory containing the requirements.txt file and enter "pip install -r requirements.txt". Follow these steps for installing the required packages and more details - [Downloading packages with requirements.txt file](https://www.geeksforgeeks.org/how-to-install-python-packages-with-requirements-txt/)
5. **Run the app**: From the terminal, navigate to the project directory and enter "py app.py" or "python app.py" to start the app on your localhost. The app runs by default on port 7000. To use the app, go to - [Open the app on a browser](http://127.0.0.1:7000/request/)
6. **Mark the location of your choice on the map**: On opening the app, a map is loaded and you can mark the location of your interest by searching for the location using search bar or by navigating on the map, and clicking on the map.
7. **Select the cloud cover**: You can select the cloud cover threshold for the image using slider provided.
8. **Submit the request**: Click on the submit button to send the request. This does the following:
   -  Loads the pixel band values represented as a graph
   -  Loads the metadata for the latest Landsat scene available within the cloud cover threshold for the location and saves the metadata file as 'mtl.xml' under the [Metadata](static/Metadata/) folder under static folder of the project directory.
   -  Loads the table showing the upcoming Landsat-8/9 pass dates and time for the selected region.
   -  Downloads the Landsat-8/9 image for a small bounding box spanning (0.05 degrees north-south and 0.05 degrees east-west of the entered coordinates) and creates a 3X3 grid around the coordinates and saves it as "clipped_3x3_polygon.shp" shapefile and "clipped_3x3_image.tiff" raster image in the [Image](static/Image) folder of the repository.
   -  Downloads the WRS-2 tile extent for the location entered showing the footprint of the Landsat scene passing over the region, under the [Footprint](static/Footprint) folder under static folder of the project directory.

## **Our Team**
- **Shreyas Goswami** (shreyubhadrawati@gmail.com)
- **Akash Kumar** (akash_k@ce.iitr.ac.in)
- **Nitin Lodhi** (nitinyou039@gmail.com)
- **Amarjeet Kumar Mahato** (amarjeet_km@ce.iitr.ac.in)
   

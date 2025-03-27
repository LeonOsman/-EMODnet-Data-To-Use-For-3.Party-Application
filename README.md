# -EMODnet-Data-To-Use-For-3.Party-Application
Geospatial Data Visualization, ROI Selection, and Filtering Using EMODnet Data To Use For 3.Party Applications
The goal of this script is to visualize and analyze multiple geospatial datasets provided by EMODnet (European Marine Observation and Data Network), which includes submarine cables, wind farms, and coastline data. The user can interactively select a region of interest (ROI) using a rectangle, filter the data within that region, and save the filtered data as .shp format for further analysis on third party software such Python with GeoPandas,QGIS,ARCGIS enviroments. This report outlines the steps performed in the code and explains the logic behind each process.
Usable Areas of Output Files:
1.	QGIS (Quantum GIS) 
2.	ArcGIS (ArcMap or ArcGIS Pro) 
3.	Python with GeoPandas 
4.	PostGIS (Spatial Database Extension for PostgreSQL) 
5.	Google Earth Engine 
6.	MapInfo Pro 
7.	R with sf and ggplot2 
8.	CartoDB (Carto)
			EMODnet (European Marine Observation and Data Network).
Available at: https://www.emodnet.eu Accessed: March 2025. Description: EMODnet provides marine data services, including data on submarine cables, wind farms, bathymetry, and other marine environmental datasets.

Step-by-Step Breakdown
1.	Import Required Libraries: The code begins by importing several libraries:
•	geopandas: Used to handle geospatial data, load shapefiles, and perform spatial operations. 
•	contextily: A tool for adding basemaps to geospatial visualizations. 
•	matplotlib: A plotting library used to create the interactive map visualization. 
•	RectangleSelector: A widget from matplotlib.widgets used to allow users to select a region on the map interactively. 
2.	Loading EMODnet Data: Three different datasets from EMODnet are loaded:
•	Submarine Cables (gdf_1): This dataset is loaded from a File Geodatabase (GDB) containing submarine cable routes, provided by EMODnet's data services. 
•	Wind Farms (gdf_2): Another dataset from a different GDB file, containing the locations of offshore wind farms in Europe, available through EMODnet. 
•	Shapefile Data (gdf_3): This dataset contains coastline data in shapefile format (SHP), specifically for the Italian coastline, sourced from EMODnet Bathymetry. 
All three datasets are loaded using geopandas.read_file() and converted to the same coordinate reference system (CRS), ensuring consistency across all datasets for correct mapping. The CRS used is EPSG:4326, which corresponds to geographic coordinates (latitude and longitude).
3.	Creating the Plot: A map is created using matplotlib with the following layers:
•	Submarine cables are plotted in blue to represent the network of submarine telecommunication cables. 
•	Wind farms are plotted in red to indicate the locations of offshore wind energy infrastructure. 
•	Shapefile data (coastline) is plotted in green to provide context for the coastal region in the dataset. 
The data layers are overlaid on a basemap, which is retrieved using contextily and provides a background map for geographical reference. The basemap is based on imagery from Esri’s World Imagery provider.
4.	Interactive Region of Interest (ROI) Selection: The main feature of this script is the interactive selection of a region of interest (ROI) on the map using a rectangle. This is achieved using RectangleSelector, a tool from matplotlib.widgets.
•	The user can click and drag to create a rectangle on the map to define the ROI. 
•	When the user completes the rectangle selection, the coordinates of the selected area are captured. 
•	The selected ROI's extent is printed, and the plot is updated to zoom in on the defined region. 
•	
5.	Filtering Data Within the ROI: When the user presses the "Enter" key, the following steps occur:
•	The region selected with the RectangleSelector is stored in the roi_extent variable. 
•	The code filters the datasets (gdf_1, gdf_2, and gdf_3) using the .cx[] spatial indexing method to select only the data within the defined bounds. 
The filtered datasets are then:
•	Printed to the console, showing the number of features (e.g., wind farms, submarine cables, and coastline features) inside the selected ROI. 
•	The coordinates of the features in the selected ROI are printed to help with further analysis. 
6.	Saving Filtered Data: The filtered data within the ROI is saved to new shapefiles for later use. The columns of the GeoDataFrames are truncated to 10 characters to avoid any issues with column name length in shapefiles.
Result;
		Selected ROI: (np.float64(11.896630141051705), np.float64(37.68139705327789), 		np.float64(12.197542888495285), np.float64(38.07592843234775))
		ROI confirmed: (np.float64(11.896630141051705), np.float64(37.68139705327789), 		np.float64(12.197542888495285), np.float64(38.07592843234775))
		Number of wind farms within ROI: 1
		Number of submarine cables within ROI: 1
		Number of shapefile features within ROI: 7
The filtered data is saved as:
•	submarine_cables_roi.shp 
•	wind_farms_roi.shp 
•	shapefile_data_roi.shp 
7.	Plotting the Filtered Data: After filtering the data, the script checks if the filtered datasets contain any data. If data is found within the selected ROI:
•	A new map is created with the filtered datasets plotted. 
•	The map is overlaid with the same basemap, and the title reflects the number of features within the selected ROI. 
If no valid data is available in the selected ROI, a message is printed indicating this.
8.	Closing the Plot: After confirming the ROI selection, the plot is closed, and the final selected ROI is printed in the console for verification.
Key Features and Functionalities:
•	Interactive ROI Selection: Users can select a region on the map to zoom into and filter data, making the process dynamic and flexible. 
•	Multi-dataset Visualization: The code visualizes multiple datasets from EMODnet, such as submarine cables, wind farms, and coastline data, in a single map, allowing users to analyze spatial relationships between them. 
•	Filtered Data Export: After selecting the ROI, the script allows for the export of filtered data for further analysis. 
•	Basemap Integration: Contextily's basemap provides a geographical reference for better understanding of the data locations in relation to the world map. 
Conclusion
This script provides a robust tool for geospatial data analysis using EMODnet datasets. It allows users to explore and filter datasets on submarine cables, offshore wind farms, and coastline features in an interactive way. The ability to select specific regions of interest, visualize multiple datasets, and export the filtered data makes this tool valuable for various applications, including marine spatial planning, infrastructure development, environmental studies, and resource management. By leveraging EMODnet's rich datasets, users can gain better insights into the spatial distribution and relationships of different marine and coastal features.

For OPENCPN 
First the user need to download data from EMODnet, then using QGIS Free Graphical Interface software convert .shp file that is my study output file, to GPX file then just place the .gpx file in the correct directory and load it into OpenCPN.

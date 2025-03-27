import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import os
# Path to your first File Geodatabase (.gdb) directory
gdb_file_1 = '/home/PycharmProjects/PythonProject2/EMODnet_HA_Cables_Telecommunication_20230628/EMODnet_HA_Cables_Telecommunication_20230628.gdb'
layer_name_1 = 'FR_SIGCables_Submarine_Cables_Routes'  # Replace with the correct layer name
gdf_1 = gpd.read_file(gdb_file_1, layer=layer_name_1)

# Path to your second File Geodatabase (.gdb) directory
gdb_file_2 = '/home/PycharmProjects/PythonProject2/EMODnet_HA_Energy_WindFarms_20240508/EMODnet_HA_Energy_WindFarms_20240508.gdb'  # Update with your second GDB path
layer_name_2 = 'EMODnet_HA_Energy_WindFarms_pt_20240508'  # Replace with the correct layer name from the second file
gdf_2 = gpd.read_file(gdb_file_2, layer=layer_name_2)

# Load your shapefile data (gdf_3)
shapefile_dir = '/home/PycharmProjects/PythonProject2/EMODnet_Bathymetry_2024_coastlines'

# Assuming your shapefile has a .shp extension (e.g., file.shp)
shapefile_path = os.path.join(shapefile_dir, '/home/PycharmProjects/PythonProject2/EMODnet_Bathymetry_2024_coastlines/Europe_2024_satellite_coastline/Europe_2024_satellite_coastline_ITA.shx')
# Path to your shapefile (add the path to your shapefile here)
gdf_3 = gpd.read_file(shapefile_path)
gdf_3 = gdf_3.to_crs(epsg=4326)  # Ensure it uses the same CRS

# Ensure all GeoDataFrames are in the same CRS (EPSG:4326 in this case)
gdf_1 = gdf_1.to_crs(epsg=4326)
gdf_2 = gdf_2.to_crs(epsg=4326)

# Plot the data with a basemap
fig, ax = plt.subplots(figsize=(12, 12))  # Slightly larger figure size for clarity

# Plot the first layer (from the first GDB file)
gdf_1.plot(ax=ax, color='blue', alpha=0.7, linewidth=2, label='Submarine Cables')

# Plot the second layer (from the second GDB file)
gdf_2.plot(ax=ax, color='red', alpha=0.5, linewidth=2, label='Wind Farms')

# Plot the shapefile data (gdf_3)
gdf_3.plot(ax=ax, color='green', alpha=0.5, linewidth=2, label='Shapefile Data')

# Add basemap from contextily (use the correct provider)
ctx.add_basemap(ax, crs=gdf_1.crs.to_string(), source=ctx.providers.Esri.WorldImagery)

# Set axis labels
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)

# Set a title for clarity
ax.set_title('Submarine Cables, Wind Farms, and Shapefile Data', fontsize=16)

# Show gridlines for better reference
ax.grid(True, linestyle='--', alpha=0.5)

# Add legend to distinguish the layers
ax.legend()

# Define the function to handle the ROI selection
roi_extent = None  # Variable to store the selected ROI extent

def onselect(eclick, erelease):
    global roi_extent
    """This function is called when a rectangle is drawn."""
    # Get the coordinates of the rectangle
    roi_extent = (eclick.xdata, eclick.ydata, erelease.xdata, erelease.ydata)
    print(f"Selected ROI: {roi_extent}")

    # Update the plot with the selected rectangle
    ax.set_xlim([roi_extent[0], roi_extent[2]])
    ax.set_ylim([roi_extent[1], roi_extent[3]])

    # Redraw the plot
    plt.draw()

def toggle_selector(event):
    """This function is called when the Enter key is pressed."""
    if event.key == 'enter' and roi_extent is not None:
        print(f"ROI confirmed: {roi_extent}")
        # Optionally, remove the rectangle selector or perform other actions here
        rectangle_selector.set_active(False)
        plt.close()  # Close the plot after pressing Enter to confirm the ROI

        # Extract coordinates within the selected ROI
        xmin, ymin, xmax, ymax = roi_extent

        # Filter the submarine cables, wind farms, and shapefile data within the selected ROI
        gdf_1_roi = gdf_1.cx[xmin:xmax, ymin:ymax]  # Using the .cx indexer to filter by bounds
        gdf_2_roi = gdf_2.cx[xmin:xmax, ymin:ymax]
        gdf_3_roi = gdf_3.cx[xmin:xmax, ymin:ymax]

        # Debug: Check if the filtered ROI contains any wind farms
        print(f"\nNumber of wind farms within ROI: {len(gdf_2_roi)}")
        print(f"Number of submarine cables within ROI: {len(gdf_1_roi)}")
        print(f"Number of shapefile features within ROI: {len(gdf_3_roi)}")

        # Print the coordinates and other geographical data within the ROI
        print("\nSubmarine Cables within ROI:")
        for idx, row in gdf_1_roi.iterrows():
            geometry = row['geometry']
            if geometry.geom_type == 'LineString':
                coords = list(geometry.coords)
                print(f"OBJECTID: {row['OBJECTID']} | Coordinates: {coords}")
            else:
                print("Unknown geometry type.")

        print("\nWind Farms within ROI:")
        for idx, row in gdf_2_roi.iterrows():
            geometry = row['geometry']
            if geometry.geom_type == 'Point':
                coords = list(geometry.coords)
                print(f"NAME: {row['NAME']} | Coordinates: {coords}")
            elif geometry.geom_type == 'MultiPoint':
                for geom in geometry.geoms:
                    coords = list(geom.coords)
                    print(f"NAME: {row['NAME']} | Coordinates: {coords}")
            else:
                print("Unknown geometry type.")

        print("\nShapefile Data within ROI:")
        for idx, row in gdf_3_roi.iterrows():
            geometry = row['geometry']
            if geometry.geom_type == 'LineString':
                coords = list(geometry.coords)
                print(f"Shapefile LineString Coordinates: {coords}")
            else:
                print("Unknown geometry type.")

        # Optionally save filtered data to files
        gdf_1_roi.columns = [col[:10] for col in gdf_1_roi.columns]  # Truncate column names to 10 characters
        gdf_2_roi.columns = [col[:10] for col in gdf_2_roi.columns]  # Truncate column names to 10 characters
        gdf_3_roi.columns = [col[:10] for col in gdf_3_roi.columns]  # Truncate column names to 10 characters

        gdf_1_roi.to_file('submarine_cables_roi.shp')
        gdf_2_roi.to_file('wind_farms_roi.shp')
        gdf_3_roi.to_file('shapefile_data_roi.shp')

        # Plot the filtered data
        if not gdf_1_roi.empty and not gdf_2_roi.empty and not gdf_3_roi.empty:  # Check if GeoDataFrames are not empty
            fig, ax = plt.subplots(figsize=(12, 12))
            gdf_1_roi.plot(ax=ax, color='blue', alpha=0.7, label='Submarine Cables')
            gdf_2_roi.plot(ax=ax, color='red', alpha=0.5, label='Wind Farms')
            gdf_3_roi.plot(ax=ax, color='green', alpha=0.5, label='Shapefile Data')
            ctx.add_basemap(ax, crs=gdf_1_roi.crs.to_string(), source=ctx.providers.Esri.WorldImagery)
            ax.set_title(f'Submarine Cables, Wind Farms, and Shapefile Data within ROI\n'
                         f'({len(gdf_1_roi)} cables, {len(gdf_2_roi)} wind farms, {len(gdf_3_roi)} features)',
                         fontsize=16)
            ax.legend()
            plt.show()
        else:
            print("No valid data to plot in the selected ROI.")


# Create a RectangleSelector widget for drawing the rectangle
rectangle_selector = RectangleSelector(ax, onselect, useblit=True, button=[1], minspanx=0.01, minspany=0.01)

# Connect the event for pressing Enter to toggle the selection
fig.canvas.mpl_connect('key_press_event', toggle_selector)

# Show the plot with the interactive navigation toolbar enabled
plt.show()

# After the plot is closed, print the selected ROI
if roi_extent:
    print(f"Final selected ROI: {roi_extent}")
else:
    print("No ROI selected.")

import pandas as pd  # For data manipulation and preprocessing
import matplotlib.pyplot as plt  # For visualizing data with bar charts and plots
import geopandas as gpd
from shapely.geometry import Point

file_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\BikeSharingData_Berlin_combinedandcleaned.pkl"

#dataset
try:
    data = pd.read_pickle(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# We’ll use random sampling to ensure all time periods are proportionally represented
#subset the data with 50,000 rows
subset_data = data.sample(n=50000, random_state=42)
print(f"Subset contains {len(subset_data)} rows.")

shapefile_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\berlin_postleitzahlen\berlin_postleitzahlen.shp"
berlin_postcodes = gpd.read_file(shapefile_path)

#GeoDataFrames for start and end points
subset_data['start_geometry'] = subset_data.apply(lambda row: Point(row['long_origin'], row['lat_origin']), axis=1)
subset_data['end_geometry'] = subset_data.apply(lambda row: Point(row['long_destination'], row['lat_destination']), axis=1)

start_gdf = gpd.GeoDataFrame(subset_data, geometry='start_geometry', crs=berlin_postcodes.crs)
end_gdf = gpd.GeoDataFrame(subset_data, geometry='end_geometry', crs=berlin_postcodes.crs)

#join to map trips to postcodes
start_joined = gpd.sjoin(start_gdf, berlin_postcodes, how='left', predicate='intersects')
end_joined = gpd.sjoin(end_gdf, berlin_postcodes, how='left', predicate='intersects')

#aggregate trip counts by postcode for start and end points
start_counts = start_joined.groupby('PLZ99').size().reset_index(name='start_count')
end_counts = end_joined.groupby('PLZ99').size().reset_index(name='end_count')

#merge start and end counts
berlin_postcodes = berlin_postcodes.merge(start_counts, on='PLZ99', how='left').merge(end_counts, on='PLZ99', how='left')
berlin_postcodes['start_count'] = berlin_postcodes['start_count'].fillna(0)
berlin_postcodes['end_count'] = berlin_postcodes['end_count'].fillna(0)

#visualize bike trips for start points
start_map = berlin_postcodes.explore(
    column='start_count',       # Column to color the map
    cmap="YlOrRd",                # Choose a color gradient
    legend=True,                # Show a legend
    tooltip=['PLZ99', 'start_count'],  # Show postcode and start count on hover
    style_kwds={"fillOpacity": 0.6}  # Add boundary styling
)
start_map.save("../results/bike_trips_start_by_postcode.html")
print("Map saved as 'bike_trips_start_by_postcode.html'")

#visualize bike trips for end points
end_map = berlin_postcodes.explore(
    column='end_count',         # Column to color the map
    cmap="YlOrRd",              # Choose a color gradient
    legend=True,                # Show a legend
    tooltip=['PLZ99', 'end_count'],  # Show postcode and end count on hover
    style_kwds={"fillOpacity": 0.6}  # Add boundary styling
)
end_map.save("../results/bike_trips_end_by_postcode.html")
print("Map saved as 'bike_trips_end_by_postcode.html'")

#static plot for start points
berlin_postcodes.plot(
    column='start_count',
    cmap='YlOrRd',
    legend=True,
    legend_kwds={'label': "Bike Trips (Start Points)"},
    edgecolor='black',
    figsize=(12, 8)
)
plt.title("Bike Trips by Postcode (Start Points)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("../results/bike_trips_start_static.png", dpi=300, bbox_inches='tight')
plt.show()

#static plot for end points
berlin_postcodes.plot(
    column='end_count',
    cmap='YlOrRd',
    legend=True,
    legend_kwds={'label': "Bike Trips (End Points)"},
    edgecolor='black',
    figsize=(12, 8)
)
plt.title("Bike Trips by Postcode (End Points)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("../results/bike_trips_end_static.png", dpi=300, bbox_inches='tight')
plt.show()
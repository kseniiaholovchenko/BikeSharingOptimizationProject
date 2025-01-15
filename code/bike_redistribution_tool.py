#================================================================================================================================================
#The purpose of the Bike Redistribution Tool is to identify areas with an excess of bikes (high numbers of drop-offs)
#and areas with a deficit of bikes (high numbers of pickups). This can help bike-sharing operators optimize bike distribution across the city.
#================================================================================================================================================

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

file_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\BikeSharingData_Berlin_combinedandcleaned.pkl"
shapefile_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\berlin_postleitzahlen\berlin_postleitzahlen.shp"

#data
try:
    data = pd.read_pickle(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

#subset the data with 50,000 rows for analysis
subset_data = data.sample(n=50000, random_state=42)

#Berlin postcodes shapefile
try:
    berlin_postcodes = gpd.read_file(shapefile_path)
    print("Shapefile loaded successfully!")
except Exception as e:
    print(f"Error loading shapefile: {e}")
    exit()

#GeoDataFrames for start and end points
subset_data['start_geometry'] = subset_data.apply(lambda row: Point(row['long_origin'], row['lat_origin']), axis=1)
subset_data['end_geometry'] = subset_data.apply(lambda row: Point(row['long_destination'], row['lat_destination']), axis=1)

start_gdf = gpd.GeoDataFrame(subset_data, geometry='start_geometry', crs=berlin_postcodes.crs)
end_gdf = gpd.GeoDataFrame(subset_data, geometry='end_geometry', crs=berlin_postcodes.crs)

#spatial join to map trips to postcodes
start_joined = gpd.sjoin(start_gdf, berlin_postcodes, how='inner', predicate='intersects')
end_joined = gpd.sjoin(end_gdf, berlin_postcodes, how='inner', predicate='intersects')

#trip counts by postcode
start_counts = start_joined.groupby('PLZ99').size().reset_index(name='start_count')
end_counts = end_joined.groupby('PLZ99').size().reset_index(name='end_count')

#merge start and end counts
bike_imbalance = start_counts.merge(end_counts, on='PLZ99', how='outer').fillna(0)
bike_imbalance['imbalance'] = bike_imbalance['end_count'] - bike_imbalance['start_count']

#merge imbalance data with Berlin postcodes for mapping
berlin_postcodes = berlin_postcodes.merge(bike_imbalance, on='PLZ99', how='left').fillna(0)

#visualize areas with excess and deficit of bikes
berlin_postcodes.plot(
    column='imbalance',
    cmap='RdYlGn',
    legend=True,
    legend_kwds={'label': "Bike Redistribution Imbalance. Red: Areas with a deficit. Green: Areas with an excess."},
    edgecolor='black',
    figsize=(12, 8)
)
plt.title("Bike Redistribution Map")
plt.savefig("../results/bike_redistribution_map.png")
plt.show()

#the redistribution insights
# bike_imbalance.to_csv("bike_imbalance_summary.csv", index=False)
# print("Bike redistribution insights saved to 'bike_imbalance_summary.csv'.")

#Heatmap with explore()
#Red: Areas with a deficit (negative imbalance) (high numbers of pickups).
#Green: Areas with an excess (positive imbalance) (high numbers of drop-offs).
imbalance_map = berlin_postcodes.explore(
    column='imbalance',       # Column to visualize
    cmap='RdYlGn',            # Color map: Red for deficits, Green for excess
    legend=True,              # Show a legend
    legend_kwds={'caption': "Bike Redistribution Imbalance. Red: Areas with a deficit. Green: Areas with an excess."},
    tooltip=['PLZ99', 'imbalance'],  # Tooltip with postcode and imbalance
    style_kwds={'fillOpacity': 0.7}, # Adjust transparency
)

imbalance_map.save("../results/bike_redistribution_heatmap.html")
print("Bike Redistribution Heatmap saved as 'bike_redistribution_heatmap.html'")


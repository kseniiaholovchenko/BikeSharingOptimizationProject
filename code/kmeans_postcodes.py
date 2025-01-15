import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import geopandas as gpd
from shapely.geometry import Point

#Dataset and shapefile
file_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\BikeSharingData_Berlin_combinedandcleaned.pkl"
shapefile_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\berlin_postleitzahlen\berlin_postleitzahlen.shp"

#Dataset
try:
    data = pd.read_pickle(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

#Subset the data for clustering
subset_data = data.sample(n=35000, random_state=42)
print(f"Subset contains {len(subset_data)} rows.")

#convert trip start times into a readable format
subset_data['time_origin'] = pd.to_datetime(subset_data['time_origin'], unit='s')
subset_data['hour'] = subset_data['time_origin'].dt.hour
subset_data['day_of_week'] = subset_data['time_origin'].dt.dayofweek

#remove outliers using IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

#Remove outliers for latitude and longitude
print("Removing outliers for latitude and longitude...")
filtered_data = remove_outliers(subset_data, 'lat_origin')
filtered_data = remove_outliers(filtered_data, 'long_origin')

print(f"Filtered data contains {len(filtered_data)} rows after outlier removal.")

#Berlin postcode shapefile
print("\nLoading Berlin postcodes shapefile...")
berlin_postcodes = gpd.read_file(shapefile_path)

#KMeans clustering and aggregate bike trip counts
def kmeans_heatmap_with_usage(data, postcodes, time_filter=None, n_clusters=20, time_label="All_Time"):
    if time_filter is not None:
        data = data[time_filter]
        print(f"Filtered data contains {len(data)} rows for {time_label}.")

    #extract latitude and longitude for clustering
    coordinates = data[['lat_origin', 'long_origin']].dropna()

    #normalize the data
    scaler = StandardScaler()
    normalized_coords = scaler.fit_transform(coordinates)

    #KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(normalized_coords)
    coordinates['cluster'] = kmeans.labels_

    #add cluster labels to the original data
    data = data.join(coordinates['cluster'], how='inner')

    #aggregate bike trip counts by cluster
    cluster_usage = data.groupby('cluster').size().reset_index(name='trip_count')

    #convert cluster data to GeoDataFrame
    data['geometry'] = data.apply(lambda row: Point(row['long_origin'], row['lat_origin']), axis=1)
    clustered_gdf = gpd.GeoDataFrame(data, geometry='geometry')

    #merge trip counts into the clustered GeoDataFrame
    clustered_gdf = clustered_gdf.merge(cluster_usage, on='cluster', how='left')

    #drop non-serializable columns
    clustered_gdf = clustered_gdf.drop(columns=['time_origin'], errors='ignore')

    #heatmap with clusters by bike usage
    heatmap = clustered_gdf.explore(
        column='trip_count', cmap='YlOrRd', tooltip=['cluster', 'trip_count'], legend=True,
        tiles="OpenStreetMap",
    )

    #postcode boundaries
    postcodes.explore(
        tiles=None,
        style_kwds={"fillOpacity": 0, "color": "black", "weight": 1},
        m=heatmap,
    )
    heatmap.save(f"../results/kmeans_heatmap_with_usage_{time_label}.html")

    print(f"Heatmap saved as kmeans_heatmap_with_usage_{time_label}.html")

    #static plot for clusters with bike usage
    fig, ax = plt.subplots(figsize=(12, 10))
    postcodes.boundary.plot(ax=ax, color='black', linewidth=0.5, label='Postcode Boundaries')
    clustered_gdf.plot(ax=ax, column='trip_count', cmap='YlOrRd', markersize=10, alpha=0.7, legend=True)
    plt.title(f"KMeans Clustering with Bike Usage ({time_label})")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.savefig(f"../results/kmeans_clusters_with_usage_{time_label}.png")
    plt.show()

    return data


#High-Demand Zones for All Time with bike usage
print("\nAnalyzing high-demand zones for all time with bike usage...")
all_time_data_with_usage = kmeans_heatmap_with_usage(filtered_data, berlin_postcodes, n_clusters=20)

# Morning (6 AM to 10 AM)
print("\nAnalyzing high-demand zones for morning (6 AM to 10 AM) with bike usage...")
morning_filter = (filtered_data['hour'] >= 6) & (filtered_data['hour'] < 10)
morning_data_with_usage = kmeans_heatmap_with_usage(filtered_data, berlin_postcodes, time_filter=morning_filter, time_label="Morning")

# Evening (4 PM to 8 PM)
print("\nAnalyzing high-demand zones for evening (4 PM to 8 PM) with bike usage...")
evening_filter = (filtered_data['hour'] >= 16) & (filtered_data['hour'] < 20)
evening_data_with_usage = kmeans_heatmap_with_usage(filtered_data, berlin_postcodes, time_filter=evening_filter, time_label="Evening")

# Weekends
print("\nAnalyzing high-demand zones for weekends (Saturday and Sunday) with bike usage...")
weekend_filter = filtered_data['day_of_week'].isin([5, 6])
weekend_data_with_usage = kmeans_heatmap_with_usage(filtered_data, berlin_postcodes, time_filter=weekend_filter, time_label="Weekends")

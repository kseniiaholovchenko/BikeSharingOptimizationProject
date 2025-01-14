import pandas as pd  # For data manipulation and preprocessing
import matplotlib.pyplot as plt  # For visualizing data with bar charts and plots
import geopandas as gpd
from shapely.geometry import Point

# Path to your dataset (replace with your actual file path)
file_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\BikeSharingData_Berlin_combinedandcleaned.pkl"

# Step 1: Load the dataset
try:
    data = pd.read_pickle(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# We’ll use random sampling to ensure all time periods are proportionally represented
# Step 2: Subset the data with 50,000 rows
subset_data = data.sample(n=50000, random_state=42)
print(f"Subset contains {len(subset_data)} rows.")

#====================================
# Convert duration from seconds to minutes
subset_data['duration_minutes'] = subset_data['duration_osrm'] / 60

# Summary statistics for trip duration and distance
# pandas’ .describe() to calculate key statistics (mean, median, min, max, etc.)
trip_stats = subset_data[['duration_minutes', 'distance_osrm']].describe()
print("Summary Statistics:")
print(trip_stats)

# Plot histograms for raw data
plt.figure(figsize=(12, 5))
# Duration histogram
plt.subplot(1, 2, 1)
plt.hist(subset_data['duration_minutes'], bins=50, color='cornflowerblue', alpha=0.7)
plt.title("Trip Duration Distribution (Unfiltered Data)")
plt.xlabel("Duration (minutes)")
plt.ylabel("Frequency")
# Distance histogram
plt.subplot(1, 2, 2)
plt.hist(subset_data['distance_osrm'], bins=50, color='#66cc66', alpha=0.7)
plt.title("Trip Distance Distribution (Unfiltered Data)")
plt.xlabel("Distance (meters)")
plt.ylabel("Frequency")
plt.savefig("../results/histogram_trip_duration_distance.png")
plt.tight_layout()
plt.show()


# Detect outliers using the Interquartile Range (IQR) method
# Calculate IQR for duration
Q1_duration = subset_data['duration_minutes'].quantile(0.25)
Q3_duration = subset_data['duration_minutes'].quantile(0.75)
IQR_duration = Q3_duration - Q1_duration
# Calculate IQR for distance
Q1_distance = subset_data['distance_osrm'].quantile(0.25)
Q3_distance = subset_data['distance_osrm'].quantile(0.75)
IQR_distance = Q3_distance - Q1_distance
# Apply a combined filter for both duration and distance
filtered_data = subset_data[
    (subset_data['duration_minutes'] >= Q1_duration - 1.5 * IQR_duration) &
    (subset_data['duration_minutes'] <= Q3_duration + 1.5 * IQR_duration) &
    (subset_data['distance_osrm'] >= Q1_distance - 1.5 * IQR_distance) &
    (subset_data['distance_osrm'] <= Q3_distance + 1.5 * IQR_distance)
]
# Print the number of filtered rows
print(f"Filtered data contains {len(filtered_data)} trips")


# Compute means and medians for both filtered and unfiltered data
# Means and medians (original data)
mean_duration = subset_data['duration_minutes'].mean()
median_duration = subset_data['duration_minutes'].median()
mean_distance = subset_data['distance_osrm'].mean()
median_distance = subset_data['distance_osrm'].median()
print(f"Mean Trip Duration: {mean_duration:.2f} minutes")
print(f"Median Trip Duration: {median_duration:.2f} minutes")
print(f"Mean Trip Distance: {mean_distance:.2f} meters")
print(f"Median Trip Distance: {median_distance:.2f} meters")

# Plot histograms for filtered data
plt.figure(figsize=(12, 5))
# Duration histogram (filtered data)
plt.subplot(1, 2, 1)
plt.hist(filtered_data['duration_minutes'], bins=50, color='cornflowerblue', alpha=0.7)
plt.title("Trip Duration Distribution (Filtered Data)")
plt.xlabel("Duration (minutes)")
plt.ylabel("Frequency")
# Distance histogram (filtered data)
plt.subplot(1, 2, 2)
plt.hist(filtered_data['distance_osrm'], bins=50, color='#66cc66', alpha=0.7)
plt.title("Trip Distance Distribution (Filtered Data)")
plt.xlabel("Distance (meters)")
plt.ylabel("Frequency")
plt.savefig("../results/filtered_histogram_trip_duration_distance.png")
plt.tight_layout()
plt.show()

# Means and medians (filtered data)
mean_duration_filtered = filtered_data['duration_minutes'].mean()
median_duration_filtered = filtered_data['duration_minutes'].median()
mean_distance_filtered = filtered_data['distance_osrm'].mean()
median_distance_filtered = filtered_data['distance_osrm'].median()
print(f"Filtered Mean Trip Duration: {mean_duration_filtered:.2f} minutes")
print(f"Filtered Median Trip Duration: {median_duration_filtered:.2f} minutes")
print(f"Filtered Mean Trip Distance: {mean_distance_filtered:.2f} meters")
print(f"Filtered Median Trip Distance: {median_distance_filtered:.2f} meters")

# Boxplots to detect and visualize outliers (Unfiltered Data)
plt.figure(figsize=(12, 5))
# Duration boxplot
plt.subplot(1, 2, 1)
plt.boxplot(subset_data['duration_minutes'], vert=False, patch_artist=True, boxprops=dict(facecolor='cornflowerblue'))
plt.title("Trip Duration Boxplot (Unfiltered Data)")
plt.xlabel("Duration (minutes)")
# Distance boxplot
plt.subplot(1, 2, 2)
plt.boxplot(subset_data['distance_osrm'], vert=False, patch_artist=True, boxprops=dict(facecolor='#66cc66'))
plt.title("Trip Distance Boxplot (Unfiltered Data)")
plt.xlabel("Distance (meters)")
plt.savefig("../results/boxplot_unfiltered_trip_duration_distance.png")
plt.tight_layout()
plt.show()

# Boxplots to detect and visualize outliers (Filtered Data)
plt.figure(figsize=(12, 5))
# Duration boxplot
plt.subplot(1, 2, 1)
plt.boxplot(filtered_data['duration_minutes'], vert=False, patch_artist=True, boxprops=dict(facecolor='cornflowerblue'))
plt.title("Trip Duration Boxplot (Filtered Data)")
plt.xlabel("Duration (minutes)")
# Distance boxplot
plt.subplot(1, 2, 2)
plt.boxplot(filtered_data['distance_osrm'], vert=False, patch_artist=True, boxprops=dict(facecolor='#66cc66'))
plt.title("Trip Distance Boxplot (Filtered Data)")
plt.xlabel("Distance (meters)")
plt.savefig("../results/boxplot_filtered_trip_distance.png")
plt.tight_layout()
plt.show()


# Relationship between trip duration and trip distance
# Scatter plot for trip duration vs. trip distance for Unfiltered Data
plt.figure(figsize=(8, 6))
plt.scatter(subset_data['distance_osrm'], subset_data['duration_minutes'], alpha=0.5, color='cornflowerblue')
plt.title("Trip Duration vs. Distance (Unfiltered Data)")
plt.xlabel("Distance (meters)")
plt.ylabel("Duration (minutes)")
plt.grid(alpha=0.3)
plt.savefig("../results/scatter_duration_vs_distance_unfiltered.png")
plt.show()

# Scatter plot for trip duration vs. trip distance for Filtered Data
plt.figure(figsize=(8, 6))
plt.scatter(filtered_data['distance_osrm'], filtered_data['duration_minutes'], alpha=0.5, color='#66cc66')
plt.title("Trip Duration vs. Distance (Filtered Data)")
plt.xlabel("Distance (meters)")
plt.ylabel("Duration (minutes)")
plt.grid(alpha=0.3)
plt.savefig("../results/scatter_duration_vs_distance_filtered.png")
plt.show()

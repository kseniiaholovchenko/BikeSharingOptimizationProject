import pandas as pd  # For data manipulation and preprocessing
import matplotlib.pyplot as plt  # For visualizing data with scatter plots and correlations
import seaborn as sns  # For creating heatmaps and advanced visualizations

# Path to your dataset (replace with your actual file path)
file_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\BikeSharingData_Berlin_combinedandcleaned.pkl"

# Step 1: Load the dataset
try:
    data = pd.read_pickle(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

#====================================
# Step 2: Subset the data for analysis
# Use a random sample of 50,000 rows to ensure efficient processing
subset_data = data.sample(n=50000, random_state=42)
print(f"Subset contains {len(subset_data)} rows.")

# Convert duration from seconds to minutes
subset_data['duration_minutes'] = subset_data['duration_osrm'] / 60

#====================================
# Step 3: Explore Correlations
# Select relevant columns for correlation analysis
relevant_columns = ['speed_osrm', 'speed_kmh', 'duration_minutes', 'distance_osrm']
correlation_matrix = subset_data[relevant_columns].corr()
print("Correlation Matrix:")
print(correlation_matrix)

# Plot a heatmap to visualize correlations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix: Speed, Duration, and Distance")
plt.savefig("../results/correlation_matrix_speed_duration_distance.png")
plt.show()

#====================================
# Step 4: Scatter Plots for Relationships
# Scatter plot: Speed (OSRM) vs Duration
plt.figure(figsize=(8, 6))
plt.scatter(subset_data['speed_osrm'], subset_data['duration_minutes'], alpha=0.5, color='cornflowerblue')
plt.title("Speed (OSRM) vs Duration")
plt.xlabel("Speed (m/s)")
plt.ylabel("Duration (minutes)")
plt.grid(alpha=0.3)
plt.savefig("../results/scatter_speed_osrm_vs_duration.png")
plt.show()

# Scatter plot: Speed (km/h) vs Duration
plt.figure(figsize=(8, 6))
plt.scatter(subset_data['speed_kmh'], subset_data['duration_minutes'], alpha=0.5, color='#66cc66')
plt.title("Speed (km/h) vs Duration")
plt.xlabel("Speed (km/h)")
plt.ylabel("Duration (minutes)")
plt.grid(alpha=0.3)
plt.savefig("../results/scatter_speed_kmh_vs_duration.png")
plt.show()

# Scatter plot: Speed (OSRM) vs Distance
plt.figure(figsize=(8, 6))
plt.scatter(subset_data['speed_osrm'], subset_data['distance_osrm'], alpha=0.5, color='pink')
plt.title("Speed (OSRM) vs Distance")
plt.xlabel("Speed (m/s)")
plt.ylabel("Distance (meters)")
plt.grid(alpha=0.3)
plt.savefig("../results/scatter_speed_osrm_vs_distance.png")
plt.show()

# Scatter plot: Speed (km/h) vs Distance
plt.figure(figsize=(8, 6))
plt.scatter(subset_data['speed_kmh'], subset_data['distance_osrm'], alpha=0.5, color='purple')
plt.title("Speed (km/h) vs Distance")
plt.xlabel("Speed (km/h)")
plt.ylabel("Distance (meters)")
plt.grid(alpha=0.3)
plt.savefig("../results/scatter_speed_kmh_vs_distance.png")
plt.show()


#====================================
# Step 5: Analyze Speed Ranges
# Histograms for speed_osrm and speed_kmh
plt.figure(figsize=(12, 5))

# Speed (OSRM) histogram
plt.subplot(1, 2, 1)
plt.hist(subset_data['speed_osrm'], bins=50, color='cornflowerblue', alpha=0.7)
plt.title("Speed Distribution (OSRM)")
plt.xlabel("Speed (m/s)")
plt.ylabel("Frequency")
# Speed (km/h) histogram
plt.subplot(1, 2, 2)
plt.hist(subset_data['speed_kmh'], bins=50, color='#66cc66', alpha=0.7)
plt.title("Speed Distribution (km/h)")
plt.xlabel("Speed (km/h)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("../results/histograms_speed_distributions.png")
plt.show()

#====================================
# Step 6: Summarize Findings
# Calculate mean and median speeds
mean_speed_osrm = subset_data['speed_osrm'].mean()
median_speed_osrm = subset_data['speed_osrm'].median()
mean_speed_kmh = subset_data['speed_kmh'].mean()
median_speed_kmh = subset_data['speed_kmh'].median()
print(f"Mean Speed (OSRM): {mean_speed_osrm:.2f} m/s")
print(f"Median Speed (OSRM): {median_speed_osrm:.2f} m/s")
print(f"Mean Speed (km/h): {mean_speed_kmh:.2f} km/h")
print(f"Median Speed (km/h): {median_speed_kmh:.2f} km/h")
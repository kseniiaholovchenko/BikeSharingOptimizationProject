import pandas as pd  # For data manipulation and preprocessing
import matplotlib.pyplot as plt  # For visualizing data with bar charts and plots

file_path = r"C:\Users\Kseniia\Desktop\universities\BHT\Urban Technology\BikeSharingProject\data\BikeSharingData_Berlin_combinedandcleaned.pkl"

# dataset
try:
    data = pd.read_pickle(file_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

#We’ll use random sampling to ensure all time periods are proportionally represented
#Subset the data with 50,000 rows
subset_data = data.sample(n=50000, random_state=42)
print(f"Subset contains {len(subset_data)} rows.")

#extract time features
#convert UNIX timestamp to datetime
subset_data['time_origin'] = pd.to_datetime(subset_data['time_origin'], unit='s')

#extract hour, day of the week, and month
subset_data['hour'] = subset_data['time_origin'].dt.hour
subset_data['day_of_week'] = subset_data['time_origin'].dt.dayofweek  # 0 = Monday, 6 = Sunday
subset_data['month'] = subset_data['time_origin'].dt.month

#Plot hourly demand
hourly_demand = subset_data['hour'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
bars = plt.bar(hourly_demand.index, hourly_demand.values, color='cornflowerblue', alpha=0.7)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 50, f"{int(height)}",
             ha='center', va='bottom', fontsize=8, color='black')
plt.title("Bike Trips by Hour")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Trips")
plt.xticks(range(0, 24))  # Ensure all hours are displayed
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("../results/hourly_demand_plot.png", dpi=300, bbox_inches='tight')
plt.show()
print("Plot hourly demand")

#Plot daily demand (day of the week)
weekly_demand = subset_data['day_of_week'].value_counts().sort_index()
plt.figure(figsize=(8, 5))
bars = plt.bar(weekly_demand.index, weekly_demand.values, color='#66cc66', alpha=0.7)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 50, f"{int(height)}",
             ha='center', va='bottom', fontsize=8, color='black')
plt.title("Bike Trips by Day of the Week")
plt.xlabel("Day of the Week (0 = Monday, 6 = Sunday)")
plt.ylabel("Number of Trips")
plt.xticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("../results/daily_demand_plot.png", dpi=300, bbox_inches='tight')
plt.show()
print("Plot daily demand")

#Plot monthly demand
monthly_demand = subset_data['month'].value_counts().reindex(range(1, 13), fill_value=0)
plt.figure(figsize=(8, 5))
bars = plt.bar(monthly_demand.index, monthly_demand.values, color='pink', alpha=0.7)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 150, f"{int(height)}",
             ha='center', va='bottom', fontsize=8, color='black')
for month in [1, 2, 3]:  # January, February, March
    plt.text(month, 800, "No Data", ha='center', color='black', fontsize=10, rotation=90)
plt.title("Bike Trips by Month")
plt.xlabel("Month")
plt.ylabel("Number of Trips")
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("../results/monthly_demand_plot.png", dpi=300, bbox_inches='tight')
plt.show()
print("Plot monthly demand")

print("Demand visualization completed!")


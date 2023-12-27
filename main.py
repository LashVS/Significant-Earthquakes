import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'Earthquakes_database - Earthquakes_database.csv'
earthquake_data = pd.read_csv(file_path)

# TASK 1

# this will create new columns 'Year', 'Month', and 'Day' from the 'Date' column
earthquake_data[['Year', 'Month', 'Day']] = earthquake_data['Date'].str.split('/', expand=True)

# this will create new columns 'Hour', 'Minute', and 'Second' from the 'Time' column
earthquake_data[['Hour', 'Minute', 'Second']] = earthquake_data['Time'].str.split(':', expand=True)

# ensures these new columns are in a numeric format for easier analysis
for col in ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']:
    earthquake_data[col] = pd.to_numeric(earthquake_data[col], errors='coerce')

# removes columns where more than half of the data is missing
threshold = len(earthquake_data) * 0.5
earthquake_data = earthquake_data.dropna(thresh=threshold, axis=1)

# rounds 'Latitude' and 'Longitude' to three decimal places for uniformity
earthquake_data['Latitude'] = earthquake_data['Latitude'].round(3)
earthquake_data['Longitude'] = earthquake_data['Longitude'].round(3)

print("displayinng the first few rows of the cleaned dataframe\n==========")
print(earthquake_data.head())



# TASK 2 

# define the bins and labels for categorization
bins = [0, 5.5, 7.0, 10]  
labels = ['Low', 'Moderate', 'High']  # labels for each category

# categorizing the 'Magnitude' field
earthquake_data['Magnitude Category'] = pd.cut(earthquake_data['Magnitude'], bins=bins, labels=labels)

print("displaying the first few rows of the dataframe with the new category column\n==========")
print(earthquake_data[['Magnitude', 'Magnitude Category']].head())



# TASK 3

# using melt() to reshape the dataset
melted_data = pd.melt(earthquake_data, id_vars=['ID'], value_vars=['Latitude', 'Longitude'],
                      var_name='Coordinate Type', value_name='Coordinate Value')

# using pivot_table() to create a summary table
pivot_table_data = earthquake_data.pivot_table(values='Magnitude', index='Year', aggfunc='mean')

print("displayinng the first few rows of the melted data and the pivot table\n==========")
print(melted_data.head())
print(pivot_table_data.head())


# TASK 4

# 1. line Chart - average magnitude over Years
line_chart_data = earthquake_data.groupby('Year')['Magnitude'].mean().dropna()
plt.figure(figsize=(10, 6))
plt.plot(line_chart_data, marker='o')
plt.title('Average Magnitude of Earthquakes Over Years')
plt.xlabel('Year')
plt.ylabel('Average Magnitude')
plt.grid(True)
plt.show()

# 2. bar Chart - count of earthquake magnitude categories
bar_chart_data = earthquake_data['Magnitude Category'].value_counts()
plt.figure(figsize=(7, 5))
bar_chart_data.plot(kind='bar')
plt.title('Count of Earthquake Magnitude Categories')
plt.xlabel('Magnitude Category')
plt.ylabel('Count')
plt.show()

# 3. scatter chart - magnitude vs depth
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Magnitude', y='Depth', data=earthquake_data)
plt.title('Magnitude vs Depth of Earthquakes')
plt.xlabel('Magnitude')
plt.ylabel('Depth')
plt.show()

# 4. histogram - distribution of earthquake magnitudes
plt.figure(figsize=(7, 5))
plt.hist(earthquake_data['Magnitude'], bins=20, color='blue', edgecolor='black')
plt.title('Distribution of Earthquake Magnitudes')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()
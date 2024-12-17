import pandas as pd

# Define the data for Fisherville
data = {
    "Date": ["2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04", "2024-10-05"],
    "Sample": ["Bird", "Water", "Water", "Bird", "Water"],
    "Concentration": [10.5, 12.3, 8.9, 7.6, 5.3],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the table (for debugging purposes)
print(df)

# Save the DataFrame to a CSV file (to use it in Flask)
df.to_csv("table1_data.csv", index=False)




# Define the data for Site 2
data = {
    "Date": ["2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04", "2024-11-05"],
    "Sample": ["Water", "Bird", "Bird", "Water", "Bird"],
    "Concentration": [2.5, 1.3, 10.6, 8.3, 4.1],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the table (for debugging purposes)
print(df)

# Save the DataFrame to a CSV file (to use it in Flask)
df.to_csv("table2_data.csv", index=False)

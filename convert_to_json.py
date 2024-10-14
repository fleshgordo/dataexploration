import pandas as pd
import json

# Path to your CSV file
csv_file = 'subdimension_text.csv'  # Replace with your actual CSV file path

# Read the CSV file
# Assuming the CSV is comma-separated
df = pd.read_csv(csv_file, sep=',', encoding='utf-8')

# Initialize an empty list to hold the JSON structure
merged_json = []

# Variable to keep track of the current main dimension
current_main = None

# Iterate through each row in the DataFrame
for _, row in df.iterrows():
    # Check if the Subdimension column is NaN or empty
    if pd.isna(row['Subdimension']) or str(row['Subdimension']).strip() == '':
        # It's a main dimension entry
        current_main = {
            "name": str(row['Dimension']).strip(),         # Added "name" field
            "title": str(row['Title']).strip(),
            "text": str(row['Dimension Text']).strip(),
            "subdimensions": []
        }
        merged_json.append(current_main)
    else:
        # It's a subdimension entry
        if current_main is not None:
            sub_dict = {
                "name": str(row['Subdimension']).strip(),
                "title": str(row['Subdimension Title']).strip(),
                "text": str(row['Dimension Text']).strip()
            }
            current_main["subdimensions"].append(sub_dict)
        else:
            print("Warning: Subdimension found without a corresponding main dimension.")

# Path to save the output JSON
output_json_file = 'output.json'  # Replace with your desired output path

# Write the merged JSON to a file with indentation for readability
with open(output_json_file, 'w', encoding='utf-8') as json_file:
    json.dump(merged_json, json_file, indent=4, ensure_ascii=False)

print(f"Merged JSON has been saved to {output_json_file}")

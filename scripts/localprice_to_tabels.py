import pandas as pd
from collections import defaultdict

df_old = pd.read_csv('calculator_localprice.csv')

location_cols = ['location', 'city', 'state', 'postal_code', 'email']
unique_locs = df_old[location_cols].drop_duplicates().reset_index(drop=True)
unique_locs['new_location_id'] = range(1, len(unique_locs) + 1)

counts = defaultdict(int)
unique_names = []
for base in unique_locs['location'].fillna(''):
    counts[base] += 1
    if counts[base] == 1:
        unique_names.append(base)
    else:
        unique_names.append(f"{base} #{counts[base]}")
unique_locs['name'] = unique_names

location_df = unique_locs[['new_location_id', 'name', 'city', 'state', 'postal_code', 'email']].copy()
location_df = location_df.rename(columns={'new_location_id': 'id'})

df_merged = df_old.merge(unique_locs, on=location_cols, how='left')

terminal_names = ['savannah', 'nj', 'houston', 'miami', 'chicago', 'losangeles']
terminal_df = pd.DataFrame({
    'id': range(1, len(terminal_names) + 1),
    'name': terminal_names
})

delivery_price_records = []
dp_id = 1
for _, row in df_merged.iterrows():
    loc_id = int(row['new_location_id'])
    vehicle_type_id = row.get('type_id')
    for term_idx, term_name in enumerate(terminal_names, start=1):
        if term_name in row and pd.notna(row[term_name]):
            delivery_price_records.append({
                'id': dp_id,
                'location_id': loc_id,
                'terminal_id': term_idx,
                'vehicle_type_id': vehicle_type_id,
                'price': row[term_name]
            })
            dp_id += 1

delivery_price_df = pd.DataFrame(delivery_price_records)

unique_vehicle_types = df_old['type_id'].dropna().unique()
vehicle_type_df = pd.DataFrame({
    'id': unique_vehicle_types,
    'auction': [None] * len(unique_vehicle_types),
    'vehicle_type': [None] * len(unique_vehicle_types),
    'specific_type': [None] * len(unique_vehicle_types)
})

location_df.to_csv('location.csv', index=False)
terminal_df.to_csv('terminal.csv', index=False)
delivery_price_df.to_csv('delivery_price.csv', index=False)
vehicle_type_df.to_csv('vehicle_type.csv', index=False)

print("Saved files:")
print("- location.csv")
print("- terminal.csv")
print("- delivery_price.csv")
print("- vehicle_type.csv")

print()
print("Summary:")
print("Total original rows:", len(df_old))
print("Unique location records created:", len(location_df))
print("Total delivery_price rows created:", len(delivery_price_df))

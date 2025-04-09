import pandas as pd
import ast


input_file = "C:\\Users\\Giuseppe\\Downloads\\flights.csv"  
output_file = "C:\\Users\\Giuseppe\\Downloads\\voli_con_lat_lon.csv"


def extract_lat_lon(location_str):
    try:
        loc_dict = ast.literal_eval(location_str.strip())
        lat = float(loc_dict.get("lat", None))
        lon = float(loc_dict.get("lon", None))
        return pd.Series([lat, lon])
    except Exception:
        return pd.Series([None, None])


df = pd.read_csv(input_file)


df[['DestLat', 'DestLon']] = df['DestLocation'].apply(extract_lat_lon)


df[['OriginLat', 'OriginLon']] = df['OriginLocation'].apply(extract_lat_lon)


df.to_csv(output_file, index=False)

print(f"File salvato con successo come '{output_file}' con le colonne lat/lon aggiunte.")
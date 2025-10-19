import os
import re
from pathlib import Path
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, text

# --- CONFIGURATION ---
DB_USER = 'postgres'
DB_PASS = 'mysecretpassword'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'forestry_db'

# --- FILE PATHS ---
SCRIPT_DIR = Path(__file__).parent.resolve()
GPKG_DIR = SCRIPT_DIR
CSV_DIR = SCRIPT_DIR / 'NEFD_v1' / '2024'

# --- NAME MAPPING DICTIONARY ---
NAME_MAPPING_DICT = {
    'Opotiki District': 'Ōpōtiki District',
    'Otorohanga District': 'Ōtorohanga District',
    'Auckland Council': 'Auckland',
    'Tauranga District': 'Tauranga City',
    'Central Hawke\'s Bay District': 'Central Hawke\'s Bay District'
}

# --- UTILITY FUNCTION ---
def clean_col_names(df):
    cols = df.columns
    new_cols = []
    for col in cols:
        new_col = re.sub(r'[^a-zA-Z0-9]', '_', col).lower()
        if new_col and new_col[0].isdigit():
            new_col = '_' + new_col
        new_cols.append(new_col)
    df.columns = new_cols
    return df

# --- MAIN SCRIPT ---
def main():
    print("--- Starting data loading process ---")
    
    try:
        engine_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(engine_url)
        print("✅ Successfully connected to the PostGIS database.")
    except Exception as e:
        print(f"❌ Could not connect to the database. Error: {e}")
        return

    # Load Territorial Authorities Geopackage
    try:
        ta_gpkg_path = GPKG_DIR / 'territorial_authorities.gpkg'
        print(f"\nProcessing '{ta_gpkg_path.name}'...")
        gdf_ta = gpd.read_file(ta_gpkg_path)
        gdf_ta = gdf_ta.rename(columns={'TA2023_V1_00_NAME': 'ta_name', 'wsr_name': 'supply_region_name'})
        print(f"Original CRS: {gdf_ta.crs}. Converting to EPSG:3857 (Web Mercator)...")
        gdf_ta = gdf_ta.to_crs("EPSG:3857") 
        gdf_ta.to_postgis('territorial_authorities', engine, if_exists='replace', index=False)
        print(f"✅ Successfully loaded geographic data into table: 'territorial_authorities' in EPSG:3857.")
    except Exception as e:
        print(f"❌ Failed to load territorial authorities. Error: {e}")
        return

    # Load Wood Supply Regions Geopackage
    try:
        wsr_gpkg_path = GPKG_DIR / 'wood_supply_regions.gpkg'
        print(f"\nProcessing '{wsr_gpkg_path.name}'...")
        gdf_wsr = gpd.read_file(wsr_gpkg_path)
        gdf_wsr = gdf_wsr.to_crs("EPSG:3857")
        gdf_wsr.to_postgis('wood_supply_regions', engine, if_exists='replace', index=False)
        print(f"✅ Successfully loaded geographic data into table: 'wood_supply_regions' in EPSG:3857.")
    except Exception as e:
        print(f"❌ Failed to load wood supply regions. Error: {e}")
        return
        
    # Load all CSV files
    print("\nProcessing all CSV files...")
    csv_files = list(CSV_DIR.glob('*_filled.csv'))
    csv_files.append(CSV_DIR / 'territorial_authority_relationships.csv')

    for file_path in csv_files:
        try:
            table_name = file_path.stem.replace('_area_by_age_and_district_filled', '').replace('_by_age_and_district_filled', '').replace('_filled', '').lower()
            
            print(f"  - Loading '{file_path.name}' into table '{table_name}'...")
            df = pd.read_csv(file_path)
            
            if 'Territorial Authority' in df.columns:
                print(f"    -> Standardizing names in '{table_name}'...")
                df['Territorial Authority'] = df['Territorial Authority'].str.strip().apply(lambda x: NAME_MAPPING_DICT.get(x, x))

            df = clean_col_names(df)
            df.to_sql(table_name, engine, if_exists='replace', index=False)
        except Exception as e:
            print(f"    ❌ Failed to load {file_path.name}. Error: {e}")
            return
    
    print("\n--- Data loading complete! ---")
    print("\nFINAL STEP: Please run the following SQL query in DBeaver to create the final view:")
    print("-" * 60)
    print("""
CREATE OR REPLACE VIEW "final_view" AS
SELECT 
    ta."TA2023_V1_00",
    ta."ta_name",
    ta."supply_region_name",
    COALESCE(asp."total", 0) AS "total_forest_area",
    ta."geometry" 
FROM 
    "territorial_authorities" AS ta
LEFT JOIN 
    "all_species" AS asp ON ta."ta_name" = asp."territorial_authority";
    """)
    print("-" * 60)

if __name__ == "__main__":
    main()
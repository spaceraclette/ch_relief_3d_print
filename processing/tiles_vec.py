"""
create_tiles_lv95.py
--------------------
Creates a grid of 40 km × 40 km tiles over a bounding box defined in
LV95 (EPSG:2056, Swiss Federal Coordinate System).
 
Tile naming convention:
  Each tile is labelled  xNyM  where
    N = 1-based column index counted from the LEFT  (west)
    M = 1-based row    index counted from the BOTTOM (south)
  Example: the bottom-left tile is x1y1, the one to its right is x2y1,
           the one above it is x1y2, etc.
 
Output: a GeoPackage (.gpkg) – open in QGIS, ArcGIS Pro, or any
        GIS tool that reads OGR/GDAL formats.
 
Dependencies:
    pip install geopandas shapely
"""
 
import math
import os
import geopandas as gpd
from shapely.geometry import box
 
 
# ---------------------------------------------------------------------------
# Configuration – edit these values to match your area of interest
# ---------------------------------------------------------------------------
 
MIN_X = 2_479_626   # western  edge in LV95 metres
MAX_X = 2_839_626   # eastern  edge in LV95 metres
MIN_Y = 1_065_599   # southern edge in LV95 metres
MAX_Y = 1_305_599   # northern edge in LV95 metres
 
TILE_SIZE_M = 40_000          # 40 km in metres
OUTPUT_FILE = "./data/vector/tiles_lv95.gpkg"
LAYER_NAME  = "tiles_40km"
 


# ---------------------------------------------------------------------------
# Create tiles
# ---------------------------------------------------------------------------
 
n_cols = math.ceil((MAX_X - MIN_X) / TILE_SIZE_M)
n_rows = math.ceil((MAX_Y - MIN_Y) / TILE_SIZE_M)
 
print(f"Bounding box  : X [{MIN_X:,.0f} – {MAX_X:,.0f}]  Y [{MIN_Y:,.0f} – {MAX_Y:,.0f}]")
print(f"Tile size     : {TILE_SIZE_M / 1000:.0f} km")
print(f"Grid          : {n_cols} columns × {n_rows} rows = {n_cols * n_rows} tiles")
print(os.getcwd())

records = []
 
for col in range(1, n_cols + 1):       # x-index: 1 = leftmost column
    for row in range(1, n_rows + 1):   # y-index: 1 = bottom row
 
        x0 = MIN_X + (col - 1) * TILE_SIZE_M
        y0 = MIN_Y + (row - 1) * TILE_SIZE_M
        x1 = x0 + TILE_SIZE_M
        y1 = y0 + TILE_SIZE_M
 
        records.append({
            "tile_id" : f"x{col}y{row}",
            "col"     : col,
            "row"     : row,
            "x_min"   : x0,
            "y_min"   : y0,
            "x_max"   : x1,
            "y_max"   : y1,
            "geometry": box(x0, y0, x1, y1),
        })
 
gdf = gpd.GeoDataFrame(records, crs="EPSG:2056")
gdf.to_file(OUTPUT_FILE, layer=LAYER_NAME, driver="GPKG")
 
print(f"Saved {len(gdf)} tiles → {os.path.abspath(OUTPUT_FILE)}")

#asfasf
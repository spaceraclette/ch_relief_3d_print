"""
clip_dem_to_tiles.py
--------------------
Clips a 30 m DEM (GeoTIFF) to each tile in a GeoPackage and saves
each clip as a separate GeoTIFF named after the tile (e.g. x1y1.tif).

Dependencies:
    pip install geopandas rasterio shapely
"""

import os
import geopandas as gpd
import rasterio
from rasterio.mask import mask


# ---------------------------------------------------------------------------
# Configuration – edit these paths
# ---------------------------------------------------------------------------

GPKG_FILE   = "./data/vector/tiles_lv95.gpkg"        # path to your tile GeoPackage
LAYER_NAME  = "tiles_40km"             # layer name inside the GeoPackage
DEM_FILE    = "./data/dem/output_hh_lv95.tif"            # path to your input DEM
OUTPUT_DIR  = "./data/dem/dem_tiles"              # folder where clipped tiles are saved


# ---------------------------------------------------------------------------
# Clip DEM to each tile
# ---------------------------------------------------------------------------

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load tiles
tiles = gpd.read_file(GPKG_FILE, layer=LAYER_NAME)
print(f"Loaded {len(tiles)} tiles from {GPKG_FILE}")

with rasterio.open(DEM_FILE) as dem:

    # Make sure tiles and DEM are in the same CRS
    tiles = tiles.to_crs(dem.crs)

    for _, tile in tiles.iterrows():
        tile_id  = tile["tile_id"]
        geometry = [tile["geometry"]]

        try:
            clipped, transform = mask(dem, geometry, crop=True, nodata=dem.nodata)

            # Update metadata for the clipped tile
            meta = dem.meta.copy()
            meta.update({
                "height"   : clipped.shape[1],
                "width"    : clipped.shape[2],
                "transform": transform,
            })

            out_path = os.path.join(OUTPUT_DIR, f"{tile_id}.tif")

            with rasterio.open(out_path, "w", **meta) as dst:
                dst.write(clipped)

            print(f"  Saved {tile_id}.tif")

        except Exception as e:
            print(f"  Skipped {tile_id}: {e}")

print(f"\nDone. Clipped tiles saved to: {os.path.abspath(OUTPUT_DIR)}")
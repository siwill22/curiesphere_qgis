#!/usr/bin/env python3
"""
Placeholder script for geomagnetic field processing.
This will be replaced with actual processing logic.
"""
import sys
import numpy as np
import xarray as xr
import pygmt
# Add parent directory to path so we can import remit
sys.path.insert(0, '/Users/simon/GIT/curiesphere')

def main():
    if len(sys.argv) != 9:
        print("Usage: script.py input_geojson output_nc vis grid_size l_max l_min altitude field_component")
        print(f"Received {len(sys.argv)} arguments: {sys.argv}")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    vis = float(sys.argv[3])
    grid_cell_size = float(sys.argv[4])
    l_max = int(float(sys.argv[5]))
    l_min = int(float(sys.argv[6]))
    altitude = float(sys.argv[7])
    field_component = sys.argv[8]
    
    print(f"Processing with parameters:")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_file}")
    print(f"  VIS: {vis}")
    print(f"  Grid cell size: {grid_cell_size}")
    print(f"  L max: {l_max}")
    print(f"  L min: {l_min}")
    print(f"  Altitude: {altitude}")
    print(f"  Field component: {field_component}")
    
    # PLACEHOLDER: Create dummy NetCDF output
    # Replace this with actual geomagnetic field calculation
    
    from remit.data.models import load_vis_model
    from remit.utils.grid import coeffs2map

    vis = load_vis_model()
    simple_vim = vis.vim()

    vsh, coeffs = simple_vim.transform(lmax=l_max)

    model_rad = coeffs2map(coeffs, altitude=altitude, lmax=l_max, lmin=l_min)

    # Convert pyshtools object to xarray
    print("Converting to xarray...")
    #model_rad = model_rad.to_xarray()

    # Convert longitude from 0-360 to -180-180 to match input data
    #print("Converting longitude from 0-360 to -180-180...")
    #model_rad = model_rad.assign_coords(lon=(((model_rad.lon + 180) % 360) - 180))
    #model_rad = model_rad.sortby('lon')
    #print(f"Longitude range: {model_rad.lon.min().values} to {model_rad.lon.max().values}")
    
    model_rad = pygmt.grdsample(grid=model_rad.to_xarray(), 
                                region='d', 
                                spacing=grid_cell_size)


    model_rad.to_netcdf(output_file)
    print(f"Created output file: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

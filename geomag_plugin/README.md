# GeoMag Processor QGIS Plugin

A QGIS plugin prototype for processing polygon layers with external Python environments.

## Installation

1. Copy the `geomag_plugin` folder to your QGIS plugins directory:
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **macOS**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

2. Restart QGIS

3. Enable the plugin in QGIS:
   - Go to `Plugins > Manage and Install Plugins`
   - Find "GeoMag Processor" and enable it

## Usage

1. Load a polygon vector layer into your QGIS project

2. Launch the plugin from the toolbar or menu: `Plugins > GeoMag Processor`

3. Configure parameters:
   - **Python Interpreter**: Select from detected Python environments
   - **Polygon Layer**: Choose your input layer
   - **VIS**: Viscosity parameter
   - **Grid Cell Size**: Output grid resolution
   - **L max/min**: Maximum/minimum spherical harmonic degree
   - **Altitude**: Calculation altitude
   - **Field Component**: Choose Br, By, or Bz

4. Click "Run" to execute

5. The output NetCDF will be loaded as a raster layer

## External Script

The plugin calls `process_script.py` with the selected Python interpreter. Currently contains placeholder code that generates dummy NetCDF output. Replace with your actual processing logic.

## Requirements

The external Python environment needs:
- numpy
- xarray
- netCDF4 (or similar NetCDF backend)

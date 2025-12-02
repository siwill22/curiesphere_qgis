from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject, QgsRasterLayer
import os
import subprocess
import tempfile
import time
from .geomag_dialog import GeoMagDialog


class GeoMagPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dialog = None
        self.action = None

    def initGui(self):
        """Create the menu entries and toolbar icons"""
        self.action = QAction("GeoMag Processor", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&GeoMag Processor", self.action)

    def unload(self):
        """Remove the plugin menu item and icon"""
        self.iface.removePluginMenu("&GeoMag Processor", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        """Run the plugin"""
        if self.dialog is None:
            self.dialog = GeoMagDialog(self.iface)
        
        self.dialog.show()
        result = self.dialog.exec_()
        
        if result:
            self.execute_processing()

    def execute_processing(self):
        """Execute the external Python script and load results"""
        # Get parameters from dialog
        python_path = self.dialog.get_python_path()
        layer = self.dialog.get_selected_layer()
        vis = self.dialog.get_vis()
        grid_size = self.dialog.get_grid_size()
        l_max = self.dialog.get_l_max()
        l_min = self.dialog.get_l_min()
        altitude = self.dialog.get_altitude()
        field_component = self.dialog.get_field_component()
        
        if not layer:
            QMessageBox.warning(None, "Error", "No layer selected")
            return

        # Generate unique temporary filenames to avoid conflicts with loaded layers
        timestamp = str(int(time.time()))
        temp_dir = tempfile.gettempdir()
        temp_input = os.path.join(temp_dir, f"input_polygon_{timestamp}.geojson")
        temp_output = os.path.join(temp_dir, f"output_result_{timestamp}.nc")
        
        from qgis.core import QgsVectorFileWriter
        QgsVectorFileWriter.writeAsVectorFormat(
            layer, temp_input, "UTF-8", layer.crs(), "GeoJSON"
        )
        
        # Path to external script (placeholder)
        script_path = os.path.join(os.path.dirname(__file__), "process_script2.py")
        
        # Build command
        cmd = [
            python_path,
            script_path,
            temp_input,
            temp_output,
            str(vis),
            str(grid_size),
            str(l_max),
            str(l_min),
            str(altitude),
            field_component
        ]

        # Debug: Print command being executed
        print(f"Executing command: {' '.join(cmd)}")
        print(f"Script path: {script_path}")
        print(f"Script exists: {os.path.exists(script_path)}")

        try:
            # Execute subprocess
            QMessageBox.information(None, "Processing", "Running external script...")

            # Create a clean environment for the subprocess
            # Remove QGIS-specific environment variables that conflict with other Python installations
            env = os.environ.copy()

            # Remove problematic environment variables
            vars_to_remove = ['PYTHONHOME', 'PYTHONPATH']
            for var in vars_to_remove:
                env.pop(var, None)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)

            if result.returncode != 0:
                error_msg = f"Script failed with return code {result.returncode}\n\n"
                error_msg += "STDERR:\n" + (result.stderr if result.stderr else "(empty)") + "\n\n"
                error_msg += "STDOUT:\n" + (result.stdout if result.stdout else "(empty)")
                QMessageBox.critical(None, "Error", error_msg)
                print(f"Command that failed: {' '.join(cmd)}")
                print(f"STDERR: {result.stderr}")
                print(f"STDOUT: {result.stdout}")
                return

            # Show output for successful run
            if result.stdout:
                print(f"Script output:\n{result.stdout}")
            
            # Load NetCDF result
            if os.path.exists(temp_output):
                layer_name = f"GeoMag_{field_component}_{timestamp}"
                rlayer = QgsRasterLayer(temp_output, layer_name)

                if rlayer.isValid():
                    QgsProject.instance().addMapLayer(rlayer)
                    QMessageBox.information(None, "Success", "NetCDF loaded successfully")

                    # Clean up temporary input file (output is kept as it's loaded in QGIS)
                    try:
                        if os.path.exists(temp_input):
                            os.remove(temp_input)
                    except Exception as e:
                        print(f"Warning: Could not remove temp input file: {e}")
                else:
                    QMessageBox.critical(None, "Error", "Failed to load NetCDF")
            else:
                QMessageBox.critical(None, "Error", "Output file not created")
                
        except subprocess.TimeoutExpired:
            QMessageBox.critical(None, "Error", "Script execution timed out")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Execution failed:\n{str(e)}")

from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                                   QComboBox, QDoubleSpinBox, QSpinBox, QPushButton,
                                   QGroupBox, QFormLayout)
from qgis.core import QgsProject, QgsWkbTypes, QgsMapLayerType
import os
import sys
import platform


class GeoMagDialog(QDialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setWindowTitle("GeoMag Processor")
        self.setMinimumWidth(500)
        self.init_ui()
        self.populate_python_envs()
        self.populate_layers()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Python Environment Selection
        env_group = QGroupBox("Python Environment")
        env_layout = QFormLayout()
        self.python_combo = QComboBox()
        env_layout.addRow("Python Interpreter:", self.python_combo)
        env_group.setLayout(env_layout)
        layout.addWidget(env_group)
        
        # Layer Selection
        layer_group = QGroupBox("Input Layer")
        layer_layout = QFormLayout()
        self.layer_combo = QComboBox()
        layer_layout.addRow("Polygon Layer:", self.layer_combo)
        layer_group.setLayout(layer_layout)
        layout.addWidget(layer_group)
        
        # Parameters
        params_group = QGroupBox("Parameters")
        params_layout = QFormLayout()
        
        self.vis_spin = QDoubleSpinBox()
        self.vis_spin.setRange(-1e9, 1e9)
        self.vis_spin.setDecimals(3)
        self.vis_spin.setValue(1.0)
        params_layout.addRow("VIS:", self.vis_spin)
        
        self.grid_size_spin = QDoubleSpinBox()
        self.grid_size_spin.setRange(0.001, 1000)
        self.grid_size_spin.setDecimals(3)
        self.grid_size_spin.setValue(1.0)
        params_layout.addRow("Grid Cell Size:", self.grid_size_spin)
        
        self.l_max_spin = QSpinBox()
        self.l_max_spin.setRange(0, 10000)
        self.l_max_spin.setValue(100)
        params_layout.addRow("L max:", self.l_max_spin)

        self.l_min_spin = QSpinBox()
        self.l_min_spin.setRange(0, 10000)
        self.l_min_spin.setValue(0)
        params_layout.addRow("L min:", self.l_min_spin)
        
        self.altitude_spin = QDoubleSpinBox()
        self.altitude_spin.setRange(-9999999, 9999999)
        self.altitude_spin.setDecimals(3)
        self.altitude_spin.setValue(0.0)
        params_layout.addRow("Altitude:", self.altitude_spin)
        
        self.field_combo = QComboBox()
        self.field_combo.addItems(['Br', 'By', 'Bz'])
        params_layout.addRow("Field Component:", self.field_combo)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run")
        self.cancel_button = QPushButton("Cancel")
        self.run_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def populate_python_envs(self):
        """Find and populate available Python environments"""
        envs = self.find_python_envs()
        for name, path in envs:
            self.python_combo.addItem(name, path)
    
    def find_python_envs(self):
        """Detect Python environments on the system"""
        envs = []
        
        # Current QGIS Python
        envs.append(('QGIS Python', sys.executable))
        
        # System Python
        if platform.system() == 'Windows':
            system_pythons = ['C:\\Python39\\python.exe', 'C:\\Python310\\python.exe', 
                            'C:\\Python311\\python.exe', 'C:\\Python312\\python.exe']
        else:
            system_pythons = ['/usr/bin/python3', '/usr/local/bin/python3']
        
        for path in system_pythons:
            if os.path.exists(path) and path != sys.executable:
                envs.append((f'System: {path}', path))
        
        # Conda environments
        conda_bases = []
        home = os.path.expanduser('~')
        
        if platform.system() == 'Windows':
            conda_bases = [
                os.path.join(home, 'anaconda3', 'envs'),
                os.path.join(home, 'miniconda3', 'envs'),
                'C:\\ProgramData\\anaconda3\\envs'
            ]
            python_exe = 'python.exe'
        else:
            conda_bases = [
                os.path.join(home, 'anaconda3', 'envs'),
                os.path.join(home, 'miniconda3', 'envs'),
                '/opt/anaconda3/envs',
                '/opt/miniconda3/envs'
            ]
            python_exe = 'bin/python'
        
        for conda_base in conda_bases:
            if os.path.exists(conda_base):
                for env_name in os.listdir(conda_base):
                    python_path = os.path.join(conda_base, env_name, python_exe)
                    if os.path.exists(python_path):
                        envs.append((f'Conda: {env_name}', python_path))
        
        return envs
    
    def populate_layers(self):
        """Populate combo box with polygon layers from current project"""
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayerType.VectorLayer:
                if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                    self.layer_combo.addItem(layer.name(), layer)
    
    def get_python_path(self):
        return self.python_combo.currentData()
    
    def get_selected_layer(self):
        return self.layer_combo.currentData()
    
    def get_vis(self):
        return self.vis_spin.value()
    
    def get_grid_size(self):
        return self.grid_size_spin.value()
    
    def get_l_max(self):
        return self.l_max_spin.value()
    
    def get_l_min(self):
        return self.l_min_spin.value()
    
    def get_altitude(self):
        return self.altitude_spin.value()
    
    def get_field_component(self):
        return self.field_combo.currentText()

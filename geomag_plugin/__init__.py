def classFactory(iface):
    from .geomag_plugin import GeoMagPlugin
    return GeoMagPlugin(iface)

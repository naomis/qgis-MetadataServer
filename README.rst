This is a Python plugin for QGIS Server to retrieve the metadata defined in the layer properties from the service's project.

Python plugins support for QGIS Server has been introduced recently with QGIS 2.8 and it is enabled by default on most distributions.

# Call
http://localhost:8000/?SERVICE=Metadata&LAYERS=...&FORMAT=XML

# Parameters
* LAYER (mandatory) : layer identifier (one layer at a time)
* FORMAT : Supported formats - XML (default) | HTML

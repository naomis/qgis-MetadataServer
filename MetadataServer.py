# -*- coding: utf-8 -*-

"""
***************************************************************************
    Metadata.py
    ---------------------
    Date                 : January 2020
    Copyright            : (C) 2020 by Patrick Chapuis
    Email                : p.chapuis at naomis dot fr
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Patrick Chapuis'
__date__ = 'January 2020'
__copyright__ = '(C) 2020, Patrick Chapuis - Naomis'


from qgis.server import QgsService
from qgis.core import QgsMapLayer, QgsMessageLog, Qgis
from PyQt5.QtXml import QDomDocument


class MetadataServerService(QgsService):
    def __init__(self):
        QgsService.__init__(self)

    def name(self):
        return "METADATA"

    def version(self):
        return "1.0.0"

    def executeRequest(self, request, response, project):
        response.setStatusCode(200)
        mdFormat = request.parameter('FORMAT') if 'FORMAT' in request.parameters() else LayerMD.MD_FORMATS[0]
        if 'LAYER' not in request.parameters():
            self.__tell(response, "LAYER is not in request's parameters", level=Qgis.Critical)
        elif mdFormat.upper() not in LayerMD.MD_FORMATS:
            self.__tell(response, "Format \"{}\" is not part of {}".format(request.parameter('FORMAT'), " | ".join(LayerMD.MD_FORMATS)), level=Qgis.Critical)
        else:
            layerName = request.parameter('LAYER')
            layer = LayerMD.GET(project, layerName)
            if layer is None:
                self.__tell(response, "Layer \"{}\" is not part of the project".format(layerName), level=Qgis.Critical)
            else:
                self.__tell(response, layer.get(mdFormat), level=Qgis.Success)

    def __tell(self, response, message, level=Qgis.Info):
        QgsMessageLog.logMessage(message, level=level)
        response.write(message)
        if level in [Qgis.Critical]:
            response.setStatusCode(500)

class MetadataServer():
    def __init__(self, serverIface):
        serverIface.serviceRegistry().registerService(MetadataServerService())

    def createService(self):
        return MetadataServerService()


class LayerMD(QgsMapLayer):
    MD_FORMATS = ["XML", "HTML"]

    @classmethod
    def GET(cls, project, layerName):
        layers = project.mapLayersByName(layerName)
        layer = layers[0] if len(layers)>0 else None
        if layer:
            layer.__class__ = cls
        return layer

    @property
    def html(self):
        return self.htmlMetadata()

    @property
    def xml(self):
        md = QDomDocument()
        self.exportNamedMetadata(md, None)
        return md.toString()

    @property
    def json(self):
        return "Not implemented yet"
    
    def get(self, format):
        if format.upper()=='XML':
            return self.xml
        elif format.upper()=='HTML':
            return self.html
        elif format.upper()=='JSON':
            return self.json
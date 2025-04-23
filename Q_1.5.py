from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFeatureSink,
    QgsFeature,
    QgsFields,
    QgsField,
    QgsGeometry,
    QgsWkbTypes,
    QgsFeatureSink
)

class GravitationalAttraction(QgsProcessingAlgorithm):
    
    INPUT_POLYGONS = 'INPUT_POLYGONS'
    INPUT_POINTS = 'INPUT_POINTS'
    INPUT_NEG_POLYGONS = 'INPUT_NEG_POLYGONS'
    OUTPUT_TABLE = 'OUTPUT_TABLE'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_POLYGONS,
                'Capas de polígonos ambientales',
                QgsProcessing.TypeVectorPolygon
            )
        )
        
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_NEG_POLYGONS,
                'Capas de polígonos negativos (vertederos)',
                QgsProcessing.TypeVectorPolygon,
                optional=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POINTS,
                'Capa de puntos de cálculo',
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_TABLE,
                'Resultado de atracción gravitacional'
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        poly_layers = self.parameterAsLayerList(parameters, self.INPUT_POLYGONS, context)
        neg_poly_layers = self.parameterAsLayerList(parameters, self.INPUT_NEG_POLYGONS, context) or []
        point_layer = self.parameterAsVectorLayer(parameters, self.INPUT_POINTS, context)
        
        fields = QgsFields()
        fields.append(QgsField('Point_ID', QVariant.Int))
        fields.append(QgsField('Attraction_Total', QVariant.Double))
        fields.append(QgsField('Attraction_Positive', QVariant.Double))
        fields.append(QgsField('Attraction_Negative', QVariant.Double))
        
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT_TABLE, context, fields, QgsWkbTypes.NoGeometry, point_layer.sourceCrs())
        
        if not poly_layers or not point_layer:
            feedback.reportError('Error: No se encontraron capas adecuadas')
            return {}
        
        results = []
        
        for point_feat in point_layer.getFeatures():
            point_geom = point_feat.geometry().asPoint()
            point_id = point_feat.id()
            
            total_attraction = 0
            positive_attraction = 0
            negative_attraction = 0
            
            # Calcular la atracción positiva
            for poly_layer in poly_layers:
                for poly_feat in poly_layer.getFeatures():
                    area = float(poly_feat['Area'])
                    density = float(poly_feat['Densidad'])
                    distance = poly_feat.geometry().distance(QgsGeometry.fromPointXY(point_geom))
                    
                    if distance > 0:
                        attraction = (area * density) / (distance ** 2)
                        positive_attraction += attraction
                        total_attraction += attraction
            
            # Calcular la atracción negativa
            for neg_poly_layer in neg_poly_layers:
                for neg_feat in neg_poly_layer.getFeatures():
                    area = float(neg_feat['Area'])
                    density = float(neg_feat['Densidad'])
                    distance = neg_feat.geometry().distance(QgsGeometry.fromPointXY(point_geom))
                    
                    if distance > 0:
                        attraction = (area * density) / (distance ** 2)
                        negative_attraction += attraction
                        total_attraction -= attraction
            
            # Normalización simple (división por 10,000)
            total_attraction_normalized = total_attraction / 10000
            positive_attraction_normalized = positive_attraction / 10000
            negative_attraction_normalized = negative_attraction / 10000
            
            # Crear el nuevo feature con los valores normalizados
            new_feat = QgsFeature()
            new_feat.setAttributes([point_id, total_attraction_normalized, positive_attraction_normalized, negative_attraction_normalized])
            sink.addFeature(new_feat, QgsFeatureSink.FastInsert)
        
        return {self.OUTPUT_TABLE: dest_id}
    
    def name(self):
        return 'gravitational_attraction'
    
    def displayName(self):
        return 'Cálculo de Atracción Gravitacional Ambiental'
    
    def group(self):
        return 'Análisis Ambiental'
    
    def groupId(self):
        return 'analysis_environmental'
    
    def createInstance(self):
        return GravitationalAttraction()

#!/usr/bin/env python3


from enum import Enum


class HY_Features(Enum):
    HY_Catchment = "hyf:HY_Catchment"
    HY_CatchmentDivide = "hyf:HY_CatchmentDivide"
    HY_HydrographicNetwork = "hyf:HY_HydrographicNetwork"
    HY_HydrometricNetwork = "hyf:HY_HydrometricNetwork"
    HY_HydroNexus = "hyf:HY_HydroNexus"
    HY_HydroLocation = "hyf:HY_HydroLocation"
    HY_HydrometricFeature = "hyf:HY_HydrometricFeature"
    HY_WaterBody = "hyf:HY_WaterBody"
    HY_Lake = "hyf:HY_Lake"
    HY_Impoundment = "hyf:HY_Impoundment"
    HY_River = "hyf:HY_River"
    HY_Channel = "hyf:HY_Channel"
    HY_FlowPath = "hyf:HY_FlowPath"
    HY_DistanceDescription = "hyf:HY_DistanceDescription"
    HY_HydroLocationType = "hyf:HY_HydroLocationType"
    HY_IndirectPosition = "hyf:HY_IndirectPosition"
    HY_DistanceFromReferent = "hyf:HY_DistanceFromReferent"
    upstreamWaterBody = "hyf:upstreamWaterBody"
    downstreamWaterBody = "hyf:downstreamWaterBody"
    lowerCatchment = "hyf:lowerCatchment"
    upperCatchment = "hyf:upperCatchment"
    realizedCatchment = "hyf:realizedCatchment"
    catchmentRealization = "hyf:catchmentRealization"
    contributingCatchment = "hyf:contributingCatchment"
    outflow = "hyf:outflow"
    realizedNexus = "hyf:realizedNexus"
    networkStation = "hyf:networkStation"
    referencedPosition = "hyf:referencedPosition"
    distanceExpression = "hyf:distanceExpression"
    distanceDescription = "hyf:distanceDescription"
    linearElement = "hyf:linearElement"
    hydrometricNetwork = "hyf:hydrometricNetwork"
    nexusRealization = "hyf:nexusRealization"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

class Feature(object):
    def __init__(self, hyfeature, id=None, is_realized=True):
        self.name = hyfeature.name
        self.feature = hyfeature
        self.type = None
        self.id = None
        self.is_realized = is_realized
        self.realized_features = []

        if self.is_realized:
            self.type = f'http://www.opengeospatial.org/standards/waterml2/hy_features/{self.name}'
            self.id = id


class HyfContext(object):

    def __init__(self):

        self.__hyfeatures = {}

    @property
    def context_url(self):
        return ['https://opengeospatial.github.io/ELFIE/json-ld/elf.jsonld']

    def add_feature(self, feature, id=None, is_realized=True):
        self.__hyfeatures[feature.name] = self.create_feature(feature,
                                                              id,
                                                              is_realized)
        return self.__hyfeatures[feature.name]

    def create_feature(self, feature, id, is_realized):
        if not isinstance(feature, HY_Features):
            raise Exception(f'Must provide member of HY_Features class')
        return Feature(feature, id=id, is_realized=is_realized)

    def add_realization(self, parent_feature, realized_feature, realized_id=None):
        feat = self.create_feature(realized_feature, realized_id, True)
        if parent_feature.is_realized:
            raise Exception('Cannot add realized HY_Feature to a realized object')

        self.__hyfeatures[parent_feature.name].realized_features.append(feat)

    @property
    def features(self):
        return self.__hyfeatures

    @property
    def context(self):
        """
        return json object
        """
        import pdb; pdb.set_trace()
        realizations = [{'@id': f.id, '@type': f.type} for f in self.features]

        return {'@type': type,
                name: realizations
                }

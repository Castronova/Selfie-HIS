#!/usr/bin/env python3


class HydrometricNetwork():
    def __init__(self):
        self.context = []
        self.features = []
       
        # add the hyf context
        self.add_context("https://www.opengis.net/def/appschema/hy_features/hyf/")

    def add_context(self, context):
        if context not in self.context:
            self.context.append(context)

    def add_feature(self, name, id,
                    description=None, geo=None, gsp=None):
        feature = {"@type": "HY_HydrometricFeature",
                   "name": name,
                   "id": id}
        if description is not None:
            feature["description"] = description
        if geo is not None:
            feature["geo"] = geo
        if gsp is not None:
            feature["hasGeometry"] = gsp

            # add the geosparql context if it doesn't already exist
            self.add_context({"gsp":
                              "http://www.opengeospatial.org/standards/geosparql/"})

        self.features.append(feature)

    def as_dict(self, geoms=True):
        if geoms:
            return {"HY_HydrometricNetwork": self.features}
        else:
            keys_to_keep = ['@type', 'name', 'id']
            res = [{key: item[key] for key in keys_to_keep}
                   for item in self.features]
            return {'HY_HydrometricNetwork': res}

    def get_context(self):
        return self.context

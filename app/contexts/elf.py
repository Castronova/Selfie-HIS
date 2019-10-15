#!/usr/bin/env python3

import shapely.wkt


class ElfContext(object):

    def __init__(self):
        self.__name = None
        self.__gsp = None
        self.__description = None
        self.__geo = None
        self.__hasGeometry = None
        self.__image = None
        self.__related = None
        self.__sameAs = None
        self.__skos = None
        self.__asWKT = None
        self.__geometry = None

    def geometry_from_wkt(self, wkt):
        self.__geometry = shapely.wkt.loads(wkt)

    @property
    def geom(self):
        return self.__geometry

    @property
    def context_url(self):
        """ returns list of context urls """
        return ['https://opengeospatial.github.io/ELFIE/json-ld/elf.jsonld',
                {'gsp': 'http://www.opengeospatial.org/standards/geosparql/'}]

    @property
    def context(self):
        """
        return json object
        """

        obj = {"description": self.description,
               "name": self.name}

        for k, v in {'geo': self.geo,
                     'gsp.hasGeometry': self.hasGeometry,
                     'image': self.image,
                     'sameAs': self.sameAs,
                     'related': self.related}.items():
            if v is not None:
                obj[k] = v

        return obj

    @property
    def skos(self):
        return self.__skos

    @property
    def gsp(self):
        return self.__gsp

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, v):
        self.__description = v

    @property
    def geo(self):
        if self.geom.type == 'Point':
            return {
                    "@type": "schema.GeoCoordinates",
                    "schema.latitude": self.geom.y,
                    "schema.longitude": self.geom.x
                    }

    @geo.setter
    def geo(self, v):
        self.__geo = v

    @property
    def hasGeometry(self):
        """ returns ELF hasGeometry json """
        return {
                "@type": "gsp:Geometry",
                "gsp:asWKT": self.asWKT
                }

    @property
    def asWKT(self):
        """ returns wkt for geometry """

        return self.geom.wkt

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, v):
        self.__image = v

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, v):
        self.__name = v

    @property
    def sameAs(self):
        return self.__sameAs

    @sameAs.setter
    def sameAs(self, v):
        self.__sameAs = v

    @property
    def related(self):
        return self.__related

    @related.setter
    def related(self, v):
        self.__related = v

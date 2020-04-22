#!/usr/bin/env python3


import requests
import xml.etree.ElementTree as ET


def PointInPolygon(lat, lon, property_name):

    url = 'https://arcgis.cuahsi.org/arcgis/services/US_WBD/HUC_WBD/MapServer/WFSServer'

    xml = f"""
    <ogc:Filter>
        <ogc:Contains>
            <ogc:PropertyName>HUC12</ogc:PropertyName>
              <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
                <gml:coordinates>{lon},{lat}</gml:coordinates>
              </gml:Point>
        </ogc:Contains>
    </ogc:Filter>
    """

    params = {
             'service': 'WFS',
             'request': 'GetFeature',
             'typeName': 'HUC_WBD:HUC12_US',
             'SrsName': 'EPSG:4326',
             'Filter': f'{xml}'
            }

    r = requests.get(url, params=params, verify=False)

    if r.status_code == 200:
        return ET.fromstring(r.text)

    return None


if __name__ == '__main__':
    lat = 34.9
    lon = -92.9
    property_name = 'HUC12'


    res = PointInPolygon(lat, lon, property_name)

    import pdb; pdb.set_trace()
    print('done')



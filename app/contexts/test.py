
import pdb
import hyf


H = hyf.HyfContext()

netStation = H.add_feature(hyf.HY_Features.networkStation, is_realized=False)
pdb.set_trace()
H.add_realization(netStation, hyf.HY_Features.HY_HydrometricFeature,
                  'https://opengeospatial.github.io/ELFIE/usgs/nwissite/huc12obs/USGS-05427880')
H.add_realization(netStation, hyf.HY_Features.HY_HydrometricFeature,
                  'https://opengeospatial.github.io/ELFIE/usgs/wqp/huc12obs/WIDNR_WQX-10001227')

realCatchment = H.add_feature(hyf.HY_Features.HY_Catchment,
                              id='https://opengeospatial.github.io/ELFIE/usgs/huc/huc12obs/070900020601',
                              is_realized=True)

print(H.context)

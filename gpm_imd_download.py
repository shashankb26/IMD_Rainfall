
import os
from array import array
import numpy as np
from osgeo import osr, gdal
import requests

import warnings
warnings.filterwarnings("ignore")

from logs import MyLogger


dirname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname)

logger = MyLogger(module_name = __name__, filename="gpm_imd.log")


def read_file(filename,nbytes,endian):
    count = os.path.getsize(filename)/nbytes
    with open(filename, 'rb') as fid:
        result = array('f')
        result.fromfile(fid,int(count))
        if endian != os.sys.byteorder: result.byteswap()
        fid.close()
        return result


def createRaster(ingrd, outraster, xulcorner, yulcorner):
        
    try:
        raw_field = read_file(ingrd,4,'little')
        data_1 = np.asarray(raw_field,np.float)
        india_dly_rainfall = data_1.reshape([281,241])
        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(outraster, 241, 281, 1, gdal.GDT_Float32)
        # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
        dst_ds.SetGeoTransform([xulcorner, 0.25, 0, yulcorner, 0, -0.25])
        srs = osr.SpatialReference()
        srs.SetWellKnownGeogCS("WGS84")
        dst_ds.SetProjection(srs.ExportToWkt())
        dst_ds.GetRasterBand(1).WriteArray(np.flipud(india_dly_rainfall))
        dst_ds.GetRasterBand(1).SetNoDataValue(float(-999))
        dst_ds.SetMetadataItem("AREA_OR_POINT","POINT")
        dst_ds = None
        logger.info(f"Raster Created: {outraster} ")
    except Exception as e:
        logger.error(f"Raster Creation Failed {ingrd}: {e}")


def download_gpm_imd(current_date, save_pathfile):
    
    url = f"https://imdpune.gov.in/Seasons/Temperature/gpm/rain.php?rain={current_date}"
    
    response = requests.get(url)

    try:    
        with open(save_pathfile, 'wb') as src:
            src.write(response.content)  
            print(response.status_code)
    
    except Exception as e:
        logger.error(f"Download Failed {current_date}: {e}")
    


if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)
    
    pass
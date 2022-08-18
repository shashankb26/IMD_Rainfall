from rasterstats import zonal_stats
import geopandas as gpd
import pandas as pd
import os
from glob import glob
from shapely.geometry import mapping


def read_farm(farm_path, setcrs=False):

    geom = pd.read_csv(farm_path, header=None, sep='\n')

    farm_poly = gpd.GeoSeries.from_wkt(geom.iloc[:, 0])

    if setcrs:
        return farm_poly.set_crs("EPSG:4326").centroid

    return farm_poly


def get_py_geometry(farm_path, **kwargs):

    farm_poly = read_farm(farm_path, **kwargs)

    return farm_poly


def get_zonal_stats(farm_path, raster_images, **kwargs):

    feat = get_py_geometry(farm_path, **kwargs)

    soil_nutrients = {}
    mylist = []
    for raster_image in raster_images:

        raster_filename = os.path.splitext(os.path.basename(raster_image))[0]
        stats = zonal_stats(feat, raster_image, stats='median',
                            geojson_out=True, nodata=-999)
        raster_stats = [i['properties'] for i in stats]
        soil_nutrients[raster_filename] = raster_stats[0]
        mylist.append(raster_stats[0]['median'])
    return soil_nutrients


if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)

    # farm_path = '/home/satyukt/sylesh/area/504.csv'
    # farm_id = os.path.basename(farm_path).split(".")[0]
    # raster_images = glob(f"../tif/*21.tif")
    # soil_nuts = get_zonal_stats(farm_path, raster_images, setcrs=True)
    # print(pd.DataFrame.from_dict(soil_nuts))

    farm_path = gpd.read_file(
        "/home/satyukt/Downloads/Thanjavur_district.gpkg")
    raster_images = glob(f"../tif/*.tif")
    soil_nutrients = {}
    mylist = []
    for raster_image in raster_images:

        raster_filename = os.path.splitext(os.path.basename(raster_image))[0]
        stats = zonal_stats(farm_path, raster_image, stats='mean',
                            geojson_out=True, nodata=-999)
        raster_stats = [i['properties'] for i in stats]
        soil_nutrients[raster_filename] = raster_stats[0]
        mylist.append(raster_stats[0]['mean'])

    df = pd.DataFrame.from_dict(soil_nutrients).T
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df = df.sort_index()
    df.to_csv("~/Downloads/Shashank_rainfall_mean.csv")

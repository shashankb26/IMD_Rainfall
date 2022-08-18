import datetime as dt
from datetime import timedelta
import os
from gpm_imd_download import createRaster, download_gpm_imd

nlat = 281
nlon = 241
res = 0.25
xulcorner = 50
yulcorner = -30 + nlat * res - res


if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)

    current_date = dt.datetime.today().date()
    prev_date = current_date - timedelta(days=1)
    time_period = 50

    for i in range(2, time_period):

        dd_date = current_date - dt.timedelta(days=i)
        ft_date = dd_date.strftime("%Y%m%d")
        raster_path = f"../tif/{ft_date}.tif"
        grd_path = f"../grd/{ft_date}.grd"

        if not os.path.exists(grd_path):
            download_gpm_imd(dd_date.strftime("%d%m%Y"), grd_path)

        if not os.path.exists(raster_path):
            createRaster(grd_path, raster_path, xulcorner, yulcorner)

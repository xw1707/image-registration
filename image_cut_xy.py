import os, sys, gdal
from gdalconst import *
import glob
SAVE_PATH = 'C:\\Users\\12043\\Desktop\\test\\'

def get_extent(fn):
    ds = gdal.Open(fn)
    rows = ds.RasterYSize
    cols = ds.RasterXSize
    print(cols, rows)
    # 获取图像角点坐标
    gt = ds.GetGeoTransform()
    minx = gt[0]
    maxy = gt[3]
    maxx = gt[0] + gt[1] * cols
    miny = gt[3] + gt[5] * rows
    print(minx, maxy, maxx, miny)
    return (minx, maxy, maxx, miny)

os.chdir(SAVE_PATH)
in_files = glob.glob('*.tif')
# 通过两两比较大小,将最终符合条件的四个角点坐标保存，
# 即为拼接图像的四个角点坐标
minX, maxY, maxX, minY = get_extent(in_files[0])
print(minX, maxY, maxX, minY)
for fn in in_files[1:]:
    minx, maxy, maxx, miny = get_extent(fn)
    print(minx, maxy, maxx, miny)
    minX = min(minX, minx)
    maxY = max(maxY, maxy)
    maxX = max(maxX, maxx)
    minY = min(minY, miny)
print( )
print(minX, maxY, maxX, minY)
print( maxX - minX, maxY - minY)

# 获取输出图像的行列数
in_ds = gdal.Open(in_files[0])
gt = in_ds.GetGeoTransform()
cols = int(maxX - minX) / abs(gt[5])
rows = int(maxY - minY) / gt[1]
print(abs(gt[5]), gt[1])
print(cols, rows)

# 创建输出图像
driver = gdal.GetDriverByName('gtiff')
out_ds = driver.Create('mosaic.tif', int(cols), int(rows))
out_ds.SetProjection(in_ds.GetProjection())
out_band = out_ds.GetRasterBand(1)

gt = list(in_ds.GetGeoTransform())
gt[0], gt[3] = minX, maxY
out_ds.SetGeoTransform(gt)

for fn in in_files:
    in_ds = gdal.Open(fn)
    trans = gdal.Transformer(in_ds, out_ds, [])
    success, xyz = trans.TransformPoint(False, 0, 0)
    x, y, z = map(int, xyz)
    data = in_ds.GetRasterBand(1).ReadAsArray()
    out_band.WriteArray(data, x, y)

del in_ds, out_band, out_ds
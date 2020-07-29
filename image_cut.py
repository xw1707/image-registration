from osgeo import gdal
from PIL import Image
from skimage import io

# 切成 X_NUM * Y_NUM 张图片
X_NUM = 4
Y_NUM = 4

IMAGE_NAME = 'C:\\Users\\12043\\Desktop\\a.png'  # 原影像 用来获取影像大小与地理坐标
SAVE_PATH = 'C:\\Users\\12043\\Desktop\\'
SAVE_NAME = 'picture_cut/'
SUB_NAME = 'result'

# 解除读取图片大小的限制
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import os
import cv2
import time

import warnings

warnings.filterwarnings("ignore")

time_start = time.time()

def train_img_cut(Dataset, sub_row, sub_col, SaveDir, Subname, startid=0):

    i, j = 0, 0
    img_row, img_col = Dataset.RasterYSize, Dataset.RasterXSize

    print(img_row, img_col)
    end_row = img_row
    end_col = img_col
    print("sub_row = ", sub_row, "sub_col = ", sub_col,
          "end_row = ", end_row, "end_col = ", end_col)

    start = startid

    while i + Y_NUM < end_row:
        while j + X_NUM < end_col:

            sub_img = Dataset.ReadAsArray(int(j), int(i), int(min(end_col - j, sub_col)),
                                          int(min(end_row - i, sub_row))).transpose(1, 2, 0).astype(np.uint8)
            print(int(j), int(i), int(min(end_col - j, sub_col)),
                  int(min(end_row - i, sub_row)))
            j += sub_col

            if not os.path.exists(SaveDir):
                os.makedirs(SaveDir)

            try:
                if start < 10:
                    io.imsave(SaveDir + '/' + Subname + '0' +
                              str(start) + '.tiff', sub_img)
                    print(start, "time:", time.time() - time_start)
                else:
                    io.imsave(SaveDir + '/' + Subname +
                              str(start) + '.tiff', sub_img)
                    print(start, "time:", time.time() - time_start)
            except IOError:
                print('fail to load image!', IOError)
                exit()

            start += 1

            del sub_img
            print("i = ", i, "j = ", j)

        i += sub_row
        j = 0
    print(start)
    return start


if __name__ == '__main__':

    id = 0

    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    Dataset = gdal.Open(IMAGE_NAME)
    xsize = Dataset.RasterXSize
    ysize = Dataset.RasterYSize

    print("time:", time.time() - time_start, "s", xsize, ysize)

    # SaveName 必须为英文
    ids = train_img_cut(Dataset, ysize / Y_NUM, xsize / X_NUM,
                        SAVE_PATH + SAVE_NAME, SUB_NAME, startid=id)

    print("time:", time.time() - time_start, "s")

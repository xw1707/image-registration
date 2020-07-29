import PIL.Image as Image
import os

IMAGES_PATH = 'C:\\Users\\12043\\Desktop\\picture_cut\\'  # 图片集地址
IMAGES_FORMAT = ['.tiff', ]  # 图片格式
IMAGE_ROW = 4  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 4  # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = 'C:\\Users\\12043\\Desktop\\final.tiff'  # 图片转换后的地址

# 获取图片集地址下的所有图片名称
image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]

# 简单的对于参数的设定和实际图片集的大小进行数量判断
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    print ValueError("error")

# 定义图像拼接函数


def image_compose():
    Dataset = gdal.Open(IMAGES_PATH + image_names[0])
    xsize = Dataset.RasterXSize
    ysize = Dataset.RasterYSize
    to_image = Image.new('RGB', (IMAGE_COLUMN * xsize,
                                 IMAGE_ROW * ysize))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (xsize, ysize), Image.ANTIALIAS)
            print(image_names[IMAGE_COLUMN * (y - 1) + x - 1])
            to_image.paste(from_image, ((x - 1) * xsize, (y - 1) * ysize))
    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


image_compose()  # 调用函数

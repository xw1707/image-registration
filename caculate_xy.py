SAVE_PATH = 'D:\\map\\'

os.chdir(SAVE_PATH)
tifFile = 's_arc0.tif'

dataset = gdal.Open(tifFile)
band = dataset.GetRasterBand(1)

xsize = dataset.RasterXSize
ysize = dataset.RasterYSize
i = 1
j = 1
totalX = 0
totalY = 0
count = 0
gt = list(dataset.GetGeoTransform())
for i in range(0, int(ysize * 0.5)):#遍历所有长度的点
    for j in range(int(xsize * 0.5),xsize):#遍历所有宽度的点
        data = band.ReadAsArray(j, i, 1, 1)
#        print (data, j, i)#打印每个像素点的颜色RGBA的值(r,g,b,alpha)
        
        if (data != 0.0):
#            print(j, i)
#            print(data)
            totalX += gt[0] + gt[1] * j
            totalY += gt[3] + gt[5] * i
            count += 1
print(count)
print(totalX / count)
print(totalY / count)
#img.putpixel((30,20),(255,0,0,255))
#img = img.convert("RGB")#把图片强制转成RGB
#img.save('C:\\Users\\12043\\Desktop\\test.tif')#保存修改像素点后的图片
del dataset
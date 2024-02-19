#! /bin/python

import os
import sys
import netCDF4 as nc
import numpy as np

from PIL import Image, ImageEnhance, ImageOps

# 参数导入
if len(sys.argv) > 1:
    data = sys.argv[1]
else:
    data = "./NC_H09_20240131_2240_R21_FLDK.06001_06001.nc"


nc = nc.Dataset(data)

def vis(nc):

    # 提取对应波段数据
    blue = nc.variables['albedo_01'][:]
    green = nc.variables['albedo_02'][:]
    red = nc.variables['albedo_03'][:]
    # 归一化
    for i in [blue, green, red]:
        i = i / np.max(i)

    # 组合成三维数组
    rgb = np.dstack((red, green, blue))

    # 转编码
    rgb = (rgb * 255).astype(np.uint8)

    imgVis = Image.fromarray(rgb)
    print("可见光处理完成")
    return imgVis

def ir(nc):
    wave = nc.variables['tbb_14'][:]

    # 归一化
    wave = ((wave - np.min(wave)) * (255 - 0)) / (np.max(wave) - np.min(wave)) + 255

    wave = wave.astype(np.uint8)

    imgIR = Image.fromarray(wave)
    imgIR = ImageOps.invert(imgIR)

    print("红外处理完成")
    return imgIR

def blend(vis, ir):

    # 确保大小模式相同
    if ir.size != vis.size:
        ir = ir.resize(vis.size)

    if ir.mode != vis.mode:
        ir = ir.convert(vis.mode)

    img = Image.blend(ir, vis, alpha=0.8)
    
    print("合并完成")
    return img

def color(img):
    #亮度
    img_1 = ImageEnhance.Brightness(img)
    img_1 = img_1.enhance(1.3)

    #对比度
    img_2 = ImageEnhance.Contrast(img_1)
    img_2 = img_2.enhance(1.1)
    
    #饱和度
    img_3 = ImageEnhance.Color(img_2)
    img = img_3.enhance(2)
    print("色彩处理完成")
    return img



if __name__ == "__main__":    
    color(blend(vis(nc), ir(nc))).save('./1.png')

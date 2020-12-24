# 获取照片中的EXIF信息，并写入到文件
# @author 冷朴承
# @time 2020-12-24
# @version 1.0

import os
import exifread


class Exif:
    def __init__(self, name, device, model, width, length, date, time, camera, lat, lon, gps, gpsTimeStamp):
        # 文件名
        self.name = name
        # 设备型号
        self.device = device
        # 设备版本
        self.type = model
        # 照片宽
        self.width = width
        # 照片长
        self.length = length
        # 创建日期
        self.date = date
        # 拍摄日期
        self.time = time
        # gsp方法(GPS/北斗)
        self.gps = gps
        # gps时间
        self.gpsTimeStamp = gpsTimeStamp
        # 相机版本
        self.camera = camera
        # 经度
        self.location_lat = lat
        # 维度
        self.location_lon = lon


def getEXFI(filePath):
    with open(filePath, 'rb') as f:
        tags = exifread.process_file(f)
        try:
            # 纬度
            LatRef = tags["GPS GPSLatitudeRef"].printable
            Lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            Lat = float(Lat[0]) + float(Lat[1]) / 60 + float(Lat[2]) / float(Lat[3]) / 3600
            if LatRef != "N":
                Lat = Lat * (-1)
            # 经度
            LonRef = tags["GPS GPSLongitudeRef"].printable
            Lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            Lon = float(Lon[0]) + float(Lon[1]) / 60 + float(Lon[2]) / float(Lon[3]) / 3600
            if LonRef != "E":
                Lon = Lon * (-1)
            f.close()
            return Exif(name=filePath, device=tags['Image Make'], model=tags['Image Model'],
                        width=tags['EXIF ExifImageWidth'],
                        length=tags['EXIF ExifImageLength'], date=tags['Image DateTime'],
                        time=tags["EXIF DateTimeOriginal"],
                        gps=tags['GPS GPSProcessingMethod'], gpsTimeStamp=tags['GPS GPSTimeStamp'],
                        camera=tags['Image Software'],
                        lat=Lat, lon=Lon)
        except:
            f.close()
            return Exif(filePath, "", "", "", "", "", "", "", "", "", "", "")


# 批量获取
def getEXFIs(driPath):
    listEXFI = []
    for root, dirs, files in os.walk(driPath):
        for file in files:
            path = os.path.join(root, file)
            exif = getEXFI(path)
            listEXFI.append(exif)
    return listEXFI


def writeToExfi(dir, file='exfi.txt'):
    list = getEXFIs(dir)
    f = open(file, mode='w')
    t = '{},{},{},{},{},{},{},{},{},{},{} \n'.format("文件名", "设备", "型号", "时间", "相机", "长度", "宽度", "经度", "维度", "定位方式",
                                                     "定位类型")
    f.write(t)
    for exfi in list:
        t = '{},{},{},{},{},{},{},{},{},{},{} \n'.format(exfi.name, exfi.device, exfi.type, exfi.time, exfi.camera,
                                                         exfi.length, exfi.width, exfi.location_lon, exfi.location_lat,
                                                         exfi.gps, exfi.gpsTimeStamp)
        print(t)
        f.write(t)
    f.close()
    print("写入完毕！")


if __name__ == "__main__":
    writeToExfi("Camera/")

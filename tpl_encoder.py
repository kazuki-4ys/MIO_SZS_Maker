import os, sys
from enum import Enum
from PIL import Image
import TPLLib

class Utils:
    @staticmethod
    def bytesToU16(buf, offset, isLE):
        num = 0
        for i in range(2):
            num <<= 8
            if isLE:
                num += buf[offset + 1 - i]
            else:
                num += buf[offset + i]
        return num
    def bytesToU32(buf, offset, isLE):
        num = 0
        for i in range(4):
            num <<= 8
            if isLE:
                num += buf[offset + 3 - i]
            else:
                num += buf[offset + i]
        return num
    def bytesToU64(buf, offset, isLE):
        num = 0
        for i in range(8):
            num <<= 8
            if isLE:
                num += buf[offset + 7 - i]
            else:
                num += buf[offset + i]
        return num
    def bytesToFile(buf, fileName):
        try:
            os.makedirs(os.path.dirname(fileName), exist_ok=True)
        except FileNotFoundError:
            pass
        try:
            f = open(fileName, 'wb')
            f.write(buf)
            f.close()
        except:
            return False
        else:
            return True
    def U16ToBytes(buf, offset, val, isLE):
        for i in range(2):
            if isLE:
                buf[offset + i] = (val >> (i * 8)) & 0xFF
            else:
                buf[offset + i] = (val >> ((1 - i) * 8)) & 0xFF
    def U32ToBytes(buf, offset, val, isLE):
        for i in range(4):
            if isLE:
                buf[offset + i] = (val >> (i * 8)) & 0xFF
            else:
                buf[offset + i] = (val >> ((3 - i) * 8)) & 0xFF
    def U64ToBytes(buf, offset, val, isLE):
        for i in range(8):
            if isLE:
                buf[offset + i] = (val >> (i * 8)) & 0xFF
            else:
                buf[offset + i] = (val >> ((7 - i) * 8)) & 0xFF
    def fileToBytes(fileName):
        try:
            f = open(fileName, 'rb')
            buf = f.read()
        except:
            return False
        else:
            return bytearray(buf)

class TPLFormat(Enum):
    I4 = 0
    I8 = 1
    IA4 = 2
    IA8 = 3
    RGB565 = 4
    RGB5A3 = 5
    RGBA32 = 6
    C4 = 8
    C8 = 9
    C14X2 = 0xA
    CMPR = 0xE

class TPLEncodeSetting():
    def __init__(self):
        self.size = None
        self.format = TPLFormat.RGB5A3

def encodeTPL(srcImage, dest, encodeSetting):
    img = Image.open(srcImage)
    img = img.convert("RGBA")
    if encodeSetting is None:
        encodeSetting = TPLEncodeSetting()
    if encodeSetting.size is not None and img.size != encodeSetting.size:
        img = img.resize(encodeSetting.size, Image.LANCZOS)
    if encodeSetting.format == TPLFormat.I4:
        encoder = TPLLib.I4Encoder
    elif encodeSetting.format == TPLFormat.I8:
        encoder = TPLLib.I8Encoder
    elif encodeSetting.format == TPLFormat.IA4:
        encoder = TPLLib.IA4Encoder
    elif encodeSetting.format == TPLFormat.IA8:
        encoder = TPLLib.IA8Encoder
    elif encodeSetting.format == TPLFormat.RGB565:
        encoder = TPLLib.RGB565Encoder
    elif encodeSetting.format == TPLFormat.RGB5A3:
        encoder = TPLLib.RGB4A3Encoder
    elif encodeSetting.format == TPLFormat.RGBA32:
        encoder = TPLLib.RGBA8Encoder
    width = img.size[0]
    height = img.size[1]
    rawRgbaPixels = list()
    for i in range(height):
        for j in range(width):
            rgbaT = img.getpixel((j, i))
            rawRgbaPixels.append(rgbaT[2])
            rawRgbaPixels.append(rgbaT[1])
            rawRgbaPixels.append(rgbaT[0])
            rawRgbaPixels.append(rgbaT[3])
    e = encoder(rawRgbaPixels, width, height)
    rawTPLPixels = bytearray(e.run())
    header = bytearray(0x40)
    header[0] = 0x00
    header[1] = 0x20
    header[2] = 0xAF
    header[3] = 0x30
    Utils.U32ToBytes(header, 4, 1, False)
    Utils.U32ToBytes(header, 8, 0xC, False)
    Utils.U32ToBytes(header, 0xC, 0x14, False)
    Utils.U16ToBytes(header, 0x14, height, False)
    Utils.U16ToBytes(header, 0x16, width, False)
    Utils.U32ToBytes(header, 0x18, encodeSetting.format.value, False)
    Utils.U32ToBytes(header, 0x1C, 0x40, False)
    header[0x2B] = 1
    header[0x2F] = 1
    rawDestData = header + rawTPLPixels
    Utils.bytesToFile(rawDestData, dest) 

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit()
    encodeTPL(sys.argv[1], sys.argv[2], None)
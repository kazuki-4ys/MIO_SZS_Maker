import random, string, os, sys, json5, json, shutil, subprocess, glob, traceback, asyncio, threading
from enum import Enum
from pathlib import Path
import ctypes
import time
from wuj5_helper import *
from wuj5.wuj5 import *
from tpl_encoder import *

class RunFunc1FrThreading(threading.Thread):
    def __init__(self, obj):
        self.obj = obj
        threading.Thread.__init__(self, daemon=True)
    def run(self):
        asyncio.run(self.runFunc1frLoop())
    async def runFunc1frLoop(self):
        while True:
            await asyncio.sleep(1 / 60)
            self.obj.run1fr()

class System():
    def __init__(self):
        self.thisScriptDir = System.getThisScriptDir()
    def getRandomDirPath(self):
        if not os.path.isdir(self.thisScriptDir + "/tmp"):
            os.makedirs(self.thisScriptDir + "/tmp", exist_ok=True)
        result = ""
        while (len(result) == 0) or os.path.isfile(result) or os.path.isdir(result):
            result = self.thisScriptDir + "/tmp/" + System.getRandomString(16)
        return result
    def getRandomFilePath(self, ext):
        if not os.path.isdir(self.thisScriptDir + "/tmp"):
            os.makedirs(self.thisScriptDir + "/tmp", exist_ok=True)
        result = ""
        while (len(result) == 0) or os.path.isfile(result) or os.path.isdir(result):
            result = self.thisScriptDir + "/tmp/" + System.getRandomString(16) + ext
        return result
    @staticmethod
    def getRandomString(length):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
        return "".join(randlst)
    def getThisScriptDir():
        #normal launch
        if os.path.basename(sys.executable) == "python.exe" or os.name != "nt":
            return os.path.dirname(__file__)
        else:
            #pyinstaller
            return os.path.dirname(sys.executable)
    def delFile(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
    def delDir(dir):
        try:
            shutil.rmtree(dir)
        except FileNotFoundError:
            pass
    def getWimgtFormatString(src):
        return ["I4", "I8", "IA4", "IA8", "RGB565", "RGB5A3", "RGBA32", None, "C4", "C8", "C14X2", None, None, None, "CMPR"][src.value]
        
class NotSupportThisBrlyt(Exception):
    pass
    
class myBrlyt():
    def __init__(self, srcPath):
        self.srcPath = srcPath
        self.system = System()
        self.jsonDict = decodeBrlyt(self.srcPath)
        group = self.getSectionByMagic("grp1")
        if len(group["panes"]) != 0:
            raise NotSupportThisBrlyt("brlyt with group not supported")
    def getTimgDirPath(self):
        return str(Path(os.path.dirname(self.srcPath)).parent) + "/timg"
    def createPicturePane(self, name, tplPath):
        timgPath = self.getTimgDirPath()
        shutil.copy(tplPath, timgPath + "/" + name + ".tpl")
        self.removePaneByName(name)
        tpls = self.getSectionByMagic("txl1")["tpls"]
        tplIndex = len(tpls)
        tplDict = dict()
        tplDict["name"] = name + ".tpl"
        tpls.append(tplDict)
        materials = self.getSectionByMagic("mat1")["materials"]
        materialIndex = len(materials)
        newMaterial = '''{
    "name": "material_name",
    "tev color 0 r": 0,
    "tev color 0 g": 0,
    "tev color 0 b": 0,
    "tev color 0 a": 0,
    "tev color 1 r": 255,
    "tev color 1 g": 255,
    "tev color 1 b": 255,
    "tev color 1 a": 255,
    "tev color 2 r": 255,
    "tev color 2 g": 255,
    "tev color 2 b": 255,
    "tev color 2 a": 255,
    "tev k color 0 r": 255,
    "tev k color 0 g": 255,
    "tev k color 0 b": 255,
    "tev k color 0 a": 255,
    "tev k color 1 r": 255,
    "tev k color 1 g": 255,
    "tev k color 1 b": 255,
    "tev k color 1 a": 255,
    "tev k color 2 r": 255,
    "tev k color 2 g": 255,
    "tev k color 2 b": 255,
    "tev k color 2 a": 255,
    "tev k color 3 r": 255,
    "tev k color 3 g": 255,
    "tev k color 3 b": 255,
    "tev k color 3 a": 255,
    "attributes": {
        "texture maps": [
            {
                "texture index": 0,
                "s": 0,
                "t": 0
            }
        ],
        "texture srts": [
            {
                "translate x": 0.0,
                "translate y": 0.0,
                "rotate": 0.0,
                "scale x": 1.0,
                "scale y": 1.0
            }
        ],
        "texture uv gens": [
            {
                "type": 1,
                "source": 4,
                "matrix": 30
            }
        ]
    }
}'''
        newMaterial = json.loads(newMaterial)
        newMaterial["name"] = name
        newMaterial["attributes"]["texture maps"][0]["texture index"] = tplIndex
        materials.append(newMaterial)
        newPane = '''{
    "magic": "pic1",
    "flags": {
        "visible": true,
        "influenced alpha": false,
        "location adjust": false
        },
    "base position": "center",
    "opacity": 255,
    "name": "pane_name",
    "user data": "",
    "translation x": 0,
    "translation y": 0,
    "translation z": 0.0,
    "rotation x": 0.0,
    "rotation y": 0.0,
    "rotation z": 0.0,
    "scale x": 1.0,
    "scale y": 1.0,
    "size x": 64.0,
    "size y": 64.0,
    "vertex color top left r": 255,
    "vertex color top left g": 255,
    "vertex color top left b": 255,
    "vertex color top left a": 255,
    "vertex color top right r": 255,
    "vertex color top right g": 255,
    "vertex color top right b": 255,
    "vertex color top right a": 255,
    "vertex color bottom left r": 255,
    "vertex color bottom left g": 255,
    "vertex color bottom left b": 255,
    "vertex color bottom left a": 255,
    "vertex color bottom right r": 255,
    "vertex color bottom right g": 255,
    "vertex color bottom right b": 255,
    "vertex color bottom right a": 255,
    "material": 0,
    "uv sets": [
        {
            "top left u": 0.0,
            "top left v": 0.0,
            "top right u": 1.0,
            "top right v": 0.0,
            "bottom left u": 0.0,
            "bottom left v": 1.0,
            "bottom right u": 1.0,
            "bottom right v": 1.0
        }
    ]
}'''
        newPane = json.loads(newPane)
        newPane["name"] = name
        newPane["material"] = materialIndex
        panes = self.getSectionByMagic("pan1")["children"]
        panes.append(newPane)

    def getSectionByMagic(self, magic):
        if self.jsonDict is None:
            return None
        for i in self.jsonDict["sections"]:
            if i["magic"] == magic:
                return i
        return None
    def removeTextureByIndex(self, index):
        tpls = self.getSectionByMagic("txl1")["tpls"]
        del tpls[index]
        materials = self.getSectionByMagic("mat1")["materials"]
        for m in materials:
            for Tmap in m["attributes"]["texture maps"]:
                if Tmap["texture index"] >= index:
                    Tmap["texture index"] -= 1
    def isThisTextureUnused(self, index):
        materials = self.getSectionByMagic("mat1")["materials"]
        if (materials is None) or len(materials) == 0:
            return True
        for m in materials:
            for Tmap in m["attributes"]["texture maps"]:
                if Tmap["texture index"] == index:
                    return False
        return True
    def removeMaterialByIndex(self, index):
        materials = self.getSectionByMagic("mat1")["materials"]
        textures = list()
        for Tmap in materials[index]["attributes"]["texture maps"]:
            textures.append(Tmap["texture index"])
        del materials[index]
        panes = self.getSectionByMagic("pan1")["children"]
        for p in panes:
            if p["material"] >= index:
               p["material"] -= 1
        for t in textures:
            if self.isThisTextureUnused(t):
                self.removeTextureByIndex(t)
    def isThisMaterialUnused(self, index):
        panes = self.getSectionByMagic("pan1")["children"]
        if len(panes) == 0:
            return True
        for p in panes:
            if p["material"] == index:
                return False
        return True
    def removePaneByName(self, name):
        panes = self.getSectionByMagic("pan1")["children"]
        targetPane = None
        for p in panes:
            if p["name"] == name:
                targetPane = p
                break
        if targetPane is None:
            return
        materialIndex = targetPane["material"]
        panes.remove(targetPane)
        if self.isThisMaterialUnused(materialIndex):
            self.removeMaterialByIndex(materialIndex)
    def save(self):
        if self.jsonDict is None:
            return
        encodeBrlyt(self.jsonDict, self.srcPath)
    def createTplList(self):
        try:
            timgPath = self.getTimgDirPath()
            tpls = self.getSectionByMagic("txl1")["tpls"]
            dest = list()
            for i in tpls:
                dest.append(timgPath + "/" + i["name"])
            return dest
        except:
            return list()


class mySzs():
    def __init__(self, srcPath):
        self.srcPath = srcPath
        self.system = System()
        self.extractedDirPath = self.system.getRandomFilePath(".szs.d")
        decode_u8(self.srcPath, self.extractedDirPath, None, list())
    def save(self, outPath):
        encode_u8(self.extractedDirPath, outPath, None, list())
    def deleteUnusedTpls(self):
        usedTpls = list()
        brlytPaths = glob.glob(self.extractedDirPath + "/*/blyt/*.brlyt")
        for bp in brlytPaths:
            myBp = myBrlyt(bp)
            usedTpls += myBp.createTplList()
        tplPaths = glob.glob(self.extractedDirPath + "/*/timg/*.tpl")
        for i in range(len(tplPaths)):
            tplPaths[i] = tplPaths[i].replace("\\", "/")
        for i in range(len(usedTpls)):
            usedTpls[i] = usedTpls[i].replace("\\", "/")
        for t in tplPaths:
            if not (t in usedTpls):
                System.delFile(t)
    def __del__(self):
        pass
        System.delDir(self.extractedDirPath)

class MIO_SZS_Task(threading.Thread):
    def __init__(self):
        self.taskDone = True
        self.error = ""
        self.curProcess = ""
        self.srcSzsDir = ""
        self.srcPngPath = ""
        self.miiId = 0x80000001
        self.destSzsDir = ""
        self.tplEncodeSetting = TPLEncodeSetting()
        self.isIconDelete = False
        threading.Thread.__init__(self, daemon=True)
        self._stop = threading.Event()
    def run(self):
        self.runAsNormal()
    def raiseExceptionToStop(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
    def runAsNormal(self):
        self.createMIOSzs(self.srcSzsDir, self.srcPngPath, self.miiId, self.destSzsDir, self.tplEncodeSetting)
    def createMIOSzs(self, srcSzsDir, srcPngPath, miiId, destSzsDir, tplEncodeSetting):
        if tplEncodeSetting is None:
            tplEncodeSetting = TPLEncodeSetting()
        s = System()
        System.delDir(System.getThisScriptDir() + "/tmp")
        System.delDir(destSzsDir)
        os.makedirs(System.getThisScriptDir() + "/tmp", exist_ok=True)
        os.makedirs(destSzsDir, exist_ok=True)
        settingDict = MyJson.decodeJson(srcSzsDir + "/setting.json")
        if settingDict is None:
            self.error = "cannot decode setting.json"
            self.taskDone = True
            return
        try:
            tmpTplPath = s.getRandomFilePath(".tpl")
            if not self.isIconDelete:
                self.curProcess = "encodeing tpl..."
                encodeTPL(srcPngPath, tmpTplPath, tplEncodeSetting)
                if not os.path.isfile(tmpTplPath):
                    self.error = "cannot encode tpl"
                    self.taskDone = True
                    return
            shutil.copy(srcSzsDir + "/setting.json", destSzsDir + "/setting.json")
            szsList = glob.glob(srcSzsDir + "/*.szs")
            for szsFile in szsList:
                brlytPath = list()
                for s in settingDict["modify_brlyt_setting"]:
                    if s["szs_filename"] == os.path.basename(szsFile):
                        brlytPath = s["brlyt_path"]
                if len(brlytPath) == 0:
                    shutil.copy(szsFile, destSzsDir + "/" + os.path.basename(szsFile))
                    continue
                self.curProcess = "extracting %s..." % (os.path.basename(szsFile))
                mySzsFile = mySzs(szsFile)
                self.curProcess = "modifying %s..." % (os.path.basename(szsFile))
                for bp in brlytPath:
                    if self.isIconDelete:
                        mblyt = myBrlyt(mySzsFile.extractedDirPath + "/" + bp)
                        mblyt.removePaneByName("mii_%08x" % (miiId))
                        mblyt.save()
                    else:
                        mblyt = myBrlyt(mySzsFile.extractedDirPath + "/" + bp)
                        mblyt.createPicturePane("mii_%08x" % (miiId), tmpTplPath)
                        mblyt.save()
                if self.isIconDelete:
                    mySzsFile.deleteUnusedTpls()
                self.curProcess = "compressing %s..." % (os.path.basename(szsFile))
                mySzsFile.save(destSzsDir + "/" + os.path.basename(mySzsFile.srcPath))
            System.delFile(tmpTplPath)
            self.curProcess = "All done!!"
            self.taskDone = True
        except:
            self.taskDone = True
            self.error = traceback.format_exc()
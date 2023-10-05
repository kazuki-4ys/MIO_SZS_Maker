from wuj5.brlyt import unpack_brlyt, pack_brlyt
import json5, json

class MyJson():
    @staticmethod
    def decodeJson(jsonPath):
        dest = None
        try:
            with open(jsonPath) as file:
                dest = json.load(file)
            return dest
        except:
            return None
    def decodeJson5(json5Path):
        dest = None
        try:
            with open(json5Path) as file:
                dest = json5.load(file)
            return dest
        except:
            return None
    def encodeJson5(jsonDict, outPath):
        with open(outPath, "w") as file:
            json5.dump(jsonDict, file)

def decodeBrlyt(srcBrlyt):
    data = None
    with open(srcBrlyt, 'rb') as in_file:
        data = in_file.read()
    val = unpack_brlyt(data)
    return val
def encodeBrlyt(srcDict, destBrlyt):
    out_data = pack_brlyt(srcDict)
    with open(destBrlyt, 'wb') as out_file:
        out_file.write(out_data)
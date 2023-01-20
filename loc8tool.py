import json
    
def intReader(file):
    return int.from_bytes(file.read(4), "big")

def strReader(file):
    strLen = int.from_bytes(file.read(4), "big")
    return file.read(strLen).decode("utf-8")

def deserialize(loc8):
    arrayLoc = {}
    langCount = intReader(loc8)
    for x in range(langCount):
        langId = intReader(loc8)
        arrayLoc[langId] = {}
        langEntries = intReader(loc8)
        for x in range(langEntries):
            stringId = intReader(loc8)
            stringContent = strReader(loc8)
            arrayLoc[langId][stringId] = stringContent
    return arrayLoc

def serialize(locjson, output):
    file = open(output, "wb")
    langCount = len(locjson)
    file.write(langCount.to_bytes(4, "big"))
    for langId in locjson:
        langEntries = len(locjson[langId])
        file.write(int(langId).to_bytes(4, "big"))
        file.write(langEntries.to_bytes(4, "big"))
        for string in locjson[langId]:
            file.write(int(string).to_bytes(4, "big"))
            file.write(len(locjson[langId][string].encode('utf8')).to_bytes(4, 'big'))
            file.write(locjson[langId][string].encode('utf8'))
    file.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E\x00\x00\x00\x00\x00\x00\x00\x0E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E')
            
print("UBIART LOC8 Tool by AugustoDoidin - 20/01/2023")
option = input("[1] - SERIALIZE\n[2] - DESERIALIZE\nSelect option: ")
match option:
    case "1":
        print("Serialize!")
        try:
            with open("localisation.json", "r", encoding="utf8") as locfile:
                locjson = json.load(locfile)
            serialize(locjson, "localisation.loc8")
        except:
            print("Serializing failed!")
    case "2":
        print("Deserialize!")
        try:
            loc8 = open("localisation.loc8", 'rb')
            with open("localisation.json", "w", encoding="utf8") as locfile:
                locfile.write(json.dumps(deserialize(loc8), indent = 4, ensure_ascii=False) )
        except:
            print("Deserializing failed!")
        
    case _:
        print("Exiting.")



    
    
    

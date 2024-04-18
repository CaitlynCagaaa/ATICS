import APIFunctions_1_1
import json
url ="http://127.0.0.1:5000/add_drawer"
jsonfile = open('drawer.json')
d =json.load(jsonfile)
d = d[0]
#ret =APIFunctions_1_1.addDrawer(url, d["DrawerNum"], d["BoxNum"], d["StartX"], d["StartY"], d["PixelWidth"], d["PixelHeight"], d["DrawerYAML"], d["PicWithAllTools"], d["PicWithNoTools"], d["DrawerSymbolsvar"])
#print(ret)
jsonfile = open('tools.json')
tools =json.load(jsonfile)
url ="http://127.0.0.1:5000/add_tool"

for tool in tools["Tools"]:
    print(tool["LocationIdentifier"])
    ret =APIFunctions_1_1.addTool(url,tool["ToolName"],tool["ToolType"],tool["ClassifierType"],tool["LocationIdentifier"],
        tool["IDAvailable"], tool["IDMark"], tool["CheckedOut"], tool["StartX"],
        tool["StartY"], tool["PixelWidth"], tool["PixelHeight"], tool["PictureWithTool"],
       tool["PictureWithoutTool"], tool["TakenManually"])
    print(ret)
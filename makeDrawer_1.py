import APIFunctions_1_1
import json
url ="http://127.0.0.1:5000/add_drawer"
jsonfile = open('drawer.json')
d =json.load(jsonfile)
d = d[0]
#ret =APIFunctions_1_1.addDrawer(url, d["DrawerNum"], d["DrawerBoxNum"], d["DrawerStartX"], d["DrawerStartY"], d["DrawerPixelWidth"], d["DrawerPixelHeight"], d["DrawerYAML"], d["DrawerPicAllTools"], d["DrawerPicNoTools"], d["DrawerSymbols"])
#print(ret)
jsonfile = open('tools.json')
tools =json.load(jsonfile)
url ="http://127.0.0.1:5000/add_tool"
for tool in tools["Tools"]:
    
     ret =APIFunctions_1_1.addTool(url,tool["ToolName"],tool["ToolType"],tool["ToolClassifierType"],tool["ToolDrawerID"],
         tool[" ToolSymbolAvailable"], tool["ToolSymbolPath"], tool["ToolCheckedOut"], tool["ToolStartX"],
         tool["ToolStartY"], tool["ToolPixelWidth"], tool["ToolPixelHeight"], tool["ToolPictureWithPath"],
        tool["ToolPictureWithoutPath"], tool["ToolInfoTakenManually"])
     print(ret)
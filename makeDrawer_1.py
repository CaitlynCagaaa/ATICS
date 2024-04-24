""" module: makeDrawer_1
    file: makeDrawer_1.py 
    application: Automated tool box inventory control system helper script
    language: python
    computer: ROG Flow Z13 GZ301ZE_GZ301ZE
    opertaing system: windows subsystem  ubuntu
    course: CPT_S 422
    team: Null Terminators
    author: Caitlyn Powers 
    date: 4/17/24
   """
import APIFunctions_1_1
import json
"""
    name:makeDrawer_1
    purpose: Put modified drawer.json and tools.json from additional script into the database. 
    operation: Prints out if the drawer and each tool was uploaded successfully. Will need to check the database before hand
    to see what the dRawerID will end up being to give to put into the tools databasse. 
"""
url ="http://127.0.0.1:5000/add_drawer"
jsonfile = open('drawer.json')
d =json.load(jsonfile)
d = d[0]
ret =APIFunctions_1_1.addDrawer(url, d["DrawerNum"], d["DrawerBoxNum"], d["DrawerStartX"], d["DrawerStartY"], d["DrawerPixelWidth"], d["DrawerPixelHeight"], d["DrawerYAML"], d["DrawerPicAllTools"], d["DrawerPicNoTools"], d["DrawerSymbols"])
print(ret)
jsonfile = open('tools.json')
tools =json.load(jsonfile)
url ="http://127.0.0.1:5000/add_tool"
for tool in tools["Tools"]:
    
     ret =APIFunctions_1_1.addTool(url,tool["ToolName"],tool["ToolType"],tool["ToolClassifierType"],tool["ToolDrawerID"],
         tool[" ToolSymbolAvailable"], tool["ToolSymbolPath"], tool["ToolCheckedOut"], tool["ToolStartX"],
         tool["ToolStartY"], tool["ToolPixelWidth"], tool["ToolPixelHeight"], tool["ToolPictureWithPath"],
        tool["ToolPictureWithoutPath"], tool["ToolInfoTakenManually"])
     print(ret)
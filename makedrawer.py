import APIFunctions_1_1
import json
url ="http://127.0.0.1:5000/add_drawer"
jsonfile = open('drawer.json')
d =json.load(jsonfile)
d = d[0]

#ret =APIFunctions_1_1.addDrawer(url, d["DrawerNum"], d["BoxNum"], d["X"], d["Y"], d["W"], d["H"], d["drawerYaml"], d["picall"], d["picno"], d["drawersymbols"])#print(ret)
jsonfile = open('tools.json')
tools =json.load(jsonfile)
url ="http://127.0.0.1:5000/add_tool"

for tool in tools["Tools"]:
    ret =APIFunctions_1_1.addTool(url,tool["Name"],tool["ToolType"],tool["ClassifierThinks"],tool["Location"],
        tool["IDAvail"], tool["IDMark"], tool["CheckedOut"], tool["X"],
        tool["Y"], tool["W"], tool["H"], tool["picfull"],
       tool["picnull"], tool["Manual"])
    print(ret)
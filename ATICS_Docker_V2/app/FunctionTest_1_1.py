from APIFunctions_1_1 import addDrawer, addTool, addEvent, getToolsInfo, getDrawersInfo, updateToolsInfo

#URL for accessing different endpoints
url = 'http://localhost:5000/add_event'

#getToolsInfo(url,100)   #getToolsInfo function

#getDrawersInfo(url,1)   #getDrawersInfo function

#updateToolsInfo(url, True,10, 100) #updateToolsInfo function

### addDrawer function test ###

drawerNum = 1
drawerBoxNum = 1
drawerStartX = 10
drawerStartY = 20
drawerPixelWidth = 100
drawerPixelHeight = 200
drawerYAML = "example_yaml_data"
drawerPicAllTools = "path_to_all_tools_image"
drawerPicNoTools = "path_to_no_tools_image"
drawerSymbols = None
#addDrawer(url, drawerNum, drawerBoxNum, drawerStartX, drawerStartY, drawerPixelWidth, drawerPixelHeight, drawerYAML, drawerPicAllTools, drawerPicNoTools, drawerSymbols)

### addTool function test ###
toolName = "test"
toolType = "test"
toolClassifierType = "test"
toolDrawerID = 1
toolSymbolAvailable = False
toolSymbolPath = "test"
toolCheckedOut = False
toolStartX = 10
toolStartY = 10
toolPixelWidth = 100
toolPixelHeight = 100
toolPictureWithPath = "test"
toolPictureWithoutPath = "test"
toolInfoTakenManually = False
#addTool(url, toolName,toolType,toolClassifierType,toolDrawerID,
#        toolSymbolAvailable, toolSymbolPath, toolCheckedOut, toolStartX,
#        toolStartY, toolPixelWidth, toolPixelHeight, toolPictureWithPath,
#        toolPictureWithoutPath, toolInfoTakenManually)

### addEvent function test ###

eventType = 1
eventToolID = 3
eventTimestamp = '2024-03-27 12:00:00'
eventDrawerLocation = 1
eventUserID = 456
eventNotes = 'Tool checked out by user'
addEvent(url, eventType, eventToolID, eventTimestamp, eventDrawerLocation, eventUserID, eventNotes)

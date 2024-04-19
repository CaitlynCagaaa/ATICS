import requests
import json
def addDrawer(url, drawerNum, drawerBoxNum, drawerStartX, drawerStartY, drawerPixelWidth, drawerPixelHeight, drawerYAML, drawerPicAllTools, drawerPicNoTools, drawerSymbols):
    data = {
        'DrawerNum': drawerNum,
        'DrawerBoxNum': drawerBoxNum,
        'DrawerStartX': drawerStartX,
        'DrawerStartY': drawerStartY,
        'DrawerPixelWidth': drawerPixelWidth,
        'DrawerPixelHeight': drawerPixelHeight,
        'DrawerYAML': drawerYAML,
        'DrawerPicAllTools': drawerPicAllTools,
        'DrawerPicNoTools': drawerPicNoTools,
        'DrawerSymbols': json.dumps(drawerSymbols)
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Drawer added successfully!")
            return True
        else:
            print("Failed to add drawer. Status code:", response.status_code)
            print("Error message from server:", response.text)
            return False
    except requests.RequestException as e:
        print("Error:", e)
        return False

def addTool(url, toolName, toolType, toolClassifierType, toolDrawerID, toolSymbolAvailable, toolSymbolPath, toolCheckedOut, toolStartX, toolStartY, toolPixelWidth, toolPixelHeight, toolPictureWithPath, toolPictureWithoutPath, toolInfoTakenManually):
    data = {
        'ToolName': toolName,
        'ToolType': toolType,
        'ToolClassifierType': toolClassifierType,
        'toolDrawerID': toolDrawerID,
        'ToolSymbolAvailable': toolSymbolAvailable,
        'ToolSymbolPath': toolSymbolPath,
        'ToolCheckedOut': toolCheckedOut,
        'ToolStartX': toolStartX,
        'ToolStartY': toolStartY,
        'ToolPixelWidth': toolPixelWidth,
        'ToolPixelHeight': toolPixelHeight,
        'ToolPictureWithPath': toolPictureWithPath,
        'ToolPictureWithoutPath': toolPictureWithoutPath,
        'ToolInfoTakenManually': toolInfoTakenManually
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Tool added successfully!")
            return True
        else:
            print("Failed to add tool. Make sure ToolDrawerID is actually in the drawers table. Status code:", response.status_code)
            print("Error message from server:", response.text)
            return False
    except requests.RequestException as e:
        print("Error:", e)
        return False
    
def addEvent(url, eventType, eventToolID, eventTimestamp, eventDrawerLocation, eventUserID, eventNotes):
    data = {
        'EventType': eventType,
        'EventToolID': eventToolID,
        'EventTimestamp': eventTimestamp,
        'EventDrawerLocation': eventDrawerLocation,
        'EventUserID': eventUserID,
        'EventNotes': eventNotes
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Event added successfully!")
            return True
        else:
            print("Failed to add event. Make sure EventToolID and EventDrawerLocation (Foreign keys) are actually in the database already.Status code:", response.status_code)
            return False
    except requests.RequestException as e:
        print("Error:", e)
        return False
    
def getToolsInfo(url, toolsDrawerID):
    #print(toolsDrawerID)
    params = {'drawer_id': toolsDrawerID}
    response = requests.get(url, params=params)
    return response.json()

def getDrawersInfo(url, drawerBoxNum):
    params = {'boxNum': drawerBoxNum}
    response = requests.get(url, params=params)
    #print(response.json())
    return response.json()

def updateToolsInfo(url, checkedOut, toolID, drawerID):
    params = {
        'checkedOut': checkedOut,
        'toolID': toolID,
        'drawerID': drawerID
    }
    response = requests.post(url, json=params)
    return response.json()
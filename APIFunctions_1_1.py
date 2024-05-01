""" module: Api_functions_1_1
    file: Api_functions_1_1.py
    application: Automated tool box inventory control system 
    language: python
    computer: i5 9600k
    opertaing system: windows subsystem  ubuntu
    course: CPT_S 422
    team: Null Terminators
    author: Navin Sabandith
    date: 4/10/24
"""

"""
These functions directly interact with the corresponding api endpoints. Functions are called with appropriate endpoint URL along with specified parameters.
Security: The api key is hardcoded into the functions below. Should an adversary attempt to issue a request to the api endpoints, it will refuse unless the key from here is included in the header.
"""

import requests
import json

"""
    name: addDrawer
    purpose: add a drawer to the drawers table in the database.
    operation: add function parameters to data dictionary. add key to the header. initiate a request.post() with url = add_drawer endpoint, json = to the data dict, and header = api
"""
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
    headers = {'API-Key': "Navinskey"}
    try:
        response = requests.post(url, json=data, headers=headers)
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

"""
    name: addTool
    purpose: add a tool to the tools table in the database.
    operation: Same operation as above.
"""
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
    headers = {'API-Key': "Navinskey"}
    try:
        response = requests.post(url, json=data, headers=headers)
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
    
"""
    name: addEvent
    purpose: add a event to the events table in the database.
    operation: Same operation as above.
"""
def addEvent(url, eventType, eventToolID, eventTimestamp, eventDrawerLocation, eventUserID, eventNotes):
    data = {
        'EventType': eventType,
        'EventToolID': eventToolID,
        'EventTimestamp': eventTimestamp,
        'EventDrawerLocation': eventDrawerLocation,
        'EventUserID': eventUserID,
        'EventNotes': eventNotes
    }
    headers = {'API-Key': "Navinskey"}
    try:
        response = requests.post(url, json=data,headers = headers)
        if response.status_code == 200:
            print("Event added successfully!")
            return True
        else:
            print("Failed to add event. Make sure EventToolID and EventDrawerLocation (Foreign keys) are actually in the database already.Status code:", response.status_code)
            print("Error message:", response.text)
            return False
    except requests.RequestException as e:
        print("Error:", e)
        return False
    
"""
    name: getToolsInfo
    purpose: get tools information in json format from the tools table in the database given a drawerID.
    operation: Send a get request to the get_tools_info url along with the drawer id and the api in the header.
"""
def getToolsInfo(url, toolsDrawerID):
    params = {'drawer_id': toolsDrawerID}
    headers = {'API-Key': "Navinskey"}
    response = requests.get(url, params=params, headers = headers)
    return response.json()

"""
    name: getDrawersInfo
    purpose: Get drawer information in json format from the drawer table in the database.
    operation: Send a get request to the get_drawers_info url along with the drawer id and the header.
"""
def getDrawersInfo(url, drawerBoxNum):
    params = {'boxNum': drawerBoxNum}
    headers = {'API-Key': "Navinskey"}
    response = requests.get(url, params=params, headers = headers)
    #print(response.json())
    return response.json()

"""
    name: updateToolsInfo
    purpose: Update a tools checked out status given toolid and drawerid
    operation: Send a post request to the update_tool url along with the params and header.
"""
def updateToolsInfo(url, checkedOut, toolID, drawerID):
    params = {
        'checkedOut': checkedOut,
        'toolID': toolID,
        'drawerID': drawerID
    }
    headers = {'API-Key': "Navinskey"}
    response = requests.post(url, json=params, headers = headers)
    print(response.text)
    return response.json()
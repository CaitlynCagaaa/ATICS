""" import name(module): automatedtoolbox
    file: automatedtoolbox.py
    application: Automated tool box inventory control system 
    language: python
    computer: ROG Flow Z13 GZ301ZE_GZ301ZE
    opertaing system: windows subsystem  ubuntu
    course: CPT_S 422
    team: Null Terminators
    author: Caitlyn Powers 
    date: 4/17/24
   """
import cv2 
import numpy as np
import json
import yaml
import argparse
import drawer
from datetime import datetime, timedelta
import socket
import jsonschema 
import toolrecognition
import copy
import os
import requests
import APIFunctions_1_1
"""
    name:
    purpose:
    operation:
"""
""" 
  name: create_error_records
  purpose: Make the error events and append them to the events list.
  
"""
def create_error_records(events,errors):
    #print(events)
    #print(errors)
    for error in errors["errors"]:
        if error == None:
            continue
        #print(error)
        #print(events)
        events["events"].append({"ID": events["total"], "EventType": error["EventType"], "ToolID": error["ToolID"], "UserID": error["UserID"], "Timestamp":error['Timestamp'] ,"Location": error["Location"], "Notes":error["ToolType"]+ str(error["ToolStartX"])+ str(error["ToolStartY"])})
        #print(events["total"])
        events["total"] = events["total"]+1
        #print(events)
    updatedEvents= events
    return updatedEvents

"""
    name:print_records
    purpose: Print the events in the events list to the terminal. 
    operation:
    Event type 0 -> drawer opened
    Event type 1 -> drawer closed
    Event type 2 -> tool checked out
    Event type 3 ->tool check in
    Event type 4 -> wrong tool error
    Event type 5-> extra tool error
    Event type 6 -> runtime error

"""
def print_records(events, toolboxID):
    
    for event in events["events"]:
        if event["EventType"] == 0:
            print("Opened: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"]) + ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
        elif event["EventType"] == 1:
            print("Closed: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"] )+ ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
        elif event["EventType"] == 2: #<Tool identifier> <employee id> <time>  <location>
            print("Tool Checked Out:\n\t"  + str(event["ToolID"]) +" " +  str(event["UserID"]) + " " + str(event["Timestamp"])+ " " + str(event["Location"] ))
        elif event["EventType"] == 3:   
            print("Tool Check In:\n\t"  + str(event["ToolID"]) +" " +   str(event["UserID"]) + " " + str(event["Timestamp"])+ " " + str(event["Location"] ))  
        elif event["EventType"] == 4:  #<error type> <tool identifier> <employee id> <time> <location> 
            print("Error:\n\t"  +"Wrong tool " + str(event["ToolID"]) +" " +   str(event["UserID"]) + " " + str(event["Timestamp"])+ " " + str(event["Location"]) + " " +str(event["Notes"]))
        elif event["EventType"] == 5:   
            print("Error:\n\t"  +"Extra tool " + str(event["ToolID"]) +" " +   str(event["UserID"]) + " " + str(event["Timestamp"]) + " " + str(event["Location"]) + " " +str(event["Notes"]))
        elif event["EventType"] == 6:   
            print("Error:\n\t"  + "Runtime error " + str(event["ToolID"]) +" " +   str(event["UserID"]) + " " + str(event["Timestamp"]) + " " + str(event["Location"]) + " " +str(event["Notes"]))      

    return

"""
    name: retrieve_drawers
    purpose: Retrieve drawers that are in the given toolbox from the database.
    operation: Schema and jsonschema.validate are used to determine if it is an error message. If it is not an error message 
        a validation error should occur and it will return the drawers list.
        Use APIgatewayurl from Global_Config.yaml to call a api function that retrives drawers from the database or returns an error messsage. 
"""
def retrieve_drawers(toolBoxID):
    schema = {
        "type" : "object",
        "properties" : {
             "message" : {"type" : "string"},
        },
        "required": 
             [
                'message',
                
            ]

    }
    url =gcon.get("APIgatewayurl")+"get_drawers_info"
    drawers=APIFunctions_1_1.getDrawersInfo(url,(toolBoxID))
    try:
            jsonschema.validate(instance=drawers, schema=schema)
            
    except jsonschema.exceptions.ValidationError as err:
         return drawers
    raise RuntimeError(drawers['message'])
    

"""
    name: retrieve_tools
    purpose: Retrieve the tools that are in the given drawer from the database.
    operation: Schema and jsonschema.validate are used to determine if it is an error message. If it is not an error message 
        a validation error should occur and it will loop over tools list and add information necessary to track tools between frames, 
        and then return the tools list. Use APIgatewayurl from Global_Config.yaml to call a api function that retrives
        a list of the tools in the drawer or returns an error messsage.  
       
"""

def  retrieve_tools(drawerID):
    schema = {
        "type" : "object",
        "properties" : {
             "message" : {"type" : "string"},
        },
        "required": 
             [
                'message',
                
            ]

    }
    url =gcon.get("APIgatewayurl")+"get_tools_info"
    #print(drawerID)
    tools =APIFunctions_1_1.getToolsInfo(url,drawerID)
    try:
            jsonschema.validate(instance=tools, schema=schema)
            
    except jsonschema.exceptions.ValidationError as err:
        #print(tools)
        for tool in tools:
            tool["timestamp"] = None
            tool["error"] = 0 
        return tools
    raise RuntimeError(tools['message'])

"""
    name: update_events
    purpose: Add the events from the events list to the events table in the database.
    operation:Use APIgatewayurl from Global_Config.yaml to call a api function that adds events from the database.
"""
def update_events(events):

    url =gcon.get("APIgatewayurl")+"add_event"
    
    for event in events["events"]:
      #print(event)
      ret =  APIFunctions_1_1.addEvent(url, event["EventType"], event["ToolID"], str(event["Timestamp"]), event["Location"], event["UserID"], event["Notes"])
    return ret
"""
    name: update_tools
    purpose: Update the status of the tools in the database and add tool checkout and checkin events to the events list.
    operation:Use APIgatewayurl from Global_Config.yaml to call a api function that updates the tool status of tools in the tools table in the database.
"""
def update_tools(oldTools, newTools, events,userID,test):
      
    if newTools!=None and oldTools!=None:
        url =gcon.get("APIgatewayurl")+"update_tool"
        for oldTool,newTool in zip(oldTools,newTools):
            #print(oldTool['CheckedOut'],newTool['CheckedOut'])
            if oldTool['ToolCheckedOut']!=newTool['ToolCheckedOut']:
                if test ==False:
                    #print(newTool['ToolID'],newTool['ToolCheckedOut'])
                    APIFunctions_1_1.updateToolsInfo(url, newTool['ToolCheckedOut'], newTool['ToolID'], newTool['ToolDrawerID'])
                if newTool['ToolCheckedOut'] == True:
                 #print(events)
                 events["events"].append({"ID": events["total"], "EventType": 2, "ToolID": newTool['ToolID'], "UserID": userID, "Timestamp":newTool['timestamp'] ,"Location": newTool['ToolDrawerID'],"Notes":None})
                else:
                 events["events"].append({"ID": events["total"], "EventType": 3, "ToolID": newTool['ToolID'], "UserID": userID, "Timestamp":newTool['timestamp'] ,"Location": newTool['ToolDrawerID'],"Notes":None})
                events["total"] = events["total"]+1
    return events

"""
    name: wait_for_signal
    purpose: Wait for signal on port from hostIP that has toolbox and UserID, and get the timestamp that signal was recieved.  Also sends heartbeat signal over the connection while waiting.
    operation:  Expects a signal in the form:  {"toolbox": #, "UserID": #}. Waits for signal in infinite while loop, if singla recived,
        validates that it is correct using jsonschem.validate, if the json correct it will end the loop and close the connection.
"""           
def wait_for_signal(hostIP,port):  
    #print("enter signal")
    schema = {
        "type" : "object",
        "properties" : {
             "toolbox" : {"type" : "number"},
             "UserID" : {"type" : "number"},
        },
        "required": 
             [
                'toolbox',
                'UserID',
            ]
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostIP, port))  
    s.listen(2)
    conn, addr = s.accept()
    with conn:
        #print(f"Connected by {addr}")
        while True:
            conn.send(b"I am alive")
            data = conn.recv(1024)
            data = json.loads(data.decode('utf-8'))
            #print(data)
            if data !=None:
                try:
                 jsonschema.validate(instance=data, schema=schema)
                except jsonschema.exceptions.ValidationError as err:
                    data =None
                    continue
                startTimeStamp = datetime.now()
                break
            else:    
                continue
    
    return data, startTimeStamp, s

"""
    name:get_footage
    purpose: Retrives the footage from the given rtspStream and saves it in the file location of savedFootage 
    while waiting for the stop signal to be recived, from the reopened connection
    operation: Expects a json of {"stop" : "", bool : true}, which will cause the program to stop getting footage. The connection is 
    non-blocking so its not waiting for a conncection instead of getting footage. 
"""
def get_footage(rtspStream, savedFootage, s, startTimeStamp):
        #print("get footage")
        timestampFrame =startTimeStamp
        endTimeStamp =None
        data =None
        schema = { "type" : "object",
        "properties" : {
             "stop" : {"type" : "string"},
             "bool" : {"type" : "boolean"},
             },
             "required": 
             [
                'stop',
                'bool',
            ]
        }
        vid = cv2.VideoCapture(rtspStream) 
        if vid.isOpened():
            #print(vid.isOpened())
            frame_width = int(vid.get(3)) 
            frame_height = int(vid.get(4)) 
            size = (frame_width, frame_height) 
            result = cv2.VideoWriter(savedFootage,  
                         cv2.VideoWriter_fourcc(*'XVID'), 
                         gcon.get("fps"), size) 
            vid.set(cv2.CAP_PROP_BUFFERSIZE,70)
            vid.set(cv2.CAP_PROP_FPS, gcon.get("fps"))
            stopNotRecv = True
            while endTimeStamp ==None or timestampFrame <= endTimeStamp:
                #print(timestampFrame)
                if stopNotRecv:
                    s.setblocking(0)
                    try :
                        conn, addr = s.accept()
                        #print(conn)
                        conn.setblocking(0)
                        data = conn.recv(1024)
                        #print(data)
                        data = json.loads(data.decode('utf-8'))
                    except BlockingIOError:
                        pass
                    if data !=None:
                        try:
                            jsonschema.validate(instance=data, schema=schema)
                            #print(data)
                            if data["bool"] ==False:
                                data =None
                                continue
                        except jsonschema.exceptions.ValidationError as err:
                            data =None
                            continue
                        endTimeStamp = datetime.now()
                        #print(endTimeStamp)
                        #print(timestampFrame)
                        stopNotRecv = False
                        
                ret, frame = vid.read() 
                if ret == False:
                    continue
                timedel = (timestampFrame + timedelta(milliseconds= 1000/gcon.get("fps")))-timestampFrame 
                timestampFrame = timestampFrame +timedel
                result.write(frame)
        else:
             raise FileNotFoundError("Unable to open RTSP stream " + rtspStream )
        vid.release()
        savedVideo = cv2.VideoCapture(savedFootage) 
        s.close()
        return endTimeStamp, savedVideo
                
                    
                    
    
    
"""
    name:main
    purpose: This is the controller function for the program.
    operation: At program start up it gets the command line arguments. If -record it saves a video with debugginf information. If -test 
    it will take a video and after it is done parsing the video, it will not update the database, although it will still retrieve the tools and 
    drawers form the database for the toolbox number that is asked for by user input. After checking that the video it is processing the frames of is open
    it will retrive the drawers for the gven toolbox and then it will enter a infinite while loop that is processing the frames of the video
    to see if a drawer has been opened or closed and if tools have been checked in or out, or if thier is some kind of error in the drawer. 
    The try except statements general behavior is to catch the error from the try make a event for it print out the events or push the events to
    the database then either go back to waiting for the next signal or close the program depedning on the mode and where the error is coming from. 
    Form ore information go to the documentation. 
    
"""
def main():
 ap = argparse.ArgumentParser()
 ap.add_argument("-test", "--test",type=str, required=False,
 help="location of video for testing", default=None)
 ap.add_argument("-record", "--record", action='store_true',
 help="int value for save modified video or not", default=False)
 args = ap.parse_args()
 events = {"events":[],"total": 0}
 errors = {"errors":[], "total": 0}
 tools = None
 lastDrawer= None
 try:
    while(True):
        if args.test!=None:
            test = True
            startTimeStamp = datetime.now()
            savedVideo = cv2.VideoCapture(args.test) 
            toolBoxID = input("What is the toolbox number of  the toolbox the video was taken from?")
            data = {"toolbox": toolBoxID, "UserID": 0}
            
        else:
            test = False
            data, startTimeStamp, s = wait_for_signal(gcon.get("rfidhost"),gcon.get("rfidport")) 
            rtsp = gcon.get("RTSP")
            try:
                endTimeStamp, savedVideo = get_footage(rtsp[data["toolbox"]],"temp"+ str(data["toolbox"])+".avi", s, startTimeStamp) 
            except FileNotFoundError as err:
                s.close()
                events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "FileNotFound "+  str(err)})
                events["total"] =events["total"]+1
                update_events(events)
                events = {"events":[],"total": 0}
                errors = {"errors":[], "total": 0}
                continue
            events["events"].append({"ID": events["total"], "EventType": 7, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Logged into toolbox "+ str(data["toolbox"]) })
            events["total"] =events["total"]+1
            
        if args.record:
            #print("recording")
            os.makedirs(str(startTimeStamp.month), exist_ok = True) 
            frame_width = int(savedVideo.get(3)) 
            frame_height = int(savedVideo.get(4)) 
            size = (frame_width, frame_height) 
            recordedVideo = cv2.VideoWriter( str(startTimeStamp.month)+ "/toolbox"+ str(data["toolbox"]) +str(startTimeStamp.day)+ str(startTimeStamp.hour)+ str(startTimeStamp.second)+ str(startTimeStamp.microsecond) + "record.avi",  
            cv2.VideoWriter_fourcc(*'MJPG'), 
            gcon.get("fps"), size) 
            #print("test" +str(timestampStart) + ".avi")
        if savedVideo.isOpened():
            #print(args.test)
            ret, frame = savedVideo.read()
            #print(ret)
            try:
                #print("check")
                drawerList = retrieve_drawers(data["toolbox"])
                #print("checkk")
            except Exception as err :
                events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Closing program, Error in retriving drawers: " +str(err)})
                events["total"] =events["total"]+1
                if test:
                    print_records(events,data["toolbox"])
                else:
                    update_events(events)   
                exit(0)
            #print(errors)
            timestampFrame = startTimeStamp
            
            try:
                while(ret):
                    #print(ret)
                    modFrame, currentDrawer, drawerSize = drawer.find_drawer(frame, drawerList,args.record)
                    if lastDrawer==None and currentDrawer!=None:
                    #print(currentDrawer)
                        events["events"].append({"ID": events["total"], "EventType": 0, "ToolID": None, "UserID": data["UserID"], "Timestamp":timestampFrame ,"Location": currentDrawer["DrawerID"], "Notes":None})
                        events["total"] =events["total"]+1
                        try:
                            #print(currentDrawer["DrawerID"])
                            tools = retrieve_tools(currentDrawer["DrawerID"])
                        except Exception as err :
                            events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Closing program, Error in retriving tools: " +str(err)})
                            events["total"] =events["total"]+1
                            if test:
                                print_records(events,data["toolbox"])
                                
                            else:
                                update_events(events)   
                                
                            exit(0)
                        response = requests.get(gcon.get("webserverurl")+currentDrawer["DrawerYAML"], allow_redirects=True)
                        content = response.content.decode("utf-8")
                        drawerConfig =yaml.safe_load(content)
                        oldtools = copy.deepcopy(tools)
                        newtools = copy.deepcopy(tools)
                    if lastDrawer!=None and currentDrawer!=lastDrawer:
                        create_error_records(events,errors)
                        update_tools(oldtools,newtools, events,data["UserID"],test)
                        events["events"].append({"ID": events["total"], "EventType": 1, "ToolID": None, "UserID": data["UserID"], "Timestamp":timestampFrame ,"Location": lastDrawer["DrawerID"],"Notes":None})
                        events["total"] =events["total"]+1
                        if test ==True:
                            
                            print_records(events,data["toolbox"])
                        else:
                            
                            update_events(events)
                        events = {"events":[],"total": events["total"]}
                        oldtools = None
                        newtools =None
                        tools = None
                        errors = {"errors":[],"total": errors["total"]}
                    if currentDrawer!=None and drawerSize[2]>0:
                        response = requests.get(gcon.get("webserverurl")+gcon.get("onnxfile"), allow_redirects=True)
                        content = response.content
                        net =  cv2.dnn.readNetFromONNX(content) 
                        #print(oldtools)
                        newtools, errors= toolrecognition.update_tools_for_frames(frame, modFrame, newtools, errors, drawerSize,timestampFrame,currentDrawer,drawerConfig,net, data["UserID"],args.record)
                        #print(oldtools)
                    if args.record==1:
                        #print("write")
                        recordedVideo.write(modFrame)
                    ret, frame = savedVideo.read() 
                    timedel = (timestampFrame + timedelta(milliseconds= 1000/gcon.get("fps")))-timestampFrame 
                    timestampFrame = timestampFrame +timedel
                    #print(timestampFrame)
                    lastDrawer = currentDrawer

                savedVideo.release()
                
                if args.record:
                   recordedVideo.release() 
                create_error_records(events,errors)
                #print(events)
                update_tools(oldtools,newtools, events,data["UserID"], test)
                if test ==True:
                    print_records(events,data["toolbox"])
                    exit(0)

                else:
                    os.remove("temp"+ str(data["toolbox"])+".avi")
                    events["events"].append({"ID": events["total"], "EventType": 8, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Logged out of toolbox "+ str(data["toolbox"]) })
                    update_events(events)
                    events = {"events":[],"total": 0}
                    errors = {"errors":[], "total": 0}
            except Exception as err :
                events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": " Error in processing frame: " +str(err)})
                events["total"] =events["total"]+1
                create_error_records(events,errors)
                #print(events)
                if oldtools !=None and newtools!=None:
                    update_tools(oldtools,newtools, events,data["UserID"], test)
                if test:
                    print_records(events,data["toolbox"])
                    exit(0)
                else:
                    update_events(events)   
                    events = {"events":[],"total": 0}
                    errors = {"errors":[], "total": 0}
                    continue
        else:
            events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "failed to open video "})
            events["total"] =events["total"]+1
            if test :
                print_records(events,data["toolbox"])
                exit(0)
            else:
                update_events(events)   
                events = {"events":[],"total": 0}
                errors = {"errors":[], "total": 0}
                continue  
 except Exception as err :
                    events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": None, "Timestamp":datetime.now() ,"Location": None,"Notes": "Closing program: " +str(err)})
                    events["total"] =events["total"]+1
                    if test:
                        print_records(events,data["toolbox"])
                        exit(0)
                    else:
                        update_events(events)   
                        exit(0)

config =open("Global_Config.yaml", "r") 
gcon =yaml.safe_load(config)
if __name__ == "__main__":
    main()
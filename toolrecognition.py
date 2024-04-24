""" import name(module): toolrecognition
    file: toolrecognition.py
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
from matplotlib import pyplot as plt
import drawer
import yaml
from shapely.geometry import Polygon
import copy
import imutils
gcon =open("Global_Config.yaml", "r")
gcon =yaml.safe_load(gcon)
"""
    name:update_tools_for_frames
    purpose:Contoller function for tool recogntion, basically is checking whether tools are checked in or out, and if thier are
    any errors in the drawer, returns updated events and errors list.
    operation:Segment drawer to find objects in drawer as countours , loop over list of tools checking if tool is visible, removing 
        countours from the tool from the contours list, crop frame to be the current tools location, chekc tool
        status , note tools status and the time after done looping check countours list for extra tools.
"""
def update_tools_for_frames(frame, modframe, tools, errors, drawerLocation,timestamp,drawer,configuration,classifier,userID, record):
    global con 
    global onnx
    onnx = classifier
    
    con = configuration
    countours =drawer_segment(frame, drawerLocation)
    
    updatedTools = copy.deepcopy(tools)
    #print(" in tool")
    for tool in updatedTools:
        #print(tool)
        toolLocation, visible= is_visible(tool,drawerLocation,drawer,gcon.get("buffer"))
        if visible:
            #print(visible)
            countours =remove_from_contours(countours, toolLocation,drawerLocation)
            #print("1")
            crop = frame[toolLocation[1]-gcon.get("buffery"):toolLocation[3]+toolLocation[1]+2*gcon.get("buffery"), toolLocation[0]-gcon.get("bufferx"):toolLocation[2]+2*gcon.get("bufferx")+toolLocation[0]].copy()
            #print("2")
            if crop.shape[0] >0 and crop.shape[1] >0: # add error for confusing  symbols and/or difference in input
                #print("3")
                status = is_checked_out(crop,modframe,tool,toolLocation,gcon.get("thresholdtool"),gcon.get("thresholdsymbol"),gcon.get("degrees"),gcon.get("degreesdiv"),errors,timestamp,drawer["DrawerID"],con.get("symbolbuffer"),userID,record)
                #print(errors)
                #print("4")
                if (tool['ToolCheckedOut'] == True and status == 1) or  (tool['ToolCheckedOut'] == False and status == 0):
                    tool['ToolCheckedOut'] = not tool['ToolCheckedOut']
                    tool['error'] = 0
                    tool["timestamp"] = timestamp
                elif status == -1:
                    tool['error'] = 1
                #print("5")
    updatedErrors = check_extra_tools(updatedTools,countours, errors, timestamp, drawer,drawerLocation,frame,modframe, onnx,userID, record)
    #print("exiting")
    #print(updatedTools)
    return updatedTools, updatedErrors
"""
    name:drawer_segment
    purpose:Finds the objects in the drawer.
    operation:Uses same drawer segmentation method as additionnalscript. If segment is -1 return empty list and program
        will not report any extra tool errors.
"""
def drawer_segment(frame, drawerLocation):
    if(con.get("segment")) == -1:
        return []
    crop = frame[drawerLocation[1]:drawerLocation[3]+drawerLocation[1], drawerLocation[0]:drawerLocation[2]+drawerLocation[0]].copy()
    gray = cv2.cvtColor(crop,con.get('grayscale'))
    gray=cv2.medianBlur(gray,con.get('blur'))
    #cv2.imshow("blurring", gray)
    ret, thresh = cv2.threshold(gray,con.get('minThreshValue'),255,con.get('threshType') )
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = con.get("increasewhite"))
    sure_bg = cv2.dilate(opening,kernel,iterations=con.get("decreaseblack"))
    contours, hierarchy= cv2.findContours(sure_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
"""
    name:is_visible
    purpose:Checks if tool is visible in the drawer.
    
"""
def is_visible(tool,drawerLocation,drawer,buffer):
    toolLocation =calculate_location(tool,drawer,drawerLocation)
    #print(toolLocation[3]*toolLocation[2],tool["W"]*tool["H"]*buffer,buffer)
    if toolLocation[3]*toolLocation[2]>=tool["ToolPixelWidth"]*tool["ToolPixelHeight"]*buffer:
        visible = True
    else:
        visible =False
    return toolLocation, visible
"""
    name:calculate_location
    purpose: Calculates location of tool or error.

"""
def calculate_location(tool,drawer,drawerLocation):
    # i can't think it through right now 
    xDiff = drawer["DrawerPixelWidth"]-drawerLocation[2]
    yDiff = drawer["DrawerPixelHeight"]-drawerLocation[3]
    #print(xDiff, yDiff, drawer["X"]+drawerLocation[2],tool['X']+tool["W"])
    #print("t")
    diff = tool["ToolStartX"] - drawerLocation[0]
    if diff<=xDiff:#something is wrong here 
        toolLocation = (drawerLocation[0],tool["ToolStartY"]-yDiff, tool["ToolPixelWidth"]-xDiff+diff,tool["ToolPixelHeight"])
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
    else:
         #print("v")
         toolLocation = (tool["ToolStartX"]-xDiff,tool["ToolStartY"]-yDiff, tool["ToolPixelWidth"],tool["ToolPixelHeight"])
         #print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    #print(toolSize)
    return toolLocation
"""
    name:remove_from_contours
    purpose: Remove the countors that are in the same area as the tool from the list.
    operation: Loop over countours and append countour ot new list if it is not in thte tools area. Use shapely library
        to see if the contours are intersecting,inside, or encompass the tool area. 
"""
def remove_from_contours(contours, toolLocation,drawerLocation):
    tool  = Polygon([(toolLocation[0] -10,toolLocation[1]-10), (toolLocation[0] -10,toolLocation[1]+toolLocation[3]+10),(toolLocation[0]+toolLocation[2]+10,toolLocation[1]+toolLocation[3]+10), (toolLocation[0]+toolLocation[2]+10,toolLocation[1]-10)])
    contourss =[]
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cont  = Polygon([(x+drawerLocation[0],y+drawerLocation[1]), (x+drawerLocation[0],y+h+drawerLocation[1]),(x+w+drawerLocation[0],y+h+drawerLocation[1]), (x+w+drawerLocation[0],y+drawerLocation[1])])
        if tool.buffer(1).intersects(cont) or tool.buffer(1).contains(cont) or cont.buffer(1).contains(tool):
            continue
        contourss.append(contour) 
    return contourss
"""
    name:check_extra_tools
    purpose: Checks for extra tools in the drawer.
    operation: Loop over contours, to see if they are an actual tool or if the contour is something else. Then in the same loop
        loop over errors to filter out repeat errors.
"""
def check_extra_tools(tools,contours, errors, timeStamp, drawer,drawerLocation,frame,modFrame, classifier,userID, record) :
    #print(errors)
    updatedErrors = {"errors":[], "total": errors["total"]}
    crop = frame[drawerLocation[1]:drawerLocation[3]+drawerLocation[1], drawerLocation[0]:drawerLocation[2]+drawerLocation[0]].copy()
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w > con.get("minWidth") and h > con.get("minHeight"):
            image = crop[y:y+h,x:x+w,].copy()
           
            cont  = Polygon([(x+drawerLocation[0],y+drawerLocation[1]), (x+drawerLocation[0],y+h+drawerLocation[1]),(x+w+drawerLocation[0],y+h+drawerLocation[1]), (x+w+drawerLocation[0],y+drawerLocation[1])])
            toolType = classifier_check(classifier, image) 
            if toolType in gcon['onnxtools']:
                
                for error in errors["errors"]:
                    err  = Polygon([(error['ToolStartX'],error['ToolStartY']), (error['ToolStartX'],error['ToolPixelWidth']),(error['ToolPixelWidth'],error['ToolPixelHeight']), (error['ToolPixelWidth'],error['ToolStartY'])])
                    check = 0
                    for error2 in updatedErrors["errors"]:
                        err2  = Polygon([(error2['ToolStartX'],error2['ToolStartY']), (error2['ToolStartX'],error2['ToolPixelHeight']),(error2['ToolPixelWidth'],error2['ToolPixelHeight']), (error2['ToolPixelWidth'],error2['ToolStartY'])])
                        if (err.buffer(1).intersects(err2) or err.buffer(1).contains(err2) or err2.buffer(1).contains(err)):
                            check =1
                            errors['errors'].remove(error)
                            break
                            
                    if(err.buffer(1).intersects(cont) or err.buffer(1).contains(cont) or cont.buffer(1).contains(err)) and check !=1:
                        updatedErrors["errors"].append(error)
                        errors['errors'].remove(error)
                        text = "error"+toolType + str(error["ID"])
                        if record:
                            modFrame = cv2.rectangle(modFrame, (x+drawerLocation[0], y+drawerLocation[1] ), (x + w+drawerLocation[0], y+h+drawerLocation[1] ), (255, 0,0), 3)
                            (wt, ht), _ = cv2.getTextSize(
                            text, cv2.FONT_HERSHEY_SIMPLEX, .005*h, 2)
                            modFrame = cv2.rectangle(modFrame, (x+drawerLocation[0], y+drawerLocation[1] - ht), (x+drawerLocation[0] + wt, y+drawerLocation[1]), (255, 0,0), 3)
                            cv2.putText(modFrame, text, (x+drawerLocation[0], y+drawerLocation[1]),cv2.FONT_HERSHEY_SIMPLEX,.005*h, (36,255,12), 2)
                            break 
                        
                    elif check!=1:
                        errors["errors"].append({"ID": errors["total"], "ToolType": toolType,"EventType": 5, "ToolID":None,  "UserID": userID, "Timestamp":timeStamp ,"Location": drawer["DrawerID"], "ToolStartX": x+drawerLocation[0], "ToolStartY": y+drawerLocation[1], "ToolPixelWidth": x+w+drawerLocation[0], "ToolPixelHeight": y+h+drawerLocation[1]})  
                        errors["total"] =errors["total"] +1
                        updatedErrors["total"] =errors["total"]          
    for error in  errors["errors"]:
       location, visible = is_visible(error,drawerLocation,drawer, gcon.get("buffer"))
       if not visible:
            updatedErrors["errors"].append(error)
       elif error["ToolID"]!=None and [tool['error'] for tool in tools if tool['ToolID']==error["ToolID"]] ==1:
           updatedErrors["errors"].append(error)

    return updatedErrors
"""
    name:is_checked_out
    purpose: Determine if tool is checked in or out.
    operation: Uses template matching to determine if tool is checked in or out, if it is not checked out it checks for
        wrong tool by looking ofr the tool symbol and determining the type of tool. If it looksl ike a nontool it increases the
        similarity of the tool checked out and tests if it is tool checked out again. 
"""
def is_checked_out(image, modFrame, tool, toolLocation, threshold,thresholdSymbol, degrees, degreesDiv, errors, timeStamp,drawerID,symbolBuffer,userID,record):
    #print(tool)
    picno = imutils.url_to_image(gcon.get("webserverurl")+tool["ToolPictureWithoutPath"])
    picfull = imutils.url_to_image(gcon.get("webserverurl")+tool["ToolPictureWithPath"])
    notEntireVisible = False
    if(tool['ToolPixelWidth']!=toolLocation[2]):
        notEntireVisible = True
        tempY = 0
        tempH = toolLocation[3] 
        tempW = toolLocation[2] 
        tempX = tool['ToolPixelWidth']-toolLocation[2]
        if  tempX <0:  
          tempX= toolLocation[2]-tool['ToolPixelWidth']
        
        #print(picno.shape[0],picno.shape[1],picno.shape[2])
        #print(picfull.shape[0],picfull.shape[1],picfull.shape[2])
        picfull= picfull[tempY:tempY+tempH, tempX:tempX+tempW]
        #print(tempX+tempW)
        #print("tool",tool["ID"],tempY,tempH,tempW,tempX)
        picno = picno[tempY:tempY+tempH, tempX:tempX+tempW]
    #print(picno.shape[0],picno.shape[1],picno.shape[2])
    #print(picfull.shape[0],picfull.shape[1],picfull.shape[2])
    #print(image.shape[0],image.shape[1],image.shape[2])
    
    
    foundNoTool,placeNoTool,similarityNoTool = drawer.draw_temp(picno,image, modFrame, image.shape[0], image.shape[1],(256,0,256), threshold,0,degrees,degreesDiv)
    #if foundNoTool ==False:
    #    similarityNoTool =0
    #cv2.imshow("wait.jpg",picfull)
    
    #cv2.waitKey(0)
    foundTool,placeTool,similarityTool = drawer.draw_temp(picfull,image, modFrame, image.shape[0], image.shape[1],(0,256,256), threshold,0,degrees,degreesDiv)
    
    #if foundTool ==False:
    #    similarityTool =0   
    if similarityTool >= similarityNoTool or (foundNoTool==False and foundTool==False):
        toolType = classifier_check(onnx,image)
        #cv2.imshow("check",picfull)
        #print(similarityTool, similarityNoTool)
        place = placeTool
        if (notEntireVisible or tool["ToolClassifierType"] ==None or toolType == tool["ToolType"] or similarityTool >=gcon.get("thresholdignoreonnx")) and symbol_check(symbolBuffer,tool, toolLocation,image,modFrame,thresholdSymbol,degrees,degreesDiv,record) and foundTool==True:
            text = tool["ToolName"] + " " +  str(round(similarityTool,2)) +'%' 
            checkedOut =1
            color = (256,0,256)
        else:
            if toolType in gcon['onnxnontools'] and similarityNoTool+gcon.get("thresholdadd") > similarityTool:
                        text = tool["ToolName"] +" " +"checkout"+ " " +  str(round(similarityNoTool,2)) +'%' + " " + toolType
                        checkedOut = 0
                        place = placeNoTool
                        color =(0,256,256)
            else:
                text = "error" + str(tool["ToolID"]) +" " +toolType+  str(round(similarityTool,2)) +'%' + " " +str(round(similarityNoTool,2))+'%'
                if tool["error"]!= 1:
                    errors["errors"].append({"ID": errors["total"] , "ToolType": toolType,"EventType": 4, "ToolID": tool["ToolID"], "UserID": userID, "Timestamp":timeStamp ,"Location": drawerID, "ToolStartX":toolLocation[0], "ToolStartY": toolLocation[1], "ToolPixelWidth": toolLocation[2], "ToolPixelHeight": toolLocation[3]})   
                    errors["total"] = errors["total"]+1
                checkedOut = -1
                color = (0,0,0)
            place = ((gcon.get("bufferx"),gcon.get("buffery")),(toolLocation[2]+3*gcon.get("bufferx"),toolLocation[3]+3*gcon.get("buffery")))
    else:
        text = tool["ToolName"] +" " +"checkout"+ " " +  str(round(similarityNoTool,2)) +'%'
        checkedOut = 0
        place = placeNoTool
        color =(0,256,256)
    if record ==1:
        #print(toolLocation[0],place[0][0])
        (wt, ht), _ = cv2.getTextSize(
         text, cv2.FONT_HERSHEY_SIMPLEX, .004*toolLocation[2], 1)
  
        modFrame = cv2.rectangle(modFrame, (toolLocation[0]+place[0][0]-gcon.get("bufferx"), toolLocation[1]+place[0][1] - ht-2*gcon.get("buffery")), (toolLocation[0]+place[0][0] + wt, toolLocation[1]+place[0][1]), (255, 0,0), 1)
        cv2.putText(modFrame, text, (toolLocation[0]+place[0][0]-gcon.get("bufferx"), toolLocation[1]+place[0][1]-2*gcon.get("buffery")),cv2.FONT_HERSHEY_SIMPLEX,.004*toolLocation[2], (36,255,12), 1)
        cv2.rectangle(modFrame, (toolLocation[0]+place[0][0]-gcon.get("bufferx"),toolLocation[1]+place[0][1]-gcon.get("buffery")), 
                      (toolLocation[0] +place[0][0]+ toolLocation[2],toolLocation[1] +place[0][1]+ toolLocation[3]), color, 2 )
        
    #print(errors) 
    return checkedOut
"""
    name:classifier_check
    purpose: Determines if the tool is the right tool type. 
    operation: Uses the onnx file to check what tool type it is.
"""
def classifier_check(classifier, image):
    normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
    classifier.setInput(cv2.dnn.blobFromImage(normalized_image, size=(224, 224), swapRB=False, crop=True))
    detection = classifier.forward()
    #print(detection)
    answer = np.absolute(detection)
    #print(answer)
    maximum = np.max(answer)
    #print(maximum)
    answer = np.where(answer == maximum)[1]
    labels= gcon.get("onnxlabels")
    #print(labels)
    #print(answer)
    index = answer.item()
    #print(labels[index])
    return labels[index]
"""
    name:symbol_check
    purpose: Determine if symbol is on the tool.
    operation: If no tool symbol is availble or the tool symbol shouldn't be visible by this point it returns true. 
"""
def symbol_check(symbolBuffer,tool, toolLocation, image, modFrame, threshold, degrees, degreesDiv, record):
    
    if tool["ToolSymbolAvailable"] ==True and toolLocation[1]*toolLocation[0]>=tool["ToolPixelWidth"]*tool["ToolPixelHeight"]*symbolBuffer:
        template = imutils.url_to_image(gcon.get("webserverurl")+tool["ToolSymbolPath"])
        #cv2.imshow("mark",template)
        found,place,_ = drawer.draw_temp(template,image, modFrame, image.shape[0], image.shape[1],(256,256,256), threshold,0,degrees,degreesDiv)
        if record ==1 and found ==True:
            cv2.rectangle(modFrame, (toolLocation[0]+place[0][0]-gcon.get("bufferx"),toolLocation[1]+place[0][1]-2*gcon.get("buffery")), 
                      (toolLocation[0] +place[0][0]+ template.shape[0],toolLocation[1] +place[0][1]+ template.shape[1]), (256,256,256), 3 )  
    else:
        found =True
    return found       
    

                


    


    
           
          
        
        


import json
import yaml
import cv2
import os
import argparse
import numpy as np
from matplotlib import pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("parse",type=str,
help="file location of image to threshod and grab data from", default=None)
ap.add_argument("dontParse",type=str,
help="only grab templates from this picture", default=None)
ap.add_argument("-confName", "--confName",type=str, required=False,
    help="file location of the configuration file default value is conf.yaml", default='conf.yaml')
args = ap.parse_args()
try:
    config =open(args.confName, "r") 
except:
     print('Could not open' + args.confName + "double check file location and permissions")
con =yaml.safe_load(config)
# Load the image
try :
 image = cv2.imread(r""+args.parse,cv2.IMREAD_UNCHANGED)
except: 
    print('Could not open' + args.parse + "double check file location and permissions")

try:
    image2 = cv2.imread(r""+args.dontParse,cv2.IMREAD_UNCHANGED)
except: 
    print('Could not open' + args.dontParse + "double check file location and permissions")
result = image.copy()
result2 = image2.copy()

os.makedirs("drawer", exist_ok = True) 


#normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
#cv2.imshow("norm", normalized_image)
gray = cv2.cvtColor(image,con.get('grayscale'))
gray=cv2.medianBlur(gray,con.get('blur'))
cv2.imshow("blurring", gray)
#normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)

ret, thresh = cv2.threshold(gray,con.get('minThreshValue'),255,con.get('threshType') )
#thresh = cv2.bitwise_not(thresh) 
cv2.imwrite("Thresholded.jpg", thresh)

kernel = np.ones((3,3),np.uint8)
cv2.imshow("kernel", kernel)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = con.get("increasewhite"))
cv2.imshow("decrease white", opening)
# sure background area

sure_bg = cv2.dilate(opening,kernel,iterations=con.get("decreaseblack"))
cv2.imshow("increase white", sure_bg)
# Finding sure foreground area
#dist_transform = cv2.distanceTransform(thresh,cv2.DIST_L1,0)
#cv2.imshow("I", dist_transform)
contours, hierarchy= cv2.findContours(sure_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#print(contours)
#print(hierarchy)
res_cpy = result.copy()
cv2.drawContours(image=res_cpy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
print(hierarchy)
#cv2.imshow("contours", image)
#contours = contours[0] if len(contours) == 2 else contours[1]
check = 1
j=0
with open("drawer"+'/tools.json', 'w') as f:
 f.write('{"Tools": [')
 for i in range(len(contours)):
    #print(i)
    if hierarchy[0,i,3] ==-1 :
          x,y,w,h = cv2.boundingRect(contours[i])
          if w > con.get('minWidth') and h >con.get('minHeight'):
            check = 0
            x,y,w,h = cv2.boundingRect(contours[i])
            if x-con.get('bufferX')> 0:
                x = x -con.get('bufferX')
            if y-con.get('bufferY')> 0:
                y = y - con.get('bufferY')
            if w+con.get('bufferX')<image.shape[0]:
                w = w +2*con.get('bufferX')
            if h+con.get('bufferY')< image.shape[1]:
                h = h + 2*con.get('bufferY')
            print("1")
            with open("drawer"+'/drawer.json', 'w') as d:
             
             #make bounding pictures
             cv2.rectangle(result, (x, y), (x+w, y+h), (255,255, 255), 3)
             (wt, ht), _ = cv2.getTextSize(
          'drawer ' + str(0)+'%', cv2.FONT_HERSHEY_SIMPLEX, .003*w, 5)
             cv2.rectangle(result2, (x, y), (x+w, y+h), (255,255, 255), 3)
  
             result = cv2.rectangle(result, (x, y - ht), (x + wt, y), (255, 0,0), 3)
             cv2.putText(result, 'drawer ' + str(0)+'%', (x, y),cv2.FONT_HERSHEY_SIMPLEX,.003*w, (36,255,12), 1)
             result2 = cv2.rectangle(result2, (x, y - ht), (x + wt, y), (255, 0,0), 3)
             cv2.putText(result2, 'drawer ' + str(0)+'%', (x, y),cv2.FONT_HERSHEY_SIMPLEX,.003*w, (36,255,12), 1)
             
    #print("x,y,w,h:",x,y,w,h)
        #print(image.shape) 
             cropped_image = image[y:y+h, x:x+w].copy()
             cropped_image2 = image2[y:y+h, x:x+w].copy()
             if con.get('segment')==0 :
              dump = [{'ID': 0, 'DrawerNum': 0 , 'BoxNum': 0,'X': x, 'Y' :y ,'W' :w , 'H' : h, 'picall':"drawer"+'/drawer_1', 'picno':"drawer"+'/drawer_2', 'drawersymbols':[{'ID': 0,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' }, {'ID': 1,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' },{'ID': 2,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' }] }]
             elif  con.get('segment')==1 :
              dump = [{'ID': 0, 'DrawerNum': 0 , 'BoxNum': 0,'X': x, 'Y' :y ,'W' :w , 'H' : h, 'picall':"drawer"+'/drawer_2', 'picno':"drawer"+'/drawer_1', 'drawersymbols':[{'ID': 0,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' }, {'ID': 1,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' },{'ID': 2,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' }] }]
             else:
                print("Plese set segment to 0 or 1 according to which picture is being thresholded in the config file for the use of this script ")
                exit()
             json.dump(dump,d)
                
        #print(cropped_image)
             cv2.imshow( "cropped",cropped_image )
             cv2.imwrite("drawer"+'/drawer_1.jpg',cropped_image)
             cv2.imwrite("drawer"+'/drawer_2.jpg',cropped_image2)
            
    else:
        print("2")
        x,y,w,h = cv2.boundingRect(contours[i])
        if w > con.get('minWidth') and h >con.get('minHeight'):
            if x-con.get('bufferX')> 0:
                x = x -con.get('bufferX')
            if y-con.get('bufferY')> 0:
                y = y - con.get('bufferY')
            if w+con.get('bufferX')<image.shape[0]:
                w = w +2*con.get('bufferX')
            if h+con.get('bufferY')< image.shape[1]:
                h = h + 2*con.get('bufferY')
            one = "/tool_" + str(j) + "_1.jpg"
            two = "/tool_" + str(j) + "_2.jpg"

            #make biunding boxes
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.rectangle(result2, (x, y), (x+w, y+h), (0, 255, 0), 3)
            (wt, ht), _ = cv2.getTextSize(
        'toolname ' + str(0)+'%', cv2.FONT_HERSHEY_SIMPLEX, .003*w, 1)
            result = cv2.rectangle(result, (x, y - ht), (x + wt, y), (255, 0, 0), 3)
            result2 = cv2.rectangle(result2, (x, y - ht), (x + wt, y), (255, 0, 0), 3)
            cv2.putText(result, one + str(0)+'%', (x, y),cv2.FONT_HERSHEY_SIMPLEX,.003*w, (36,255,12), 1)
            cv2.putText(result2, two + str(0)+'%', (x, y),cv2.FONT_HERSHEY_SIMPLEX,.003*w, (36,255,12), 1)
            
    #print("x,y,w,h:",x,y,w,h)
            
        #print(image.shape) 
            cropped_image = image[y:y+h, x:x+w].copy()
            cropped_image2 = image2[y:y+h, x:x+w].copy()
            
            if con.get('segment')==0 :
                    dump = {'ID': j, 'Name': 'img' + str(i),'ToolType': None, 'ClassifierThinks': None, 'Location': 0, 'Who': None, 'IDAvail': False,'IDMark': None , 'CheckedOut': False,'X': x, 'Y' :y ,'W' :w , 'H' : h, 'picfull': "drawer"+one, 'picnull': "drawer"+two, 'Manual':False}
            elif con.get('segment')==1 :
                    dump = {'ID': j, 'Name': 'img' + str(i),'ToolType': None, 'ClassifierThinks': None, 'Location': 0, 'Who': None, 'IDAvail': False,'IDMark': None , 'CheckedOut': False,'X': x, 'Y' :y ,'W' :w , 'H' : h, 'picfull': "drawer"+two, 'picnull': "drawer"+one, 'Manual':False}
            json.dump(dump,f)
            f.write(',\n')
        #print(cropped_image)
            cv2.imshow( "cropped",cropped_image )
            cv2.imwrite("drawer"+one,cropped_image)
            cv2.imwrite("drawer"+two,cropped_image2)
            j=j+1
 f.write("]}")
    

cv2.imwrite("drawer"+'/imgbounded1.jpg',result)
cv2.imwrite("drawer"+'/imgbounded2.jpg',result2)
#result =cv2.resize(result,None,.75,.75)
cv2.imshow("bounding boxes", result)
# Wait for the user to press a key
cv2.waitKey(0)
cv2.destroyAllWindows()
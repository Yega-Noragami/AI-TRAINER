#import necessary libraries 
import cv2 
import mediapipe as mp 
import math 
import time 

'''
Now this module can be used to extract datapoints easily 
Phase -1 done


Phase -2 -> implement tracking for workout 

Phase-3 ->  
'''

class poseDetector():

    def __init__(self , mode = False , upBody = False , smooth = True , detectionCon= 0.5 , trackCon=0.5):
        '''
        AllParameters 

        static_image_mode = False 
        upper_body_only = False ,
        smooth_landmarks = True,
        min_detection_confidence = 0.5, 
        min_tracking_confidence = 0.5
        '''

        # new object will have its variables (OOPS Concept)
        self.mode = mode 
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon


        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode ,self.upBody , self.smooth , self.detectionCon , self.trackCon )

    # draw -> display on image or not 
    def findPose(self , img , draw = True):

        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.pose.process(imgRGB)

            #connects the joints  joints only if condition passed (only if landmark is detected)
            if self.results.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img , self.results.pose_landmarks , self.mpPose.POSE_CONNECTIONS)

            return img

        except:
            return 0


    # returns list of joint id alone with (x, y) coordinates
    def findPosition(self , img , draw= True):
        '''
        You can get the joint ID and x,y coordinates . Refer to meidapipe for respective joint id
        you can get (x,y) joint coordinate by ( lmlist[joint_id][1] , lmlist[joint_id][2] )
        '''
        #check if results are available , only then use for loop iteration
        self.lmList=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                #Get the height , width amd chancel of the landmark 
                h, w, c = img.shape
                #to get pixel value for x and y
                cx = int(lm.x*w)
                cy = int(lm.y*h)
                self.lmList.append([id , cx , cy])
                if draw:
                    '''
                    parametrs 
                    image , coordinate , radius size , color ,  Filled or no Filled 
                    '''
                    cv2.circle (img, (cx, cy), 5 , (255,0,0), cv2.FILLED)       

        return self.lmList 

    #return the angle between any 3 points passesd
    def findAngle(self , img , p1 , p2 , p3 , draw = True):

        # Get landmarks 
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        

        #Calculate the Angle 
        angle = math.degrees(math.atan2(y3-y2 , x3-x2) - math.atan2(y1-y2 , x1-x2))


        if angle <0 : 
            angle*= -1
        else : 
            angle = (360-angle)

        # To highlight the power points you are focussing on!
        if draw:
            #separate the points line by white color 
            cv2.line(img , (x1 , y1) , (x2 , y2) , (255 , 255 , 25), 3)
            cv2.line(img , (x3 , y3) , (x2 , y2) , (255 , 255 , 25), 3)
            #separate the joint by color 
            cv2.circle (img, (x1, y1), 5 , (0 , 0 , 255), cv2.FILLED)  
            cv2.circle (img, (x1, y1), 10 , (0 , 0 , 255), 2)  
            cv2.circle (img, (x2, y2), 5 , (0 , 0 , 255), cv2.FILLED) 
            cv2.circle (img, (x2, y2), 10 , (0 , 0 , 255), 2)   
            cv2.circle (img, (x3, y3), 5 , (0 , 0 , 255), cv2.FILLED)  
            cv2.circle (img, (x3, y3), 10 , (0 , 0 , 255), 2)  

            # show angle on the image 
            point = (x2 + 10, y2+ 50)

            '''
            paramters : image = cv2.putText(image, text, org, font, fontScale,
                  color, thickness, cv2.LINE_AA, True) 
            '''
            cv2.putText(img , str(int(angle)) ,point , cv2.FONT_HERSHEY_PLAIN, 2 , (255 , 0 , 0) , 2 ,cv2.LINE_AA, False )
        
        return angle

def main():

    # IMPORT VIDEO 
    cap = cv2.VideoCapture('PoseVideos/1.mp4')

    # # WEBCAM VERSION  
    # cap = cv2.VideoCapture(0)


    pTime=0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)

        # Will thow an error if the respective joint is not detected in the video stream. 
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList)



        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime =cTime

        cv2.putText(img, str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3, (255,0,0),3)   
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        cv2.destroyAllWindows()


if __name__=="__main__":
    main()

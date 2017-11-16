
import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np
#for importing files
import glob, os
import matplotlib.pyplot as plt



#Library for hull calculation
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from matplotlib.path import Path
from scipy.spatial import distance


# ## Helper Methods
def SecsToGameTime(time):
    mins=(int(time)/60)
    secs=int(time)%60
    print (str(mins)+":"+str(secs))

def GameTimetoSeconds(time):
    mins, secs = time.split(":")
    timeSecs = int(mins)*60+int(secs)
    print(timeSecs)
    return timeSecs


# #### Hull Calculation Helper Method
def getHull(moments, teamID):
    points = []
    
    if(moments[5][1][0] == teamID):
        for positions in moments[5][1:6]:
            #print positions
            points.append([positions[2],positions[3]])
        print(points)
    else:
        for positions in moments[5][6:11]:
            #print positions
            points.append([positions[2],positions[3]])
        print(points)
    
    np_points = np.asarray(points)
    np_points
    hull = ConvexHull(np_points)
    
    return hull,np_points

def distFromCentroid(hull, x,y):
        cx = np.mean(hull.points[hull.vertices,0])
        cy = np.mean(hull.points[hull.vertices,1])
        return ((x-cx)^2+(y-cy)^2)^.5

def isInHull(hull,np_points,x,y):
    #point in hull?
    hull_path = Path( np_points[hull.vertices] )
    isInPath = hull_path.contains_point((x,y))
    return (isInPath == True)


# ### Given the game time (12:00) and eventNumber from the Play-by-play data for a recorded event, this method returns the correct eventNumber from the SportsVU data since they actually dont matchup.  This method converts the gametime into seconds (720s = 12:00) which is formatted in SportsVU.  It traverses up and down events until the gametime is within a selected eventNumber.
def findCorrectMomentData(rawSportVUData, quarterPBP, gametimePBP, approxEventNumPBP):
    print("Finding correctSportVU eventNum gameid:"+rawSportVUData['gameid'])

    found = False;
    moments = None
    #convert gametimePBP (12:00) to seconds (720)
    gameInSeconds = GameTimetoSeconds(gametimePBP)
    while (found == False):
        print("Currently checking eventNumPBP: "+str(approxEventNumPBP))
        moments = MomentsfromEventNum(rawSportVUData, approxEventNumPBP)
        
        if len(moments) == 0:
            return None
        
        quarterSportVU = int(moments[0][0])
        print("PBP quareter:"+str(quarterPBP)+"quartersportVU :"+str(quarterSportVU))
        print("PBP gameclock:"+str(gameInSeconds)+" SportsVU moment clock:"+str(moments[0][2]))
        
        #check whether this EventNum moment is the correct time frame of the play from Play-by-play
        if(quarterPBP < quarterSportVU):
            approxEventNumPBP -= 1
        elif(quarterPBP > quarterSportVU):    
            approxEventNumPBP  += 1
        elif(int(moments[0][2]) > gameInSeconds and int(moments[len(moments)-1][2]) < gameInSeconds):
            found=True
        elif(moments[0][2] < gameInSeconds):
            approxEventNumPBP -= 1
        elif(moments[len(moments)-1][2] > gameInSeconds):
        # look ahead 1 event 
            approxEventNumPBP += 1
        else:
            return "error"
    print("extracted event num "+ str(approxEventNumPBP))
    return approxEventNumPBP

def MomentsfromEventNum(eventsData, eventNum):
    return eventsData['events'][eventNum]["moments"]


# ## Identify Moment of CATCH
# 
# 1.  //sort events moment data from end time to beginning (reverse order)
# timeballReceived, locationballReceived = getReceive (recieverID, List[Moments]) 
# 
# Each moment is taken every .25s, so the FIRST 8 moments (8 *.25 = 2 seconds) when the receiverID and ball are within (dist <= 1 ft), is when the ball was the moment before the ball was released.
# 
# reset numCount = 0;
# 
# Starting from this time, continue iterating through moments. If dist from receiver and ball >=1 ft, then this is time the ball was caught.
# 
# ***separate calculation to check when the ball dist less than 1 ft for another teammate to determine if it was a pass in a certain amount of time (counted numCount)****
# 
# 2.  Find "latest" instance when   distFrom ( Moment.Positions[0].x,Moment.Position[0].y , Moment.Position[ ??=playerID ].x , Moment.Position[ ??=playerID].y) <= 1ft )
# 
#    return the timemilis ,  position[0].x , position[0].y
# 


def getCatchEventDetails(receiverID, passerID, gametimePBP, moments):
    print ("Getting Catch Event Details")
    momentsReversed = moments[::-1]

    index=0
    found = False
    gameInSeconds = GameTimetoSeconds(gametimePBP)
    print("num of moments: "+str(len(momentsReversed)))
    while (found == False):
        if(int(momentsReversed[index][2]) >=  gameInSeconds):
            found=True
        elif(int(momentsReversed[index][2]< gameInSeconds)):
            index += 1
        else:
            return "ERROR"
    
    print("starting at time: "+ str(momentsReversed[index][2]))
    
    #Found the index of the approx start of the event
    numCounts=0
    for i in range(index,len(momentsReversed)):
        if numCounts >= 3:
            timeBallReleased = momentsReversed[i][2]
            indexBallReleased = i
            break
        else:
            ball = momentsReversed[i][5][0]
            for positions in momentsReversed[i][5]:
                if positions[1] == receiverID:
                    player_x = positions[2]
                    player_y = positions[3]
            dist = distance.euclidean([player_x,player_y],[ball[2],ball[3]])
            if dist <= 2:
                print("receiver holding ball: " + str( momentsReversed[i][3]))
                numCounts += 1
                
    #count when ball is caught
    numCounts=0
    for j in range(indexBallReleased, len(momentsReversed)):
        if numCounts >= 3:
            timeBallCaught = momentsReversed[j][2]
            indexBallCaught = j
            break
        else:
            ball = momentsReversed[j][5][0]
            for positions in momentsReversed[j][5]:
                if positions[1] == receiverID:
                    player_x = positions[2]
                    player_y = positions[3]
            dist = distance.euclidean([player_x,player_y],[ball[2],ball[3]])
            if dist >= 2:
                print("receiver just caught ball: " + str(momentsReversed[j][3])+" "+str(j))
                numCounts += 1
                
    #count when ball is passed
    numCounts=0
    for k in range(indexBallCaught, len(momentsReversed)):
        if numCounts >= 2:
            timeBallPassed = momentsReversed[k][2]
            indexBallPassed = k
            break
        else:
            print("aga")
            ball = momentsReversed[k][5][0]
            for positions in momentsReversed[k][5]:
                if positions[1] == passerID:
                    player_x = positions[2]
                    player_y = positions[3]
            dist = distance.euclidean([player_x,player_y],[ball[2],ball[3]])
            if dist <= 2:
                print("passer just passed ball: " +str(momentsReversed[k][3]))
                numCounts += 1
                
    SecsToGameTime(timeBallPassed)
    SecsToGameTime(timeBallCaught)
    SecsToGameTime(timeBallReleased)      
    return timeBallReleased, indexBallReleased, timeBallCaught, indexBallCaught, timeBallPassed, indexBallPassed
   


# ### Extracts Assists, Bad Passes, Alley Oops from csvs in current directory and saves them into separate csv files


def main():
    AST_df = pd.DataFrame()
    BadPass_df = pd.DataFrame()
    AlleyOop_df = pd.DataFrame()
    curPath = os.getcwd()
    print curPath
    os.chdir(curPath+"\pbp-csv")
    for pbpFile in glob.glob("*.csv"):
        print(pbpFile)
        #read file as df
        events_df = pd.read_csv(pbpFile)
        ASTList = events_df[events_df['EVENTMSGTYPE'].isin([1,2]) & ( events_df['VISITORDESCRIPTION'].str.contains("AST", na = False ) | events_df['HOMEDESCRIPTION'].str.contains("AST", na = False )  ) ]
        BadPassList= events_df[( events_df['VISITORDESCRIPTION'].str.contains("Bad", na = False ) | events_df['HOMEDESCRIPTION'].str.contains("Bad", na = False )  ) ]
        AlleyOopList= events_df[events_df['EVENTMSGTYPE'].isin([1,2]) & ( events_df['VISITORDESCRIPTION'].str.contains("Alley", na = False ) | events_df['HOMEDESCRIPTION'].str.contains("Alley", na = False )  ) ]
        AST_df = AST_df.append(ASTList)
        BadPass_df = BadPass_df.append(BadPassList)
        AlleyOop_df = AlleyOop_df.append(AlleyOopList)
        
    AST_df.to_csv("AST_Parsed.csv", sep='\t')
    BadPass_df.to_csv("BadPass_Parsed.csv", sep='\t')
    AlleyOop_df.to_csv("AlleyOop_Parsed.csv", sep='\t')


    # ## AST_df  assists data frame has time and event num of all assists....
    AST_df

    # for each assist event ....
    curPath = os.getcwd()
    print curPath
    SportVU_JSON_Rootpath = "C:\Users\jchin\Documents\GitHub\Data Mining Course\DataMining-Project-Folder\JupyterNotebooks\SportVU_JSON_Data\\"
    #print SportVU_JSON_Rootpath+str(gameid)+".json"
    gameid_prev = 0;
    for index, ast in AST_df.iterrows():
        gameid = ast["GAME_ID"]    #game id from PBP
        eventNumPBP = ast["EVENTNUM"] #eventNumber for the play
        gametimePBP = ast["PCTIMESTRING"]  #game time for the play
        quarterPBP = int(ast["PERIOD"])
        print("prevGameID:"+str(gameid_prev)+", currentlyAnalyzingGameID:"+str(gameid))
        print("PBPEventNum:"+str(eventNumPBP)+", gametimePBP:"+str(gametimePBP))
        #check if SportVU json data is already opened for this PBP play
        if(gameid_prev != gameid):
            #open raw JSON SportVU data using game id from assist
            with open(SportVU_JSON_Rootpath+"00"+str(gameid)+".json") as data_file:    
                rawSportVUData = json.load(data_file)
                json_normalize(rawSportVUData['events'])
            gameid_prev = gameid
        
        #get the correct eventNum (returned as long) in SportsVU
        eventNumSportsVU = findCorrectMomentData(rawSportVUData, quarterPBP, gametimePBP, eventNumPBP)
        
        #extract SportsVU movements for that eventNum
        #rawpossessionSportsVU = MomentsfromEventNum(rawSportVUData, int(eventNumSportsVU))



if __name__ == "__main__":
    main()





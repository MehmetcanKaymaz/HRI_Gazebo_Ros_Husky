import numpy as np
import json
#from simple_cmd import SimpleControl
from vision_cmd import SimpleControl
import cv2
import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose
import threading
import time
from dance import HuskyDancer,HuskySadDancer
#################################################################################################################################################
class LoadLevelParams:
    def __init__(self,json_file="levels.json",level=1):
        self.json_file=json_file
        f = open(json_file)
        data = json.load(f)

        self.min_dist=data["min_dist"]

        self.level=level
        self.level_name="level"+str(self.level)

        self.world_name=data[self.level_name]["file_name"]
        self.init_pose=data[self.level_name]["init_pose"]
        self.final_pose=data[self.level_name]["final_pose"]
        self.duration=data[self.level_name]["duration"]


    def info(self):
        print("World Level : ",self.level)
        print("World Name : ",self.level_name)
        print("World Init Pose : ",self.init_pose)
        print("World Final Pose : ",self.final_pose)
        print("Worlf Duration : ",self.duration)

#################################################################################################################################################
class HuskyPositionListener:
    def __init__(self):
        # Initialize the ROS node
        #rospy.init_node('husky_position_listener', anonymous=True)

        # Subscribe to the /gazebo/model_states topic
        rospy.Subscriber('/gazebo/model_states', ModelStates, self.callback)

        # Initialize the Husky position variables
        self.husky_x = -1
        self.husky_y = -1

        # Start the listener thread
        self.listener_thread = threading.Thread(target=self.listener_loop)
        self.listener_thread.start()

        time.sleep(1)

    def callback(self, data):
        # Get the index of the Husky model in the message
        husky_index = data.name.index('husky')

        # Get the pose of the Husky model
        husky_pose = data.pose[husky_index]

        # Extract the x and y positions of the Husky in the x-y plane
        self.husky_x = husky_pose.position.x
        self.husky_y = husky_pose.position.y

    def listener_loop(self):
        # Continuously listen to the /gazebo/model_states topic
        rospy.spin()

    def get_pose(self):
        # Return the x and y positions of the Husky in the x-y plane
        return [self.husky_x, self.husky_y] 
#################################################################################################################################################            

class Sim:
    def __init__(self,level=1):
        self.LevelParams=LoadLevelParams(level=level)

        self.control=SimpleControl()

        self.position_reader=HuskyPositionListener()

        self.success=False

    def loop(self):
        statu=True
        t1=time.time()
        while statu:
            #statu=self.control.apply_control()

            self.control.single_update()

            # Exit if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            dist_statu=self.check_pose()
            if dist_statu:
                print("Reached The Final Location!!!!!")
                self.success=True
                break

            t2=time.time()
            if t2-t1>self.LevelParams.duration:
                print("Time Over")
                break
        
        #self.control.t.join()
        #self.position_reader.listener_thread.join()
        self.control.run_rose=False
        #self.control.t.join()

        # Release the webcam and close the window
        self.control.cap.release()
        cv2.destroyAllWindows()

        if self.success:
            dancer=HuskyDancer(x=self.LevelParams.final_pose[0],y=self.LevelParams.final_pose[1])
            dancer.dance()
        else:
            curr_pose=self.position_reader.get_pose()
            dancer=HuskySadDancer(x=curr_pose[0],y=curr_pose[1])
            dancer.dance()
        



    def check_pose(self):
        cur_pose=self.position_reader.get_pose()
        final_pose=self.LevelParams.final_pose

        dist=np.sqrt(pow(cur_pose[0]-final_pose[0],2)+pow(cur_pose[1]-final_pose[1],2))

        if dist<self.LevelParams.min_dist:
            return True
        else:
            return False

#sim=Sim(level=2)
#sim.loop()

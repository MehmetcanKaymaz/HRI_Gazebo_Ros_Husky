import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import numpy as np

class HuskyDancer:
    def __init__(self,x=0,y=0):
        #rospy.init_node('husky_position_controller')

        rospy.wait_for_service('/gazebo/set_model_state')
        self.set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        self.x=x
        self.y=y
    
    def dance(self):    
        model_state = ModelState()
        model_state.model_name = 'husky'  # Replace 'husky' with the actual model name of your robot

        N=100
        f=100

        
        for i in range(f):

            for j in range(N):

                # Set the desired position
                model_state.pose.position.x = self.x  # Replace with your desired x-coordinate
                model_state.pose.position.y = self.y  # Replace with your desired y-coordinate
                model_state.pose.position.z = .0  # Replace with your desired z-coordinate

                # Set the desired orientation as a quaternion
                model_state.pose.orientation.x = 0.0  # Replace with your desired x component of the quaternion
                model_state.pose.orientation.y = 1.0  # Replace with your desired y component of the quaternion
                model_state.pose.orientation.z = 0.0  # Replace with your desired z component of the quaternion
                model_state.pose.orientation.w = .5+j/N  # Replace with your desired w component of the quaternion

                self.set_model_state(model_state)

            for j in range(N):

                # Set the desired position
                model_state.pose.position.x = self.x  # Replace with your desired x-coordinate
                model_state.pose.position.y = self.y  # Replace with your desired y-coordinate
                model_state.pose.position.z = .0  # Replace with your desired z-coordinate

                # Set the desired orientation as a quaternion
                model_state.pose.orientation.x = 0.0  # Replace with your desired x component of the quaternion
                model_state.pose.orientation.y = 1.0  # Replace with your desired y component of the quaternion
                model_state.pose.orientation.z = 0.0  # Replace with your desired z component of the quaternion
                model_state.pose.orientation.w = 1.5-j/N  # Replace with your desired w component of the quaternion

                self.set_model_state(model_state)


class HuskySadDancer:
    def __init__(self,x=0,y=0):
        #rospy.init_node('husky_position_controller')

        rospy.wait_for_service('/gazebo/set_model_state')
        self.set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        self.x=x
        self.y=y
    
    def dance(self):    
        model_state = ModelState()
        model_state.model_name = 'husky'  # Replace 'husky' with the actual model name of your robot

        N=100
        f=10

        
        for i in range(f):

            for j in range(N):

                # Set the desired position
                model_state.pose.position.x = self.x  # Replace with your desired x-coordinate
                model_state.pose.position.y = self.y  # Replace with your desired y-coordinate
                model_state.pose.position.z = .0  # Replace with your desired z-coordinate

                # Set the desired orientation as a quaternion
                model_state.pose.orientation.x = 1.0  # Replace with your desired x component of the quaternion
                model_state.pose.orientation.y = .5+j/N  # Replace with your desired y component of the quaternion
                model_state.pose.orientation.z = 0.0  # Replace with your desired z component of the quaternion
                model_state.pose.orientation.w = 0.0  # Replace with your desired w component of the quaternion

                self.set_model_state(model_state)

            for j in range(N):

                # Set the desired position
                model_state.pose.position.x = self.x  # Replace with your desired x-coordinate
                model_state.pose.position.y = self.y  # Replace with your desired y-coordinate
                model_state.pose.position.z = .0  # Replace with your desired z-coordinate

                # Set the desired orientation as a quaternion
                model_state.pose.orientation.x = 1.0  # Replace with your desired x component of the quaternion
                model_state.pose.orientation.y = 1.5-j/N  # Replace with your desired y component of the quaternion
                model_state.pose.orientation.z = 0.0  # Replace with your desired z component of the quaternion
                model_state.pose.orientation.w = 0.0  # Replace with your desired w component of the quaternion

                self.set_model_state(model_state)



if __name__ == '__main__':
    try:
        husky = HuskySadDancer()
        husky.dance()
    except rospy.ROSInterruptException:
        pass

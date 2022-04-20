import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from time import sleep
import sys
import math
import subprocess

# First three denote the position and orientation of the first turtle. Next 3 second. t stands for theta.
x1,y1,t1,x2,y2,t2 = 5,7,0.5,7,7,-1.5

subprocess.run(["rosservice","call","/kill","'turtle1'"])
subprocess.run(['rosservice', 'call', '/spawn', '--', str(x1), str(y1), str(t1), '"turtle1"'])
subprocess.run(['rosservice', 'call', '/spawn', '--', str(x1), str(y1), str(t1), '"turtle2"'])

# The following 2 functions will keep us upto date with the positions of the 2 turtles using the subscription feeds.

def pose_callback1(pose):
	global x1,y1,t1
	x1 = pose.x
	y1 = pose.y
	t1 = pose.theta
	
def pose_callback2(pose):
	global x2,y2,t2
	x2 = pose.x
	y2 = pose.y
	t2 = pose.theta
	

# Here comes the real stuff.

def move_turtles():
    global x1,y1,t1,x2,y2,t2
    
    # Here we define the masses and inital velocities of the objects.
    
    m1=100000000
    m2=10000000000
    
    linear_v1=0.6
    linear_v2=0.1
    w1=w2=0
        
    rospy.init_node('gravity', anonymous=False)
    
    #Getting the publishers ready for updating the velocities later.
    
    pub1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    
    #Getting the feed up to give us positions
    
    rospy.Subscriber('/turtle1/pose',Pose, pose_callback1)
    rospy.Subscriber('/turtle2/pose',Pose, pose_callback2)
    
    # This rate is high because I will update the velocities once in a
    # small time interval dt. The dt is 1/frequency given here.
    
    rate = rospy.Rate(10000) # 10000hz
    
    # These will be stuffed with the updated velocities and published. 
    vel1 = Twist()
    vel2 = Twist()
    
    # Now we just need to figure out what to stuff. Once we do that, job is basically done.
    # But here, we have a problem. Let's say turtle1 has an initial velocity v1, and once dt passes,
    # I want to tell it, this is your new velocity. However, we cannot make the turtle instantaneously rotate its head to face the direction of the new velocity.
    # So, if we want absolute perfection, we can freeze the simulation of gravity for dt, 
    # just stuff a linearv=0, angularv=delta theta/dt, and then feed the updated velocity as linear with angular 0.
    # If we just stuff linear and angular together, the angle the turtle should face now, will be faced in time dt. 
    # That is, the angular velocity lags behind the linear velocity by time dt. 
    # I am lazy, and dt is small. Ignore the lag.
    
    
          
    while not rospy.is_shutdown():
    
    	r2 = (x2-x1)**2+(y2-y1)**2
    	F = 6.6743*(10**(-11))*m1*m2/r2
    	dt = 1/10000
		    
    	v1xnew = linear_v1*math.cos(t1) + (F*(x2-x1)/(m1*math.sqrt(r2)))*dt
    	v1ynew = linear_v1*math.sin(t1) + (F*(y2-y1)/(m1*math.sqrt(r2)))*dt
    	linear_v1 = math.sqrt(v1xnew**2 + v1ynew**2)
    		   
    	v2xnew = linear_v2*math.cos(t2) + (F*(x1-x2)/(m2*math.sqrt(r2)))*dt
    	v2ynew = linear_v2*math.sin(t2) + (F*(y1-y2)/(m2*math.sqrt(r2)))*dt 
    	linear_v2 = math.sqrt(v2xnew**2 + v2ynew**2)   
    		    
    	temp=math.atan(v1ynew/v1xnew)
    		    
    	if v1xnew<0:
    		    	if temp>0:
    		    		t1new=(temp-math.pi)
    		    	else:
    		    		t1new=(temp+math.pi)
    	else:
    		    	t1new=temp
    		    	
    	w1=((t1new-t1)%(2*math.pi))/dt
		    	
    	temp2=math.atan(v2ynew/v2xnew)
    	if v2xnew<0:
    		    	if temp2>0:
    		    		t2new=(temp2-math.pi)
    		    	else:
    		    		t2new=(temp2+math.pi)
    	else:
    		    	t2new=temp2
    		    	
    	w2=((t2new-t2)%(2*math.pi))/dt
    	     
    	vel1.linear.x = linear_v1
    	vel1.linear.y = 0
    	vel1.linear.z = 0

    	vel1.angular.x = 0
    	vel1.angular.y = 0
    	vel1.angular.z = w1
		   
    	vel2.linear.x = linear_v2
    	vel2.linear.y = 0
    	vel2.linear.z = 0

    	vel2.angular.x = 0
    	vel2.angular.y = 0
    	vel2.angular.z = w2


    	pub1.publish(vel1)
    	pub2.publish(vel2)

    	rate.sleep()

if __name__ == '__main__':
    
    try:
        move_turtles()
    except rospy.ROSInterruptException:
        pass

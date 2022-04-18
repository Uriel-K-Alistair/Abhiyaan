#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>


int main(int argc, char **argv)
{
  ros::init(argc, argv, "talker");
  ros::NodeHandle n;
  ros::Publisher team_abhiyaan_pub = n.advertise<std_msgs::String>("/team_abhiyaan", 1000);
  ros::Rate loop_rate(10);

  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    ss << "Team Abhiyaan rocks";
    msg.data = ss.str();
    team_abhiyaan_pub.publish(msg);
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}


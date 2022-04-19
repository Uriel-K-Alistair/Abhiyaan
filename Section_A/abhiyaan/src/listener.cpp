#include "ros/ros.h"
#include "std_msgs/String.h"
#include <cstdio>

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  std::cout<<msg->data.c_str();
  std::cout<<std::endl;
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/team_abhiyaan", 1000, chatterCallback);
  ros::spin();
  return 0;
}



#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <cstdio>


class ear{
   public:
      std::string revstr;
      void chatterCallback(const std_msgs::String::ConstPtr& msg);
      };
      
      
void ear::chatterCallback(const std_msgs::String::ConstPtr& msg)
{
  std::string x = msg->data.c_str();
  x+=' ';
  std::stringstream ss;
  
  int no=x.length();
  int start=0;
  
  for(int i=0;i<no;i++){
  	char t=x.at(i);
  	if(t==' '){
	    for(int j=i;j>start-1;j--){
        ss<<x.at(j);
      }
      ss<<' ';
      start=i+1;
	  }
  }
    
  revstr=ss.str();  
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "reverser");
  ros::NodeHandle n;
  ros::Publisher team_abhiyaan_pub2 = n.advertise<std_msgs::String>("/naayihba_maet", 1000);
  ear myear;
  ros::Subscriber sub = n.subscribe("/team_abhiyaan", 1, &ear::chatterCallback, &myear); 
  std_msgs::String rmsg;
  
  ros::Rate loop_rate(10); 
while (ros::ok()){  
  ros::spinOnce();
  //std::cout<<myear.revstr;
  rmsg.data = myear.revstr;
  team_abhiyaan_pub2.publish(rmsg);
  loop_rate.sleep();
  }
  
  ros::spin();
  return 0;
}



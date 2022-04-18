#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>
#include <cstdio>

/*
At the core of this code, in the middle of main, we just subscribe to /team_abhiyaan" 
and run a function every time we see a message.
This function will take the message and reverse the string. I will then have to publish the string to another topic.

For whatever reason, I'm unable to publish inside the function, so I retain the publising business in main.
The only job of the function is to hear the message, reverse it and keep it for my use. 
In order to access this function's output, I am making it a class method, and keeping the reversed string as an attribute.

That's basically it. Subscribe-Reverse-Publish-Repeat.
*/
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



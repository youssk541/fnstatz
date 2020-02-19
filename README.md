## Final school project : Twitter notifications for financial markets 

This project is designed to automatically publish tweets about financial markets . 


## Setup

# Step 0
Donwload the project. This can be done directly by using the green download button. (If you do it this way don't forget to unpack the compressed folder)  
It can also be done through a command prompt by writing the command line : **git clone github.com/youssk541/fnstatz** 
After this step you should have the project folder on your machine.
# Step1

Create a twitter developper app . You can find a comprehensive tutorial here : [Link](https://www.youtube.com/watch?v=2o_qt9cXicM)

# Step 2

In  _docs/twitter_credentials.py_ , fill out the 4 fields : 

- ACCESS_TOKEN=""
- ACCESS_TOKEN_SECRET=""
- CONSUMER_KEY=""
- CONSUMER_SECRET=""

Enter the credentials that you've been given for your account (Make sure to also store them somewhere else as they might not be given again)

# Step 3
Make sure that you have python on your machine as well as an environment variable linked with the install folder for your version of python (usually in the C:\program_files folder but it might not be the case if you chose to save it somewhere else).  
If you don't have python , you can download it from here [link](https://www.python.org/downloads/)  
To set up an environment variable, check out this tutorial : [link](https://www.youtube.com/watch?v=Y2q_b4ugPWk)  
# Step 4
Now that you have your environment set up properly, you can start using the application.

First double click on _Startup_ to initalize the application: This will download the python requirements and all files necessary for the application to function correctly . This step might take a few minutes .

The project is now fully set-up, you can double click on  _startTwitter_ to start the publications and analysis.



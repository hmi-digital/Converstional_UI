## [Conversational User Interface(UI)](https://hmi-digital.github.io/) - The next interaction paradigm
**Conversational UI** is evolving into the interface of future . It gives user a privilege of interacting with computers more naturally than they currently do.

Conversational UI takes two forms — 
 - **Voice assistant** that allows user to talk (uses speech recognition)
 - **Chatbots** that allow user to type.
  
The arrival of chatbots have opened up new realms of the customer engagement. Some of the advantages of Chatbots
- Ability to engage with the users in a natural and friendly manner 
- Multimodal interface provides ease of interaction 
- Wasy integration with familiar platforms like Facebook, Skype, MS Teams, Slack etc. through API 
- Capability to outperform humans with the speed of handling customer queries 
- Improved efficiency with round the clock customer service 
- Easy to build and cost efficient

Overview
------------
This repo provides you the chatbot engine that you can download and customize to your business needs.

The BOT platform is client-server architecture, client being different channels - browser, mobile App or messenger tools like FaceBook, Slack, MS Teams etc.

The BOT server support REST APIs as well as WebSocket using Jetty Server as a API gateway. 

<img src="https://github.com/hmi-digital/Conversational_UI/blob/master/Conversational_UI/Documents/architecture.png" alt="Platform Architecture"/>

There are three major components of BOT platform -

- DIALOG Engine (DE) – This is core module, and it maintains the state of dialog with the end user

- NLP Engine (NE)– This module identifies intent and entities for given user utterances using advanced NLP algorithms

- BROKER Engine (BE)– This is communication module and handles messages between DE and NE and uses Kafka based messaging system. 

Documents can be found at [this](https://github.com/hmi-digital/Conversational_UI/tree/master/Conversational_UI/Documents) location. Quick Start Guide is easy way to get started.

Prerequisite
------------
This system was implemented and tested under Windows, Linux and Mac OS X with the following software 

+ Ubuntu 14.10.4 / Mac OS X 10.10 / Windows 10
+ OpenJDK 15 or higher (all system variables are set JAVA_HOME etc.) This should work on Java JDK 1.8 but not tested.
+ Python 3.8 or higher

Download and install **NLP Engine**
---------------------------------
+ Clone or download this repo and copy files from Releases to D:/ folder (or your prefered location)
+ Locate NLPEngine folder
+ Ensure that you have following folder structure

     - config
     - coreNLP
     - keys
     - pubsub
     - requirements.txt
     - service.py
     
+ Install all the required python modules from requirements.txt

```
$ python -m install pip install -r ./requirements.txt
```
+ Download NLTK data
```
$ python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
>>> exit()
```
+  Run **NLP Engine** 
```
$ python service.py
```

Download and install **Dialog Engine**
------------------------------------
+ Go to DialogEngine folder 
+ Ensure that you have following folder structure
     
     - lib
     - res
     - hmi.jar
     
+ Open command prompt, go to D:\DialogEngine folder and run following command
```
$ java -jar hmi.jar -h
usage: bot [-f <arg>] [-h] [-i <console, rest>] [-p <arg>] [-r <arg>] [-s
       <arg>]
 -f,--file <arg>                  specify dialogue path and file, e.g. -f
                                  /res/dialogue1.xml
 -h,--help                        print this message
 -i,--interface <console, rest>   select user interface
 -p,--port <arg>                  port on which jetty server runs, e.g. -p
                                  8080
 -r,--resource <arg>              load dialogue (by name) from resources,
                                  e.g. -r dialogue1
 -s,--store <arg>                 load dialogue (by name) from internal
                                  store, e.g. -s dialogue1
                                  
$ java -jar hmi.jar -i rest –p 8080 -r trip_en
```
+ Above command will run a sample trip booking use case (at D:\DialogEngine\res\dialogues folder)
+ Bot engine is now ready to interact at port 8080 and uses inbuilt jetty server
+ Go to chrome browser and enter URL - https://\<Your Machine IP\>:8080/en
  
Go through the detailed document located [here](https://github.com/hmi-digital/Conversational_UI/tree/master/Conversational_UI/Documents) to understand the different features and functionalities of BOT platform

# Introduction

Welcome to the readme file for the Socket Programming-project!

This project focusses on the security of transfering live video through socket programming using Python 3.12. This project consists of three seperate prototypes using different approached to encryption:
<br>
•	Prototype 1 (ALE_Client.py & ALE_Server.py): Application Level Encryption (ALE)
<br>
•	Prototype 2 (TLS_Client.py & TLS_Server.py): Transport Layer Security (TLS)
<br>
•	Prototype 3 (ALE_TLS_Client.py & ALE_TLS_Server.py): ALE + TLS

This readme file will provide instruction on how to use each prototype in a ubuntu 20.04 environment:

# Prototype 1 (ALE_Client.py & ALE_Server.py): Application Level Encryption (ALE)
1. Make sure to use two seperate terminals
2. In both terminals to the folder of this using the linux commandline.
```cd {path to project}```
3. Only use this step if you want a fresh venv for this project! Otherwise skip to step 4.<br>
3.a Create a new virtualenv by using ```virtualenv venv```<br>
3.b Activate the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)<br>
3.c install dependecies of this project via ```pip install -r requirements.txt```<br>
4. In both terminals activate the the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)
5. Run the server socket using ```python ALE_Server.py```
6. Run the client socket using ```python ALE_Client.py```
7. Video transmitted should be visible, press 'q' to exit and close both sockets.

# Prototype 2 (TLS_Client.py & TLS_Server.py): Transport Layer Security (TLS)
1. For this prototype a root self signed certificate and private key must be used, follow the steps of: 
https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8 and place the files in the keys folder
2. Make sure to use two seperate terminals
3. In both terminals to the folder of this using the linux commandline.
```cd {path to project}```
4. Only use this step if you want a fresh venv for this project! Otherwise skip to step 5.<br>
4.a Create a new virtualenv by using ```virtualenv venv```<br>
4.b Activate the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)<br>
4.c install dependecies of this project via ```pip install -r requirements.txt```<br>
5. In both terminals activate the the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)
6. Run the server socket using ```python TLS_Server.py```
7. Run the client socket using ```python TLS_Client.py```
8. Video transmitted should be visible, press 'q' to exit and close both sockets.

# Prototype 3 (ALE_TLS_Client.py & ALE_TLS_Server.py): Application Layer Encryption & Transport Layer Security (TLS)
1. For this prototype a root self signed certificate and private key must be used, follow the steps of: 
https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8 and place the files in the keys folder
2. Make sure to use two seperate terminals
3. In both terminals to the folder of this using the linux commandline.
```cd {path to project}```
4. Only use this step if you want a fresh venv for this project! Otherwise skip to step 5.<br>
4.a Create a new virtualenv by using ```virtualenv venv```<br>
4.b Activate the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)<br>
4.c install dependecies of this project via ```pip install -r requirements.txt```<br>
5. In both terminals activate the the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)
6. Run the server socket using ```python ALE_TLS_Server.py```
7. Run the client socket using ```python ALE_TLS_Client.py```
8. Video transmitted should be visible, press 'q' to exit and close both sockets.

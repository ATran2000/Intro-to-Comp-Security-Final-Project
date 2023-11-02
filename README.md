# Intro-to-Comp-Security-Final-Project

About:  
Own implementation of Apple's AirDrop where you can securely send files to other clients on the server.

For a visual representation of the project, check it out on my portfolio website! <br>
Link to the website: [`https://avtran-portfolio.vercel.app/projects/securedrop`](https://avtran-portfolio.vercel.app/projects/securedrop)

Steps To Use Code:  
1) Download the project directory.  
2) After downloading, create a copy of the project directory and delete AFILE.txt.  
3) Open up a terminal and run server.py in the Project_Network directory in the original project directory.  
4) Open up another terminal and run secure_drop.py in the original project directory and go through the registration process. Run secure_drop.py again and go through login process.  
5) Repeat step 4 but in the copy of the project directory.  
6) In both directories, add each other as friends. For instructions, type help in the terminal.
7) You should see each other in the contact list when typing the list command.
8) In the original project directory, lets send a file from the original directory to the copied directory. Type 'send (contact_email_chosen_for_copy) AFILE.txt'. You should see a prompt in the 
   terminal for the copied directory, type 'y' and AFILE.txt should show up as a new file.

Note:
- Doing ctrl-c will absolutely break the program. So make sure to always stop the program by typing the exit command.
- In order to fix the broken program, make sure to close all other secure_drop programs and close the server.py program. In the directory that is broken, make sure to delete
  user.json, and contacts.json. In addition, delete server_list.json to make sure everything runs smoothly.

Interesting Things From Project:
- bcrypt is used to encrypt the password, so if you have created a user in a secure_drop program and check the user.json file, you should see that the value for the key password is encrypted.
- The contacts.json file is encrypted. Whenever you create a new user while not logged into the program, your contacts list is hidden from anyone that wants to access it. It will only be readble
  to the user when the user logs into the program.
- The server_list.json file actively adds and removes users from the json object when the users logs into the program and exits.
- The contacts.json and server_list.json file actively displays new users in the json object when the user adds a new contact.
- The list command only displays contacts that the user has added and whom added the user back. In addition, the contact only appears if the contact is online and logged in.

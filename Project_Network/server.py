'''
Class: Introduction to Computer Security
Assignment: Project
Team 3: Eddie Tran, Alvin Tran, Joshua Hou
Date: 12/14/2021
'''

import socket
import json
import os

open("server_list.json", "a+") # opens server_list.json / creates if does not exist


hostname = socket.gethostname() # returns name of device
host = socket.gethostbyname(hostname) # returns ip address of the device
port = 5555 # port number that clients will use to communicate with the server

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # AF_INET is family of protocols. SOCK_DGRAM is a type that for connectionless protocols
s.bind((host, port)) # binds address:(hostname, port#) to socket 
print("Server is Live. Accepting Users...\n")

while True:
    flag = "Idle" # our flag parameter

    data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
    flag = data.decode("utf-8") # decode the flag so it's readable
    
    if flag == "Adding User":
        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        data = data.decode("utf-8") # decode data so it's readable
        user_email = data # store data as good var name
        port = addr[1]  # store port as good var name

        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        data = data.decode("utf-8") # decode data so it's readable
        user_contact = json.loads(data) # store data as good var name
        
        on_server = {"email": user_email, "port": port} # json objects
        on_server.update(user_contact) # update based off objects

        file_path = "server_list.json" # get file path of server list
        if os.path.getsize(file_path) == 0:  # checks if there is anything in the server_list json file
            with open("server_list.json", "a+") as f:  # if there is nothing, will create a new dictionary and append first key-value pair
                file_data = {}
                file_data["server_info"] = []
                file_data["server_info"].append(on_server)
                f.seek(0)
                json.dump(file_data, f, indent=4)
                print("User Added.")
        else:
            with open("server_list.json", "r+") as f: # load json data if exist
                file_data = json.load(f)
                file_data["server_info"].append(on_server) # add
                f.seek(0)
                json.dump(file_data, f, indent=4)
                f.truncate()
                print("User Added.") # confirmation
    
    elif flag == "Receiving Port": # retrieve port data and send to client
        data, addr = s.recvfrom(1024)
        port_data = addr[1]
        port_data = str(port_data)
        port_data = port_data.encode("utf-8") # encode data to send
        s.sendto(port_data, (host, addr[1]))

    elif flag == "Updating Contacts": # update contact list
        with open("server_list.json", "r+") as f: # open server list
            file_data = json.load(f) # load data
            data, addr = s.recvfrom(1024) # receive data
            new_contact = data.decode("utf-8") # decode data
            new_contact = json.loads(data) # assign data to good var name

            for e in file_data["server_info"]:  # loop through json
                if addr[1] == e["port"]: # if port == desired port
                    for x in e["contact_info"]: # loop through contact info
                        if new_contact["email"] == x["email"]: # if emails match, update
                            x.update(new_contact)
                            f.seek(0)
                            json.dump(file_data, f, indent = 4)
                            f.truncate()
                            break
                    else:
                        e["contact_info"].append(new_contact) # append email
                        f.seek(0)
                        json.dump(file_data, f, indent=4)
                        f.truncate()
    
    elif flag == "Listing Contacts":
        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        user_email = data.decode("utf-8") # decodes data

        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        contact_email = data.decode("utf-8") # decodes data

        found = False # flag

        with open("server_list.json", "r+") as f: # open and load server list json data
            file_data = json.load(f)
            for e in file_data["server_info"]: # loop through contacts
                if contact_email == e["email"]: # if contact emails match then loop contact info
                    for u in e["contact_info"]:
                        if user_email == u["email"]: # if client email matches correctly return true and send to client
                            found = True
                            msg = "true"
                            msg = msg.encode("utf-8")
                            s.sendto(msg, (host, addr[1]))
                            break

        if found == False: # if it doesn't send false instead
            msg = "false"
            msg = msg.encode("utf-8")
            s.sendto(msg, (host, addr[1]))

    elif flag == "Sending File":
        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        user_email = data.decode("utf-8") # decodes data

        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        contact_email = data.decode("utf-8") # decodes data

        found = False # flag

        for e in file_data["server_info"]: # similar to list, loop server json data
                if contact_email == e["email"]: # check if emails match
                    for u in e["contact_info"]: # loop to check contact json data
                        if user_email == u["email"]: # if it matches return true and send to client, other wise return false
                            found = True

                            contact_port = e["port"]
                            contact_port = str(contact_port)
                            contact_port = contact_port.encode("utf-8")
                            s.sendto(contact_port, (host, addr[1]))
                            break

        if found == False:
            msg = "false"
            msg = msg.encode("utf-8")
            s.sendto(msg, (host, addr[1]))
                
    elif flag == "Removing User": # removes user from server list
        data, addr = s.recvfrom(1024) # this method receives UDP message , 1024 means the # of bytes to be read from the udp socket.
        data = data.decode("utf-8") # decodes data
        user_email = data # set data to good var name

        with open("server_list.json", "r+") as u: # load data
                file_data2 = json.load(u)
                count = 0 # our counter
                for e in file_data2["server_info"]: # loop through json
                    if e["email"] == user_email: # if email exist, then we pop (remove)
                        file_data2["server_info"].pop(count)
                        u.seek(0)
                        json.dump(file_data2, u, indent = 4)
                        u.truncate()
                    count = count + 1
        print("User Removed.")
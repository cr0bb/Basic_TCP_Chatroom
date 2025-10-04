# Basic TCP Chatroom #
Made by Corbin Parsley

#### This is a simple, local TCP chatroom I made in python to practice basic socket programming and a little bit of networking. ####

The server is ran with 'server.py' and a new connection can be made by running 'client.py' and choosing a nickname.
The password for the admin account, chat and activity logs, and the ban list are all stored in unecrypted plaintext files (hopefully implementing encryption soon).

I am new to scripting in python and networking in general, so any review/feedback is welcome!

## Features ##
- Local chatting on a TCP server
- Chat and activity logging
- Allows for multiple connections with multi-threading
- Two client types:
  * Normal Client (Any username)
    - Can send basic commands ('/quit', '/help', etc.) to server
    - Broadcasts messages to all other clients
  * ADMIN Client
    - Requires ADMIN password to connect (stored in 'password.txt')
    - Can send basic and ADMIN ('/kick', '/ban', etc.)
    - Has access to chat and activity logs through '/alogs' and '/clogs' commands
### Commands ### 
  - Basic Commands:
    * /help - displays a list of available commands
    * /list - displays a list of connected clients
    * /quit - quits the server
  - Admin Commands:
    * /alogs [n]                - displays the last [n] activity logs
    * /ban [nickname]           - bans a client from the server
    * /clearlogs [ 'c' / 'a' ]  - clears chat or activity logs
    * /clogs [n]                - displays the last [n] chat logs
    * /kick [nickname]          - kicks a client from the server
    * /pw [ 'c' / 'v' ]         - change or view the admin password
 ### Logs ###
  - Chat Logs: 'chats.log'
    * Logs any and all chats from current and previous connetions to the server, can be cleared with '/clearlogs c'
  - Activity Logs: 'activity.log'
    * Logs any and all connections, disconnections, kicks, and bans, can be cleared with '/clearlogs a'

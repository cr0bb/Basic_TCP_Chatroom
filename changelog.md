# CHANGELOG #

## Version 1.0.0 ##
### Summary ###
  - Initial version
  - Basic functionality and commands
  - Admin Password, chat/activity logs, etc. are stored in plaintext or log files
  - Only works locally ('127.0.0.1') on a set TCP port
### Features ###
  - Local chatting
  - Chat and Activity Logging
    * Logs all chat messages to a file (chat.txt)
    * Logs all activity (client connects/disconnects) to a file (activity.txt)
   - Multiple Clients ran in separate threads
#### Clients ####
  - Normal Client (Any other username):
    * Can send basic commands to the server ('/help', '/quit', '/list', etc.)
    * Can broadcast messages to other clients
   
  - ADMIN Client ('ADMIN' username):
    * Requires admin password to connect (password.txt)
    * Can send basic AND ADMIN commands ('/kick', '/ban', '/clearlogs', etc.) to the server
    * Has access to chat and activity logs through '/clogs' and '/alogs' commands
#### Commands ####
  - Basic Commands
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
  

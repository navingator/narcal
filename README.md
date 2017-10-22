# narcal
This application aims to solve some of the more annoying aspects of the one45 calendar feeds. It will clean up:

* Summary to only include the name of the event
* Location to concatenate location and room number and replace configured strings (see below)

## Configuration
Currently, there are 3 forms of configuration available, shown in the config folder and in the base directory. There are samples in this folder that can be copied into the correct configuration file. Be careful with newlines at the ends of these files. I had a strange error that I don't have time to investigate with newlines on my ubuntu server, so I recommend that you don't append them to the ends of the configuration files.

First, you should specify sources and usernames for each person in the sources.csv file. There must be a header row, and each row following must have the username, name, and one45 calendar URL in that order. 

Second, you should specify replacements as necessary in the location.replacements.csv file. As before, there must be a header row, and each row following must have the old text followed by the replacement text.

Lastly, you will need to configure .env in the base directory to specify the host and port.

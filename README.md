# Full Service Bot 5000
This was created for a Twitch streamer to have running in their chat.

This will reply to users in a variety of ways based off of four lists. It will respond positively, negatively, neutrally, or with an insane response at random. 
It will also set a trigger OBS sources to enable then disable so that the bot gains a graphical response

A .token, .channel, and .obs-websocket file will need to be created.
The .token file will only contain the Twitch access token, and the .channel file will have to Twitch channel name to post in.
The first line in the .obs-websocket file will be the port, and the second will be the websocket plugin password

The response lists are in the responses folder. Add each response on a new line. In the responses folder there should be a positive-responses.txt, a negative-responses.txt, a neutral-responses.txt, and an insane-responses.txt.
I've only added two each as an example, and will add it to the gitignore after so the streamer's responses aren't tracked.

In OBS, in whichever scene you choose, have a corresponding source for each response file. By default, the code works with sources named 'fsbPositive', 'fsbNegative', 'fsbNeutral', and 'fsbInsane'. Make sure to change the scene variable in the obs_controller.py file to scene name the sources are under.
# Full Service Bot 5000
This was created for a Twitch streamer to have running in their chat.

This will reply to users in a variety of ways based off ChatGPT 4.0, prompted in a way to give the impression of a particular personality.
It will also trigger the enabling, then disabling after a duration, a source inside a scene in OBS

## A .env file will need to be created. It should look like the following
```
OPENAI_API_KEY=theOpenAiKey
TWITCH_ACCESS_TOKEN=theTwitchAccessToken
CHANNEL=theTwitchChannelToChatOn
WEB_SOCKET_PORT=webSocketPort
WEB_SOCKET_PASSWORD=webSocketPassword
```

## OBS Sources
In OBS, in whichever scene you choose, have a corresponding source for each response file. By default, the code works with sources named 'fsbPositive', 'fsbNegative', 'fsbNeutral', and 'fsbInsane'. Make sure to change the scene variable in the obs_controller.py file to scene name the sources are under.

## Not currently in use
* chatgpt_response.py - This was a test using a cheaper ChatGPT 3.5 model, but I found the response time too slow. I will revisit later to see if there have been speed improvements

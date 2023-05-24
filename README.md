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

## Install and run
1. Install Python 3.9
2. Activate the virtual environment with Python 3.9 selected 
3. 'pip install requirements.txt'
4. Run main.py

## Not currently in use
* chatgpt_response_davinci.py - This was a test using the Davinci model as it was easier to get the responses I was going after, but it is relatively expensive. I ended up getting just as good results with the cheaper model after playing with the prompts.
* chatgpt_response_gpt4.py - I don't yet have access to this model, it was just prep
from twitchio.ext import commands
from random import random
import threading
from dotenv import load_dotenv
import os

import obs_controller
import chatgpt_response as cr
import log


class Bot(commands.Bot):

    def __init__(self):
        access_token = os.getenv('TWITCH_ACCESS_TOKEN')
        self.channel = os.getenv('CHANNEL')

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=access_token, prefix='!', initial_channels=[self.channel])

    async def get_response(self, user_name, user_message):
        response = cr.get_reply(user_name, user_message)

        # Control OBS, the OBS controller is run on a separate thread to prevent holding up the response
        emotion = cr.determine_tone(response)
        toggle_graphic_thread = threading.Thread(target=obs_controller.toggle_fsb_visual, args=[emotion])
        toggle_graphic_thread.start()
        return f'{response}'

    async def start_dialog(self, user_name, user_message):
        dialog = cr.get_dialog(user_name, user_message)

        # Control OBS, the OBS controller is run on a separate thread to prevent holding up the response
        emotion = cr.determine_tone(dialog)
        toggle_graphic_thread = threading.Thread(target=obs_controller.toggle_fsb_visual, args=[emotion])
        toggle_graphic_thread.start()
        return f'{dialog}'

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console and log it...
        message_log_text = f'{message.author.display_name}: {message.content}'
        print(message_log_text)
        log.log_chat(message_log_text)

        # Randomly pick someone speaking to talk with
        random_threshold = 0.25
        random_number = random()
        if random_number < random_threshold and message.content[0] != '!':
            await self.speak_unprompted(message.author.display_name, message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command(aliases=['fsb5000,', 'fsb5000!', 'fsb5000.', 'fsb5000;'])
    async def fsb5000(self, ctx: commands.Context):
        fsb_response = await self.get_response(ctx.author.display_name, ctx.message.content)
        await ctx.send(f'@{ctx.author.display_name} {fsb_response}')
        fsb_response_log_text = f'***** Full Service Bot 5000: {ctx.author.display_name} -> {fsb_response}'
        print(fsb_response_log_text)
        log.log_chat(fsb_response_log_text)

    async def speak_unprompted(self, viewer, viewer_text):
        fsb_dialog = await self.start_dialog(viewer, viewer_text)
        await self.get_channel(self.channel).send(f'@{viewer} {fsb_dialog}')
        fsb_dialog_log_text = f'*********** Full Service Bot 5000: {viewer} -> {fsb_dialog}'
        print(fsb_dialog_log_text)
        log.log_chat(fsb_dialog_log_text)


if __name__ == '__main__':
    load_dotenv()
    bot = Bot()
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.

from twitchio.ext import commands
from random import randint
import threading
import response
import obs_controller


class Bot(commands.Bot):

    def __init__(self):
        with open('.token') as f:
            access_token = f.read().strip()

        with open('.channel') as f:
            channel = f.read().strip()

        self.all_responses = response.load_all_responses()

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=access_token, prefix='!', initial_channels=[channel])

    async def get_response(self):
        random_list = randint(0, len(self.all_responses) - 1)
        random_response = randint(1, len(self.all_responses[random_list]) - 1)

        emotion_file = self.all_responses[random_list][0]
        chosen_response = self.all_responses[random_list][random_response]

        del self.all_responses[random_list][random_response]

        if len(self.all_responses[random_list]) == 1:
            file = self.all_responses[random_list][0]
            loaded_responses = response.load_specific_responses(file)
            for item in loaded_responses:
                self.all_responses[random_list].append(item)

        # Control OBS, the OBS controller is run on a separate thread to prevent holding up the response
        emotion = response.parse_emotional_response(emotion_file)
        toggle_graphic_thread = threading.Thread(target=obs_controller.toggle_fsb_visual, args=[emotion])
        toggle_graphic_thread.start()
        return f'{chosen_response}'

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

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command(aliases=['fsb5000,', 'fsb5000!', 'fsb5000.', 'fsb5000;'])
    async def fsb5000(self, ctx: commands.Context):
        fsb_response = await self.get_response()
        await ctx.send(f'{ctx.author.name}{fsb_response.strip()}')
        print(f'Full Service Bot 5000: {ctx.author.name}{fsb_response.strip()}')


if __name__ == '__main__':
    bot = Bot()
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.

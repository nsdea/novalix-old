# Local
try:
    from .helpers import config, management
except ImportError:
    import helpers.config, helpers.management

import os
import discord

from dotenv import load_dotenv
from prsaw import RandomStuff
from discord.ext import commands
from discord.commands import slash_command

load_dotenv()

class ChatBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rs = RandomStuff(async_mode=True, api_key=os.getenv('PRSAW'))
    
    @commands.Cog.listener()
    async def on_message(self, message): 
        if not message.content:
            return

        if message.author.bot or message.content[0] in '!"§$%&/()=?`´+*#\'-_.:,;<>|':
            return

        valid = False

        if isinstance(message.channel, discord.DMChannel):
            valid = True
        else:
            if config.load('chatbot_channels').get(message.guild.id):
                if config.load('chatbot_channels').get(message.guild.id).get('channel') == message.channel.id:
                    valid = True

        if valid:
            async with message.channel.typing():
                try:
                    ai_response = await self.rs.get_ai_response(message.content)
                    ai_response = ai_response[0].get('message')
                except Exception as e:
                    ai_response = f'Sorry, there\'s an error: `{e}`'
                await message.channel.send(ai_response)

    @commands.has_permissions(manage_channels=True)
    @slash_command(description='🤖 Sets the channel in which the chatbot can respond to.')
    async def chatbot(self, ctx,
        channel: discord.commands.Option(discord.TextChannel, 'ChatBot Channel (Optional)', required=False, default=None),
        mode: discord.commands.Option(str, 'Mode (Optional)', required=False, default='normal'),
    ):

        chatbot_channels_config = config.load('chatbot_channels')
        chatbot_channels_config[ctx.guild.id] = {'channel': channel.id if channel else None, 'mode': mode}
        config.save(chatbot_channels_config, 'chatbot_channels')

        await ctx.respond(embed=discord.Embed(title='Alright!', description=f'The chatbot channel is now set to {channel.name if channel else "no channel"}. Go send a message in there, the bot will respond!\nYou can only have one chatbot channel at the time.', color=management.color()).set_footer(text='Use /channels to view the channel settings.'))


def setup(client):
    client.add_cog(ChatBot(client))
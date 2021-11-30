try:
    from .helpers import config, management, images
except ImportError:
    import helpers.config, helpers.management

import discord.commands

from discord.ext import commands
from discord.commands import slash_command

class JoinLeave(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        await channel.send(file=images.join(member=member))

    @commands.has_permissions(manage_channels=True)
    @slash_command(description='👋 Sets the server\'s welcome/join message channel.')
    async def joins(self, ctx,
        channel: discord.commands.Option(discord.TextChannel, 'Welcome Message Channel'),
        style: discord.commands.Option(str, 'Style of the image (Optional)', required=False, default='join'),
        text: discord.commands.Option(str, 'Additional text (Optional)', required=False, default=''),
    ):

        join_channels_config = config.load('join_channels')
        join_channels_config[ctx.guild] = {'channel': channel.id, 'style': style, 'text': text, 'details': ''}
        config.save(join_channels_config, 'join_channels')
        await ctx.respond(title='Alright!', description=f'The welcome message channel is now set to {channel.name}.\nBy the way, you can only have 1 join **and** 1 leave channel at the time. (If you don\'t get it: you can have 1 joinchannel and 1 leavechannel per server, but you **can** use the same channel for both join **and** leave.)', color=management.color())

def setup(client):
    client.add_cog(JoinLeave(client))
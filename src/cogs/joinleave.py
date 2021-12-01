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
        channel = discord.utils.get(member.guild.channels, id=str(config.load('join_channels')[member.guild.id]['channel']))
        await channel.send(file=images.join(member=member))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, id=str(config.load('leave_channels')[member.guild.id]['channel']))
        await channel.send(file=images.leave(member=member))

    @commands.has_permissions(manage_channels=True)
    @slash_command(description='👋 Sets the server\'s welcome/join message channel.')
    async def joins(self, ctx,
        channel: discord.commands.Option(discord.TextChannel, 'Welcome Message Channel'),
        style: discord.commands.Option(str, 'Style of the image (Optional)', required=False, default='join'),
        text: discord.commands.Option(str, 'Additional text (Optional)', required=False, default='Make sure to read and accept the rules.'),
    ):

        join_channels_config = config.load('join_channels')
        join_channels_config[ctx.guild.id] = {'channel': channel.id, 'style': style, 'text': text, 'details': 'Have fun!'}
        config.save(join_channels_config, 'join_channels')

        await ctx.respond(embed=discord.Embed(title='Alright!', description=f'The welcome message channel is now set to {channel.name}.\nBy the way, you can only have 1 join **and** 1 leave channel at the time. (If you don\'t get it: you can have 1 joinchannel and 1 leavechannel per server, but you **can** use the same channel for both join **and** leave.)', color=management.color()))

    @commands.has_permissions(manage_channels=True)
    @slash_command(description='😞 Sets the server\'s leave message channel.')
    async def leaves(self, ctx,
        channel: discord.commands.Option(discord.TextChannel, 'Leave Message Channel'),
        style: discord.commands.Option(str, 'Style of the image (Optional)', required=False, default='leave'),
        text: discord.commands.Option(str, 'Additional text (Optional)', required=False, default='Hope you had fun :\')'),
    ):

        join_channels_config = config.load('leave_channels')
        join_channels_config[ctx.guild.id] = {'channel': channel.id, 'style': style, 'text': text, 'details': 'Goodbye!'}
        config.save(join_channels_config, 'leave_channels')

        await ctx.respond(embed=discord.Embed(title='Alright!', description=f'The leave message channel is now set to {channel.name}.\nBy the way, you can only have 1 join **and** 1 leave channel at the time. (If you don\'t get it: you can have 1 joinchannel and 1 leavechannel per server, but you **can** use the same channel for both join **and** leave.)', color=management.color()))

def setup(client):
    client.add_cog(JoinLeave(client))
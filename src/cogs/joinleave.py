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
        try:
            channel = discord.utils.get(member.guild.channels, id=int(config.load('join_channels')[member.guild.id]['channel']))
            await channel.send(content=member.mention, file=images.join(member=member))
        except KeyError:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            channel = discord.utils.get(member.guild.channels, id=int(config.load('leave_channels')[member.guild.id]['channel']))
            await channel.send(content=member.mention, file=images.leave(member=member))
        except KeyError:
            pass

    @commands.has_permissions(manage_channels=True)
    @slash_command(description='👋 Sets the server\'s welcome/join message channel.')
    async def joins(self, ctx,
        channel: discord.commands.Option(discord.TextChannel, 'Welcome Message Channel', required=False, default=None),
        style: discord.commands.Option(str, 'Style of the image (Optional)', required=False, default='join'),
        text: discord.commands.Option(str, 'Additional text (Optional)', required=False, default='Make sure to read and accept the rules.'),
    ):

        join_channels_config = config.load('join_channels')
        join_channels_config[ctx.guild.id] = {'channel': channel.id if channel else None, 'style': style, 'text': text, 'details': 'Have fun!'}
        config.save(join_channels_config, 'join_channels')

        await ctx.respond(embed=discord.Embed(title='Alright!', description=f'The welcome message channel is now set to {channel.name if channel else "no channel"}.\nBy the way, you can only have 1 join **and** 1 leave channel at the time. (If you don\'t get it: you can have 1 joinchannel and 1 leavechannel per server, but you **can** use the same channel for both join **and** leave.)', color=management.color()).set_footer(text='Use /channels to view the channel settings.'))

    @commands.has_permissions(manage_channels=True)
    @slash_command(description='😞 Sets the server\'s leave message channel.')
    async def leaves(self, ctx,
        channel: discord.commands.Option(discord.TextChannel, 'Leave Message Channel', required=False, default=None),
        style: discord.commands.Option(str, 'Style of the image (Optional)', required=False, default='leave'),
        text: discord.commands.Option(str, 'Additional text (Optional)', required=False, default='I hope you had fun :\')'),
    ):

        leave_channels_config = config.load('leave_channels')
        leave_channels_config[ctx.guild.id] = {'channel': channel.id if channel else None, 'style': style, 'text': text, 'details': 'Goodbye!'}
        config.save(leave_channels_config, 'leave_channels')

        await ctx.respond(embed=discord.Embed(title='Alright!', description=f'The leave message channel is now set to {channel.name if channel else "no channel"}.\nBy the way, you can only have 1 join **and** 1 leave channel at the time. (If you don\'t get it: you can have 1 joinchannel and 1 leavechannel per server, but you **can** use the same channel for both join **and** leave.)', color=management.color()).set_footer(text='Use /channels to view the channel settings.'))

def setup(client):
    client.add_cog(JoinLeave(client))
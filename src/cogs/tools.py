try:
    from .helpers import config, management
except ImportError:
    import helpers.config, helpers.management

import discord.commands

from discord.ext import commands
from discord.commands import slash_command, message_command

class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(send_messages=True)
    @slash_command(description='💬 Sends a message into the channel.')
    async def send(self, ctx, message: discord.commands.Option(str, 'The message text')):
        embed = discord.Embed(title=message, color=management.color())
        embed.set_footer(text=f'Sent by {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @commands.has_permissions(add_reactions=True)
    @slash_command(description='😀 Reacts to the last message in the channel.')
    async def react(self, ctx, emoji: discord.commands.Option(str, 'The emoji to react with')):
        embed = discord.Embed(
            title='Alright!',
            description=f'I just reacted with {emoji}.',
            color=management.color(),
        )

        async for message in ctx.channel.history(limit=1):
            await message.add_reaction(emoji)
        await ctx.respond(embed=embed)

    @slash_command(description='📜 Lists which channels have special features, e.g. join messages.')
    async def channels(self, ctx):
        def find(config_name: str):
            try:
                return discord.utils.get(ctx.guild.channels, id=config.load(config_name)[ctx.guild.id]['channel']).mention
            except:
                return 'Not set'
        
        embed = discord.Embed(
            title='Special Channels',
            description= f'''
**Join Channel** (`/joins`): {find('join_channels')}
**Leave Channel** (`/leaves`): {find('leave_channels')}
**Chatbot Channel** (`/chatbot`): {find('chatbot_channels')}
''',
            color=management.color(),
        )

        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Tools(client))
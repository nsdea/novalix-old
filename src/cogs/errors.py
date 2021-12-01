try:
    from .helpers import config, management
except ImportError:
    import helpers.config, helpers.management

import discord
import traceback

from discord.ext import commands
from discord.commands import slash_command

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        error_message = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        error_message = error_message.split('\n\nThe above exception was the direct cause of the following exception:')[0]

        embed = discord.Embed(
            title='Command Error',
            description=f'```py\n{error_message[:4050]}```',
            color=management.color('error')
        )

        if len(error_message) > 4050:
            embed.set_footer(text=f'Only showing first 4050 instead of the total {len(error_message)} characters of the error message.')

        try:
            await ctx.respond(embed=embed)
        except:
            await ctx.send(embed=embed)

        if management.testing_mode():
            raise error # if this is a testing system, show the full error in the console

def setup(client):
    client.add_cog(Errors(client))
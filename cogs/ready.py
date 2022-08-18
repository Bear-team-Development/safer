from discord.ext import commands
import discord


class ready(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("Ready")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("------")


def setup(bot):
    bot.add_cog(ready(bot))

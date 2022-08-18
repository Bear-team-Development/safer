from discord.ext import commands
import discord
from discord.commands import slash_command, ApplicationContext


class safe_check(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @slash_command(description="檢查安全建議")
    async def safecheck(self, ctx: ApplicationContext):
        if ctx.author.guild_permissions.administrator:
            warn = []
            if ctx.guild.default_role.permissions.mention_everyone:
                warn.append("危險：所有人可以tag everyone")
            verification_level = ctx.guild.verification_level
            if verification_level == discord.VerificationLevel.none:
                warn.append("危險：驗證等級為無")
            elif verification_level == discord.VerificationLevel.low:
                warn.append("注意：驗證等級過低")
            if ctx.guild.mfa_level == 0:
                warn.append("提醒：兩步驟驗證未開啟")
            if ctx.guild.nsfw_level == 0:
                warn.append("提醒：年齡限制過濾器未開啟")
            embed = discord.Embed(title="安全建議", color=discord.Color.red())

            if len(warn):
                for i in warn:
                    embed.add_field(name=i, value="\u200b", inline=False)
            else:
                embed.add_field(name="未發現問題", value="恭喜，你的伺服器很安全", inline=False)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("你沒有權限")


def setup(bot):
    bot.add_cog(safe_check(bot))

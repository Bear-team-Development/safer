from discord.ext import commands
import discord
from utils.anti_nuke import anti_nuke


class safe(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, _: discord.Member) -> None:
        await anti_nuke(guild, discord.AuditLogAction.ban)

    @commands.Cog.listener()
    async def on_emoji_update(self, emoji: discord.Emoji) -> None:
        await anti_nuke(emoji.guild, discord.AuditLogAction.emoji_update)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, _: discord.Member) -> None:
        await anti_nuke(guild, discord.AuditLogAction.unban)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.channel) -> None:
        await anti_nuke(channel.guild, discord.AuditLogAction.channel_create)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.channel) -> None:
        await anti_nuke(channel.guild, discord.AuditLogAction.channel_delete)

    @commands.Cog.listener()
    async def on_member_kick(self, member: discord.Member) -> None:
        await anti_nuke(member.guild, discord.AuditLogAction.kick)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        await anti_nuke(role.guild, discord.AuditLogAction.role_create)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await anti_nuke(role.guild, discord.AuditLogAction.role_delete)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, _: discord.Guild) -> None:
        await anti_nuke(before, discord.AuditLogAction.guild_update)


def setup(bot):
    bot.add_cog(safe(bot))

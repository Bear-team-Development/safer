import discord
import utils.score as score


async def anti_nuke(guild: discord.Guild, action: discord.AuditLogAction) -> None:

    logs = await guild.audit_logs(limit=1, action=action).flatten()
    logs = logs[0]
    s = score.get_score(logs.user, guild)
    if s >= 4:
        try:
            await logs.user.send(f"你被炸群偵測到了")
        except:
            pass

        await logs.user.ban(reason=f"炸群偵測")
    else:
        score.add_score(logs.user, guild)

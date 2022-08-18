import redis, discord

r = redis.Redis(host="localhost", port=6379, db=0)


def get_score(user: discord.User, guild: discord.Guild) -> int:
    res = r.get(f"{guild.id}:{user.id}")
    if res is None:
        return 0
    else:
        return int(res)


def set_score(user: discord.User, guild: discord.Guild, score: int) -> None:
    r.set(f"{guild.id}:{user.id}", score)
    r.expire(f"{guild.id}:{user.id}", 2)


def add_score(user: discord.User, guild: discord.Guild, score: int = 1) -> None:
    if get_score(user, guild) is None:
        set_score(user, guild, score)
    else:
        r.incrby(f"{guild.id}:{user.id}", score)
        r.expire(f"{guild.id}:{user.id}", 2)

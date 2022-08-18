import dotenv
from glob import glob
import os

dotenv.load_dotenv()

import discord
from threading import Thread


bot = discord.Bot(intents=discord.Intents.all())


for path in glob("cogs/*.py"):
    bot.load_extension(f"cogs.{path[5:-3]}")
if __name__ == "__main__":
    t = Thread(target=os.system, args=("redis-server",))
    t.start()

    bot.run(os.environ["token"])

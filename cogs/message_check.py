import os
from discord.ext import commands
from datetime import datetime, timedelta
import discord
from nsfw_detector import predict
import aiohttp
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
import json

model = predict.load_model("./nsfw_mobilenet2.224x224.h5")


class message_check(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:

        self.bot = bot
        with open("scam.json", "r") as f:
            self.scam = set(json.load(f))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if len(re.findall("[\w-]{24}\.[\w-]{6}\.[\w-]{27}", message.content)) > 0:
            print("Token found")
            await message.delete()
            await message.channel.send(f"{message.author.mention}你的訊息中含有token")
            return

        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

        matches = re.findall(regex, message.content)
        for metch in matches:

            metch = urlparse(metch).netloc

            if metch in self.scam:
                print(message.content)
                await message.delete()
                await message.channel.send(f"{message.author.mention}你輸入了詐騙連接")
                try:
                    await message.author.timeout(
                        datetime.utcnow() + timedelta(30), reason="詐騙連結"
                    )
                except:
                    pass
                break
        if not message.channel.is_nsfw():
            for attachment in message.attachments:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as response:
                        tmp_file = await response.read()
                        with open("tmp/tmp.jpg", "wb") as f:
                            f.write(tmp_file)

                prediction = predict.classify(model, "tmp/tmp.jpg")
                if (
                    prediction["tmp/tmp.jpg"]["sexy"]
                    + prediction["tmp/tmp.jpg"]["porn"]
                    >= 0.5
                ):
                    await message.channel.send(f"{message.author.mention} 請勿發送色情圖片")
                    try:
                        await message.author.timeout(
                            datetime.utcnow() + timedelta(30), reason=""
                        )
                    except:
                        pass

    @commands.Cog.listener()
    async def on_message_edit(self, _, message: discord.Message) -> None:

        if len(re.findall("[\w-]{24}\.[\w-]{6}\.[\w-]{27}", message.content)) > 0:
            print("Token found")
            await message.delete()
            await message.channel.send(f"{message.author.mention}你的訊息中含有token")
            return

        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

        matches = re.findall(regex, message.content)
        for metch in matches:

            metch = urlparse(metch).netloc

            if metch in self.scam:
                print(message.content)
                await message.delete()
                await message.channel.send(f"{message.author.mention}你輸入了詐騙連接")
                try:
                    await message.author.timeout(
                        datetime.utcnow() + timedelta(30), reason="詐騙連結"
                    )
                except:
                    pass
                break
        if not message.channel.is_nsfw():
            for attachment in message.attachments:
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as response:
                        tmp_file = await response.read()
                        with open("tmp/tmp.jpg", "wb") as f:
                            f.write(tmp_file)

                prediction = predict.classify(model, "tmp/tmp.jpg")
                if (
                    prediction["tmp/tmp.jpg"]["sexy"]
                    + prediction["tmp/tmp.jpg"]["porn"]
                    >= 0.5
                ):
                    await message.channel.send(f"{message.author.mention} 請勿發送色情圖片")
                    try:
                        await message.author.timeout(
                            datetime.utcnow() + timedelta(30), reason=""
                        )
                    except:
                        pass


def setup(bot):
    bot.add_cog(message_check(bot))

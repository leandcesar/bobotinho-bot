# -*- coding: utf-8 -*-
from datetime import datetime

from bobotinho.bot import Bot, Context, Message, command, commands
from bobotinho.apis import Discord
from bobotinho.models import Bug, Suggest


class Pyramid:
    def __init__(self) -> None:
        self.init()

    def init(self, user: str = "", word: str = "", count: int = 0) -> bool:
        self.user = user
        self.word = word
        self.i = self.max = count
        self.raising = True
        return False

    def increase(self) -> bool:
        self.i += 1
        self.max += 1
        self.raising = True
        return False

    def decrease(self) -> bool:
        self.i -= 1
        self.raising = False
        return bool(self.i <= 1 and self.max >= 3)

    def update(self, message: Message) -> bool:
        parts = message.content.strip().split()
        word = parts[0]
        count = parts.count(word)
        is_pattern = (len(parts) == count)
        is_same = (self.user == message.author.name and self.word == word)
        if not is_pattern:
            return self.init()
        if is_same and self.raising and (count == self.i + 1):
            return self.increase()
        if is_same and (count == self.i - 1):
            return self.decrease()
        if (count == 1):
            return self.init(message.author.name, word, 1)
        return self.init()


class General(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.boot = datetime.utcnow()

    @property
    def boot_ago(self) -> str:
        time = datetime.utcnow() - self.boot
        hours, remainder = divmod(time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{int(hours)}h"
        if minutes:
            return f"{int(minutes)}min"
        return f"{int(seconds)}s"

    @command(aliases=["bot", "info"])
    async def botinfo(self, ctx: Context) -> None:
        ctx.response = (
            f"estou conectado à {len(ctx.bot.channels)} canais, "
            f"com {len(ctx.bot.commands)} comandos, "
            f"feito por @{ctx.bot.config.dev} em Python (Twitchio) e hospedado em Heroku"
        )

    @command(aliases=["commands"])
    async def help(self, ctx: Context) -> None:
        ctx.response = f"veja todos os comandos em {ctx.bot.config.site_url}/docs/help"

    @command(aliases=["add"])
    async def invite(self, ctx: Context) -> None:
        ctx.response = f"me adicione no seu chat em {ctx.bot.config.site_url}/invite"

    @command()
    async def news(self, ctx: Context) -> None:
        ctx.response = f"para ver as novidades, entre no servidor do Discord em {ctx.bot.config.site_url}/discord"

    @command(aliases=["pong"])
    async def ping(self, ctx: Context) -> None:
        ctx.response = "pong 🏓"

    @command(aliases=["discord", "github", "twitter"])
    async def site(self, ctx: Context) -> None:
        ctx.response = f"acesse {ctx.bot.config.site_url}"

    @command()
    async def uptime(self, ctx: Context) -> None:
        ctx.response = f"eu acordei há {self.boot_ago}"

    @command(usage="digite o comendo e explique detalhadamente o bug que você encontrou")
    async def bug(self, ctx: Context, *, content: str) -> None:
        bug = await Bug.create(author=ctx.author.name, source=ctx.channel.name, content=content)
        ctx.response = f"seu bug foi reportado 🐛 (ID {bug.id})"
        if self.bot.config.bugs_url:
            data = {
                "title": f"Bug #{bug.id:04}",
                "description": bug.content,
                "color": self.bot.config.color,
                "author_name": bug.author,
                "footer_text": bug.source,
                "timestamp": bug.updated_at,
            }
            await Discord.webhook(self.bot.config.bugs_url, data)

    @command(
        aliases=["suggestion"],
        usage="digite o comando e uma sugestão de recurso ou modificação para o bot",
    )
    async def suggest(self, ctx: Context, *, content: str) -> None:
        suggest = await Suggest.create(author=ctx.author.name, source=ctx.channel.name, content=content)
        ctx.response = f"sua sugestão foi anotada 📝 (ID {suggest.id})"
        if self.bot.config.suggestions_url:
            data = {
                "title": f"Sugestão #{suggest.id:04}",
                "description": suggest.content,
                "color": self.bot.config.color,
                "author_name": suggest.author,
                "footer_text": suggest.source,
                "timestamp": suggest.updated_at,
            }
            await Discord.webhook(self.bot.config.suggestions_url, data)

    @commands.Cog.event("event_message")
    async def pyramid(self, message: Message) -> None:
        if message.echo:
            return None
        if not self.bot.channels[message.channel.name].get("pyramid"):
            self.bot.channels[message.channel.name]["pyramid"] = Pyramid()
        if self.bot.channels[message.channel.name]["pyramid"].update(message):
            pyramid = self.bot.channels[message.channel.name]["pyramid"]
            response = f"você fez uma pirâmide de {pyramid.max} {pyramid.word}"
            await message.channel.send(f"{message.author.name}, {response}")


def prepare(bot: Bot) -> None:
    bot.add_cog(General(bot))

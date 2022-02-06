# -*- coding: utf-8 -*-
from bobotinho.bot import Bot, Context, command, commands, exceptions
from bobotinho.models import Channel


class Settings(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if not ctx.author.is_mod and ctx.author.name not in (ctx.channel.name, self.bot.config.dev):
            raise exceptions.ModRequired
        return True

    @command(usage="digite o comando e um termo que eu não possa dizer")
    async def banword(self, ctx: Context, *, word: str) -> None:
        if word in self.bot.channels[ctx.channel.name]["banwords"]:
            ctx.response = "esse já é um termo banido"
        else:
            self.bot.channels[ctx.channel.name]["banwords"].append(word)
            channel = await Channel.get(user_id=self.bot.channels[ctx.channel.name]["id"])
            channel.banwords[word] = ctx.author.id
            await channel.save()
            ctx.response = "não irei mais enviar mensagens que tiverem esse termo"

    @command(usage="digite o comando e um termo que deseja desbanir")
    async def unbanword(self, ctx: Context, *, word: str) -> None:
        if word in self.bot.channels[ctx.channel.name]["banwords"]:
            self.bot.channels[ctx.channel.name]["banwords"].remove(word)
            channel = await Channel.get(user_id=self.bot.channels[ctx.channel.name]["id"])
            channel.banwords.pop(word)
            await channel.save()
            ctx.response = f'"{word}" foi removido dos termos banidos'
        else:
            ctx.response = f'"{word}" não é um termo banidos'

    @command(usage="digite o comando e o nome do comando que deseja reativar")
    async def enable(self, ctx: Context, command: str) -> None:
        command = self.bot.get_command(command)
        if not command:
            ctx.response = "esse comando não existe"
        elif command.name in self.bot.channels[ctx.channel.name]["disabled"]:
            self.bot.channels[ctx.channel.name]["disabled"].remove(command.name)
            channel = await Channel.get(user_id=self.bot.channels[ctx.channel.name]["id"])
            channel.disabled.pop(command.name)
            await channel.save()
            ctx.response = f'"{command.name}" foi reativado'
        else:
            ctx.response = f'"{command.name}" já está ativado'

    @command(usage="digite o comando e o nome do comando que deseja desativar")
    async def disable(self, ctx: Context, command: str) -> None:
        command = self.bot.get_command(command)
        if not command:
            ctx.response = "esse comando não existe"
        elif command.name in ("disable", "enable", "start", "stop"):
            ctx.response = f'"{command.name}" não pode ser desativado'
        elif command.name in self.bot.channels[ctx.channel.name]["disabled"]:
            ctx.response = f'"{command.name}" já está desativado'
        else:
            self.bot.channels[ctx.channel.name]["disabled"].append(command.name)
            channel = await Channel.get(user_id=self.bot.channels[ctx.channel.name]["id"])
            channel.disabled[command.name] = ctx.author.id
            await channel.save()
            ctx.response = f'"{command.name}" foi desativado'

    @command()
    async def start(self, ctx: Context) -> None:
        if self.bot.self.bot.channels[ctx.channel.name]["online"]:
            ctx.response = "já estou ligado ☕"
        else:
            self.bot.channels[ctx.channel.name]["online"] = True
            await Channel.filter(user_id=self.bot.channels[ctx.channel.name]["id"]).update(online=True)
            ctx.response = "você me ligou ☕"

    @command()
    async def stop(self, ctx: Context) -> None:
        self.bot.channels[ctx.channel.name]["online"] = False
        await Channel.filter(user_id=self.bot.channels[ctx.channel.name]["id"]).update(online=False)
        ctx.response = "você me desligou 💤"


def prepare(bot: Bot) -> None:
    bot.add_cog(Settings(bot))

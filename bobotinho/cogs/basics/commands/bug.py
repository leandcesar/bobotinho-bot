# -*- coding: utf-8 -*-
from bobotinho.apis import Discord
from bobotinho.database.models import Bug

description = "Reporte um bug que está ocorrendo no Bot"
usage = "digite o comando e o bug que você encontrou"


async def command(ctx, *, content: str):
    bug = await Bug.create(
        author=ctx.author.name,
        source=ctx.channel.name,
        content=content,
    )
    ctx.response = f"seu bug foi reportado 🐛 (ID {bug.id})"

    if url := ctx.bot.config.bugs_url:
        data = {
            "title": f"Bug #{bug.id:04}",
            "description": bug.content,
            "color": ctx.bot.config.color,
            "author_name": bug.author,
            "footer_text": bug.source,
            "timestamp": bug.updated_at,
        }
        await Discord.webhook(url, data)

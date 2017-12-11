import config
import discord
import datetime as dt
import pprint
import time
from error_handler import get_logger, logexcept
from models import LogMessage, LogEmbed, LogRevision, LogAttachment

cfg = config.botConfig()

client = discord.Client()

logger = get_logger('betterlogbot')

@client.event
async def on_ready():
    # Bots ready
    logger.info(f"{client.user.name} ({client.user.id}) is now online.")


@client.event
@logexcept
async def on_message(message):
    embeds = []
    for e in message.embeds:
        embeds.append(
            LogEmbed(
                title=e.title,
                type=e.type,
                description=e.description,
                url=e.url,
                timestamp=e.timestamp
            )
        )
    attachments = []
    for a in message.attachments:
        attachments.append(
            LogAttachment(
                attachid=a.id,
                size=a.size,
                height=a.height,
                width=a.width,
                filename=a.filename,
                url=a.url
            )
        )
    rev = LogRevision(
        content=message.content,
        timestamp=message.created_at
    )
    msg_item = Message(
        guild=message.guild.id,
        snowflake=message.id,
        author=message.author.id,
        channel=message.channel.id,
        revisions=[rev],
        embeds=embeds,
        attachments=attachments,
        pinned=message.pinned,
        tts = message.tts
    )
    msg_item.save()


@client.event
@logexcept
async def on_raw_message_edit(message_id, data):
    pp = pprint.PrettyPrinter(depth=4)
    logger.info(f"Message edited: {message_id}")
    pp.pprint(data)


@client.event
async def on_message_delete(message):
    pass

client.run(cfg.token)

import config
import discord
import datetime as dt
import time
from error_handler import get_logger
from models import *

cfg = config.botConfig()

client = discord.Client()

logger = get_logger('betterlogbot')

@client.event
async def on_ready():
    # Bots ready
    logger.info(f"{client.user.name} ({client.user.id}) is now online.")


@client.event
async def on_message(message):
    m, created = Message.get_or_create(
        snowflake=message.id,
        defaults={
            'author': message.author.id,
            'content': message.content
        }
    )


@client.event
async def on_message_delete(message):
    now = dt.datetime.utcnow()
    logger.info("Grabbing audit logs")
    entries = await message.guild.audit_logs(
        limit=1,
        action=discord.AuditLogAction.message_delete,
        after=(now - dt.timedelta(seconds=5))
    ).flatten()
    logger.info("Audit log get!")
    authorname = f"{message.author.name}#{message.author.discriminator}"
    if len(entries) > 0:
        entry = entries[0]
        deleter = f"{entry.user.name}#{entry.use.discriminator}"
        deleter_id = entry.user.id
    else:
        deleter = authorname
        deleter_id = message.author.id
    await client.get_channel(384194130894389249).send(
        f'Message from {authorname} deleted by {deleter}: {message.content}'
    )

    logger.info("Updating DB")
    m, created = Message.get_or_create(
        snowflake=message.id,
        defaults={
            'author': message.author.id,
            'content': message.content,
            'deleted': True,
            'deleted_by': deleter_id
        }
    )
    if not created:
        m.deleted = True
        m.save()

client.run(cfg.token)

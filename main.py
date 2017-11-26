import discord
from error_handler import get_logger
from models import *

client = discord.Client()

logger = get_logger('betterlogbot')

@client.event
async def on_ready():
    # Bots ready
    logger.info(f"{client.user.name} is now online.")


@client.event
async def on_message(message):
    m = Message.get_or_create(
        snowflake=message.id,
        defaults={
            'author': message.author.id,
            'content': message.content
        }
    )


@client.event
async def on_message_delete(message):
    entries = await message.guild.audit_log(
        limit=50,
        action=discord.AuditLogAction.message_delete
    )
    message = entries[0].target
    print(message)

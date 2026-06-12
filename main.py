"""
AI-Powered Discord Bot
=======================
A production-ready Discord bot built with discord.py.
Features slash commands, a modular cog architecture, AI chat via OpenAI,
and 24/7 deployment support.

Author: Lloyd
License: MIT
"""

import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Bot Setup
# ---------------------------------------------------------------------------

# Define required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="An AI-powered Discord bot with slash commands and modular architecture.",
)


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
@bot.event
async def on_ready():
    """Fired when the bot has connected and is ready."""
    logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)

    # Set a custom status
    activity = discord.Activity(
        type=discord.ActivityType.listening, name="/help for commands"
    )
    await bot.change_presence(activity=activity)

    # Load all cogs from the cogs/ folder
    cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
        logger.info("Created missing cogs directory: %s", cogs_dir)

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                logger.info("Loaded cog: %s", cog_name)
            except Exception as exc:
                logger.error("Failed to load cog %s: %s", cog_name, exc)

    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        logger.info("Synced %d slash command(s).", len(synced))
    except Exception as exc:
        logger.error("Failed to sync commands: %s", exc)

    logger.info("Bot is ready! Invite URL:")
    logger.info(
        "https://discord.com/api/oauth2/authorize?client_id=%s&permissions=274877975552&scope=bot%%20applications.commands",
        bot.user.id,
    )


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Global error handler for prefix commands."""
    if isinstance(error, commands.CommandNotFound):
        return  # Silently ignore unknown commands
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ I don't have the required permissions to do that.")
    else:
        logger.error("Unhandled command error: %s", error)
        await ctx.send("❌ Something went wrong. Please try again later.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    """Validate config and start the bot."""
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set!")

    bot.run(TOKEN, log_handler=None)  # log_handler=None since we configure our own


if __name__ == "__main__":
    main()

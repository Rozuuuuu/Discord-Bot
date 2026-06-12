"""
General Commands Cog
=====================
Basic utility and fun commands: ping, info, serverinfo, avatar.
"""

import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    """General-purpose slash commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ------------------------------------------------------------------
    # /ping — Latency check
    # ------------------------------------------------------------------
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency_ms}ms**",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

    # ------------------------------------------------------------------
    # /serverinfo — Show server details
    # ------------------------------------------------------------------
    @app_commands.command(name="serverinfo", description="Display information about this server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        embed.add_field(name="👑 Owner", value=str(guild.owner), inline=True)
        embed.add_field(name="👥 Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="💬 Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="🎭 Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
        embed.add_field(name="🆔 Server ID", value=str(guild.id), inline=True)
        await interaction.response.send_message(embed=embed)

    # ------------------------------------------------------------------
    # /avatar — Show a user's avatar
    # ------------------------------------------------------------------
    @app_commands.command(name="avatar", description="Display a user's avatar")
    @app_commands.describe(user="The user whose avatar you want to see (defaults to you)")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        embed = discord.Embed(
            title=f"🖼️ {target.display_name}'s Avatar",
            color=discord.Color.purple(),
        )
        embed.set_image(url=target.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ------------------------------------------------------------------
    # /help — Custom help command
    # ------------------------------------------------------------------
    @app_commands.command(name="help", description="Show all available commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Bot Commands",
            description="Here are all the commands you can use:",
            color=discord.Color.gold(),
        )
        embed.add_field(name="/ping", value="Check the bot's latency", inline=False)
        embed.add_field(name="/serverinfo", value="Display server information", inline=False)
        embed.add_field(name="/avatar [user]", value="Show a user's avatar", inline=False)
        embed.add_field(name="/ai <question>", value="Ask the AI anything", inline=False)
        embed.add_field(name="/help", value="Show this help message", inline=False)
        embed.set_footer(text="Built by Lloyd • Powered by discord.py")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """Called by bot.load_extension() to register this cog."""
    await bot.add_cog(General(bot))

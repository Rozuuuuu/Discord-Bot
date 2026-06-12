"""
AI Chat Cog
============
Integrates OpenAI GPT for intelligent conversational responses via /ai.
"""

import os
import discord
from discord import app_commands
from discord.ext import commands
import openai


class AIChat(commands.Cog):
    """AI-powered chat commands using OpenAI."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
        self.system_prompt = (
            "You are a helpful, friendly AI assistant inside a Discord server. "
            "Keep replies concise (under 300 words), well-formatted for Discord, "
            "and use markdown when appropriate."
        )

    # ------------------------------------------------------------------
    # /ai <question> — Ask the AI
    # ------------------------------------------------------------------
    @app_commands.command(name="ai", description="Ask the AI anything")
    @app_commands.describe(question="Your question for the AI")
    async def ai(self, interaction: discord.Interaction, question: str):
        if not self.client:
            await interaction.response.send_message(
                "⚠️ AI is not configured. The bot admin needs to set `OPENAI_API_KEY`.",
                ephemeral=True,
            )
            return

        # Defer the response — AI calls can take a few seconds
        await interaction.response.defer(thinking=True)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question},
                ],
                max_tokens=1024,
                temperature=0.7,
            )
            ai_reply = response.choices[0].message.content

            # Discord has a 2000-char limit; truncate if needed
            if len(ai_reply) > 1990:
                ai_reply = ai_reply[:1990] + "…"

            embed = discord.Embed(
                title="🤖 AI Response",
                description=ai_reply,
                color=discord.Color.blue(),
            )
            embed.set_footer(text=f"Asked by {interaction.user.display_name}")
            await interaction.followup.send(embed=embed)

        except openai.AuthenticationError:
            await interaction.followup.send(
                "⚠️ AI authentication failed. Please contact the bot admin."
            )
        except openai.RateLimitError:
            await interaction.followup.send(
                "⏳ The AI is busy right now. Please try again in a moment."
            )
        except Exception as exc:
            await interaction.followup.send(
                f"❌ Something went wrong: {exc}"
            )


async def setup(bot: commands.Bot):
    """Called by bot.load_extension() to register this cog."""
    await bot.add_cog(AIChat(bot))

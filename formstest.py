from discord.ext.forms import Form, ReactionForm
from discord.ext import commands
import discord
bot = commands.Bot(command_prefix="!")

@bot.command()
async def testform(ctx):
    form = Form(ctx,'Title')
    form.add_question('Question 1')
    form.add_question('Question 2')
    form.add_question('Question 3')

    result = await form.start()
    await ctx.send(f"```py\n{result}\n```")

@bot.command()
async def reactionform(ctx):
    embed=discord.Embed(title="Reaction Menu Test",description="Delete 20 messages?")
    message = await ctx.send(embed=embed)
    form = ReactionForm(message,bot,ctx.author)
    form.add_reaction("✅",True)
    form.add_reaction("❌",False)
    choice = await form.start()
    if choice:
        await ctx.channel.purge(limit=20)

bot.run('token')
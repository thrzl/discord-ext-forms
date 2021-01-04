#from discord.ext.forms import Form, ReactionForm, ReactionMenu
import discord.ext.forms as forms
from discord.ext import commands
import discord
bot = commands.Bot(command_prefix="!")

@bot.command()
async def testform(ctx):
    form = forms.Form(ctx,'Title')
    form.add_question('Question 1')
    form.add_question('Question 2')
    form.add_question('Question 3')

    result = await form.start()
    await ctx.send(f"```py\n{result}\n```")

@bot.command()
async def reactionform(ctx):
    embed=discord.Embed(title="Reaction Menu Test",description="Delete 20 messages?")
    message = await ctx.send(embed=embed)
    form = forms.ReactionForm(message,bot,ctx.author)
    form.add_reaction("✅",True)
    form.add_reaction("❌",False)
    choice = await form.start()
    if choice:
        await ctx.channel.purge(limit=20)

@bot.command()
async def reactionmenu(ctx):
    embed1=discord.Embed(description="This is embed1")
    embed2=discord.Embed(description="This is embed2")
    embed3=discord.Embed(description="This is embed3")
    rmenu = forms.ReactionMenu(ctx,[embed1,embed2,embed3])
    await rmenu.start()

bot.run('NzkxMjkwMDg1MzU3MTI1NjMz.X-NAUQ.ZycmgMWO56IegaE6fCdliUE5EVI')
#from discord.ext.forms import Form, ReactionForm, ReactionMenu
import discord.ext.forms as forms
from discord.ext import commands
import discord
bot = commands.Bot(command_prefix="!")

@bot.command()
async def test_form(ctx):
    form = forms.Form(ctx,'Title')
    form.add_question('Question 1')
    form.add_question('Question 2')
    form.add_question('Question 3')
    form.edit_and_delete(True)
    form.set_timeout(5)
    await form.set_color("#7289DA")
    result = await form.start()
    await ctx.send(f"```py\n{result}\n```")
    assert True

@bot.command()
async def test_reactions(ctx):
    embed=discord.Embed(title="Reaction Menu Test",description="Delete 20 messages?")
    message = await ctx.send(embed=embed)
    form = forms.ReactionForm(message,bot,ctx.author)
    form.add_reaction("✅",True)
    form.add_reaction("❌",False)
    choice = await form.start()
    if choice:
        await ctx.channel.purge(limit=20)
    assert True

@bot.command()
async def test_menu(ctx):
    embed1=discord.Embed(description="This is embed1")
    embed2=discord.Embed(description="This is embed2")
    embed3=discord.Embed(description="This is embed3")
    rmenu = forms.ReactionMenu(ctx,[embed1,embed2,embed3])
    await rmenu.start()
    assert True

bot.run('NzkxMjkwMDg1MzU3MTI1NjMz.X-NAUQ.iSo3rc17-wIBQcR1o8kZ0Uj7sJM')
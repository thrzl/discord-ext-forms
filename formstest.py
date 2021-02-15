#from discord.ext.forms import Form, ReactionForm, ReactionMenu
import discord.ext.forms as forms
from discord.ext import commands
import discord
bot = commands.Bot(command_prefix="!")

@bot.command()
async def testform(ctx):
    form = forms.Form(ctx,'Title')
    form.add_question('Give me an invite link!','invite','invite')
    form.add_question('Mention a Channel','channel','channel')
    form.add_question('Ping a User!','member','member')
    form.edit_and_delete(True)
    form.set_timeout(60)
    await form.set_color("#7289DA")
    print("Starting form...")
    result = await form.start()
    print("Completed form!")
    embed=discord.Embed(title="Data",description=f"Invite: {result.invite.guild}\nChannel: {result.channel.mention}\nMember: {result.member.mention}")
    await ctx.send(embed=embed)

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

bot.run('token')
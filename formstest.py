from discord.ext.forms.form import Validator
import discord.ext.forms as forms
from discord.ext import commands
import discord
bot = commands.Bot(command_prefix="!")

@bot.command()
async def testform(ctx):

    async def to_int(ctx, msg: discord.Message):
        try:
            return int(msg.content)
        except Exception as e:
            return False

    form = forms.Form(ctx, 'Title')
    form.add_question('Give me an invite link!', 'invite', Validator('invite'))
    form.add_question('Mention a Channel', 'channel', Validator('channel'))
    form.add_question('Ping a User!', 'member', Validator('member'))
    form.add_question('Give me a number!', 'number', to_int)
    form.add_question('How are you?', 'feels')
    form.edit_and_delete(True)
    form.set_timeout(60)
    await form.set_color("#7289DA")
    print("Starting form...")
    result = await form.start()
    print("Completed form!")
    embed=discord.Embed(title="Data", description=f"Invite: {result.invite.guild}\nChannel: {result.channel.mention}\nMember: {result.member.mention}\nNumber: `{result.number}`\n Feels: `{result.feels}`")
    await ctx.send(embed=embed)

@bot.command()
async def reactionform(ctx):
    embed=discord.Embed(title="Reaction Menu Test", description="Delete 20 messages?")
    message = await ctx.send(embed=embed)
    form = forms.ReactionForm(message, bot, ctx.author)
    form.add_reaction("✅", True)
    form.add_reaction("❌", False)
    choice = await form.start()
    if choice:
        await ctx.channel.purge(limit=20)

@bot.command()
async def reactionmenu(ctx):
    embed1=discord.Embed(description="This is embed1")
    embed2=discord.Embed(description="This is embed2")
    embed3=discord.Embed(description="This is embed3")
    rmenu = forms.ReactionMenu(ctx, [embed1, embed2, embed3])
    await rmenu.start()

bot.run('NzkxMjkwMDg1MzU3MTI1NjMz.X-NAUQ.9Wop9mq_7AsgXOcnkld4tAiKDiU')
from discord.ext.forms.form import Validator
import discord.ext.forms as forms
from discord import Client, app_commands, Object, Interaction
import discord
client = Client()

slash = app_commands.CommandTree(client)

TEST_GUILD = Object(758827653842075709)

@client.event
async def on_ready():
    print("ready")
    await slash.sync(guild=TEST_GUILD)



@slash.command(guild=TEST_GUILD, description="test")
async def testform(ctx):

    async def to_int(ctx, msg: discord.Message):
        try:
            return int(msg.content)
        except Exception as e:
            return False

    form = forms.Form(ctx, 'Title')
    form.add_question(question='Give me an invite link!', validator=Validator('invite'))
    form.add_question(question='Mention a Channel', validator=Validator('channel'))
    form.add_question(question='Ping a User!', validator=Validator('member'))
    form.add_question(question='Give me a number!', validator=to_int)
    form.add_question(question='How are you?')
    
    result = await form.start()
    
    embed=discord.Embed(title="Data", description=f"Here's the data you gave me! \n {chr(10).join([i.answer for i in result])}")
    await ctx.send(embed=embed)

@slash.command()
async def reactionform(ctx):
    embed=discord.Embed(title="Reaction Menu Test", description="Delete 20 messages?")
    message = await ctx.send(embed=embed)
    form = forms.ReactionForm(message, client, ctx.author)
    form.add_reaction("✅", True)
    form.add_reaction("❌", False)
    choice = await form.start()
    if choice:
        await ctx.channel.purge(limit=20)

@slash.command()
async def reactionmenu(ctx: Interaction):
    embed1=discord.Embed(description="This is embed1")
    embed2=discord.Embed(description="This is embed2")
    embed3=discord.Embed(description="This is embed3")
    rmenu = forms.ReactionMenu(ctx, [embed1, embed2, embed3])
    await rmenu.start()

client.run()
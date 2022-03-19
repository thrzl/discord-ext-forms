from discord.ext.forms.buttons import ButtonForm
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

@slash.command(guild=TEST_GUILD, description="test button")
async def reactionform(interaction: Interaction):
    embed=discord.Embed(title="Reaction Menu Test", description="Delete 20 messages?")
    form = ButtonForm(embed=embed, interaction=interaction)
    form.add_button(custom_id="confirm", emoji="✅", text="confirm", result=True, style=discord.ButtonStyle.green)
    form.add_button(custom_id="deny", emoji="❌", text="confirm", result=False, style=discord.ButtonStyle.red)
    choice, inter = await form.start()
    print(choice)
    if choice:
        await interaction.channel.purge(limit=20)
    else:
        await inter.response.send_message(content="Action Cancelled.", embed=embed)

@slash.command()
async def reactionmenu(ctx: Interaction):
    embed1=discord.Embed(description="This is embed1")
    embed2=discord.Embed(description="This is embed2")
    embed3=discord.Embed(description="This is embed3")
    rmenu = forms.ReactionMenu(ctx, [embed1, embed2, embed3])
    await rmenu.start()

client.run()
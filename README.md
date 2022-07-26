
## Example:
```py
from discord.ext.forms import Form
from discord.ext import commands
bot = commands.Bot(command_prefix="!")

@bot.command()
async def testform(ctx):
    channel, user = ctx.channel, ctx.author
    form = Form(ctx,'Title', channel=channel, client=user, bot=bot)
    form.add_question('Question 1','first')
    form.add_question('Question 2','second')
    form.add_question('Question 3','third')
    result = await form.start()
    return result

>> result.first
"This was my response to question 1"

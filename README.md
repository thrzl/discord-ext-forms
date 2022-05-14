# discord-ext-forms
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/isigebengu-mikey/discord-ext-forms/LICENSE)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![Downloads](https://pepy.tech/badge/discord-ext-forms)](https://pepy.tech/project/discord-ext-forms)
[![Code of Conduct](https://img.shields.io/badge/code%20of-conduct-ff69b4.svg?style=flat)](https://github.com/isigebengu-mikey/discord-ext-forms/CODE_OF_CONDUCT.md)
![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)



### An easier way to make forms and surveys in discord.​py.
This module is a very simple way to ask questions and create complete forms in discord.py without using an entire 30 lines!

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
```
![Example GIF](https://mikey.has-no-bra.in/9NoRXO.gif)
Using this module, you can make a 3 question form with only 5 lines of code.

## Links
### [How To Contribute](contribute.md)
### [Changelog](CHANGELOG.md)
### [Code of Conduct](CODE_OF_CONDUCT.md)

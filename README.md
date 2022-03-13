# discord-ext-forms
[![mit license](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/isigebengu-mikey/discord-ext-forms/license)
[![pr's welcome](https://img.shields.io/badge/prs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![downloads](https://pepy.tech/badge/discord-ext-forms)](https://pepy.tech/project/discord-ext-forms)
[![code of conduct](https://img.shields.io/badge/code%20of-conduct-ff69b4.svg?style=flat)](https://github.com/isigebengu-mikey/discord-ext-forms/code_of_conduct.md)
![github last commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat)
[![open source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)



### an easier way to make forms and surveys in discord.​py.
this module is a very simple way to ask questions and create complete forms in discord.py without using an entire 30 lines!

## example:
```py
from discord.ext.forms import form
from discord.ext import commands
bot = commands.bot(command_prefix="!")

@bot.command()
async def testform(ctx):
    form = form(ctx,'title')
    form.add_question('question 1','first')
    form.add_question('question 2','second')
    form.add_question('question 3','third')
    result = await form.start()
    return result

>> result.first
"this was my response to question 1"
```
![example gif](https://mikey.has-no-bra.in/9NoRXO.gif)
using this module, you can make a 3 question form with only 5 lines of code.

## links
### [how to contribute](contribute.md)
### [changelog](changelog.md)
### [code of conduct](code_of_conduct.md)

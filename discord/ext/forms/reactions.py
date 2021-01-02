import typing
from discord.ext import commands
import discord
from typing import List
import re
class ReactionForm(object): # I don't like subclassing shut up
    """
    The Reaction input object.

    ...

    Parameters
    ----------
    message : discord.Message
        The context of the form object. If it is none, the `channel` attribute is required in the `start` method.

    bot : typing.Union[discord.CLient, discord.ext.commands.Bot]
        The bot being used for the form.
    """
    def __init__(self, message:discord.Message, bot: typing.Union[discord.Client, commands.Bot]):
        self._msg = message
        self._bot = bot
        self._reactions = {}
        self.timeout = 120

    def set_timeout(self,timeout:int) -> None:
        self.timeout = timeout

    def add_reaction(self,reaction:discord.Emoji,result) -> dict:
        """Adds a question to the form.

        Returns the full list of questions the form has, including the newly added one. The questions are held
        in dictionaries containing the `question` and optionally `type` keys. The `question` key contains the
        question as a string, and the `type` key contains the input validation (if any is specified)
        """
        self._reactions[reaction] = result
        return self._reactions

    async def set_color(self,color) -> None:
        """Sets the color of the form embeds."""
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str)
        if not match:
            raise InvalidColor("")
        self._color = color

    async def start(self,channel=None) -> List[dict]:
        """Starts the form in the specified channel. If none is specified, the channel will be fetched from the `context` parameter of the form's initialization."""
        elist = []
        answers = []
        if not channel:
            channel = self._ctx.channel
        for q in self._questions:
            embed=discord.Embed(description=q['question'])
            embed.set_author(name=f"{self.title}: {self._questions.index(q)+1}/{len(self._questions)}",icon_url=self._bot.user.avatar_url)
            if self._color:
                embed.color=self._color
            elist.append(embed)
        prompt = None
        for embed in elist:
            if self.editanddelete:
                if not prompt:
                    prompt = await self._ctx.channel.send(embed=embed)
                else:
                    await prompt.edit(embed=embed)
            else:
                prompt = await self._ctx.channel.send(embed=embed)
            def check(m):
                return m.channel == prompt.channel and m.author == self._ctx.author
            question = [x for x in self._questions if x['question'] == embed.description]
            question = question[0]
            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
            question['answer'] = msg.content
            self._questions[self._questions.index(question)] = question
            if 'type' in question.keys(): # TODO: Add input validation
                #if question['type'] == 'invite'
                pass
        return self._questions

class InvalidColor(Exception):
    pass
import discord
from discord.ext import commands
from typing import List
class Form(object):
    """
    The base form object.

    ...

    Parameters
    ----------
    ctx : discord.Context
        The context of the form object. If it is none, the `channel` attribute is required in the `start` method.

    title : str
        The title of the form.

    """
    def __init__(self, ctx:commands.Context, title):
        self._ctx = ctx
        self._bot = ctx.bot
        self._questions = []
        self.title = title
        self.timeout = 120
        self.editanddelete = False
        self.color = None

    def set_timeout(self,timeout:int) -> None:
        self.timeout = timeout

    def add_question(self,question,qtype=None) -> List[dict]:
        """Adds a question to the form.

        Returns the full list of questions the form has, including the newly added one. The questions are held
        in dictionaries containing the `question` and optionally `type` keys. The `question` key contains the
        question as a string, and the `type` key contains the input validation (if any is specified)
        """
        dictionary = {'question':question}
        if qtype:
            if qtype.lower() == 'invite':
                pass
            elif qtype.lower() == 'channel':
                pass
            elif qtype.lower() == 'user':
                pass
            else:
                raise InvalidFormType(f"Type '{qtype}' is invalid!")
            dictionary['type'] = qtype
        self._questions.append(dictionary)
        return self._questions

    def edit_and_delete(self,choice:bool=None) -> bool:
        """Set's whether the bot should edit the prompt and delete the input messages. """
        if choice == None:
            if self.editanddelete == True:
                self.editanddelete = False
                return False
            else:
                self.editanddelete = True
                return True
        else:
            self.editanddelete = choice

    async def set_color(self,color:discord.Color) -> None:
        """Sets the color of the form embeds."""
        try:
            color = await commands.ColorConverter().convert(self._ctx,color)
        except Exception as e:
            raise InvalidColor(e)
        self.color = color

    async def start(self,channel=None) -> List[dict]:
        """Starts the form in the specified channel. If none is specified, the channel will be fetched from the `context` parameter of the form's initialization."""
        elist = []
        answers = []
        if not channel:
            channel = self._ctx.channel
        for q in self._questions:
            embed=discord.Embed(description=q['question'])
            embed.set_author(name=f"{self.title}: {self._questions.index(q)+1}/{len(self._questions)}",icon_url=self._bot.user.avatar_url)
            if self.color:
                embed.color=self.color
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

class InvalidFormType(Exception):
    """The exception raised when a form type is invalid."""
    pass

class InvalidColor(Exception):
    """The exception raised when the color type is invalid."""
    pass
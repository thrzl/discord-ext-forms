import discord
from discord.ext import commands
from typing import List
class Form(object):
    """The basic form object.

    Parameters:
    -----------

        ctx (discord.ext.commands.Context): The context of the form.

        title (str): The title of the form.
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
        """Sets the timeout for the form.

        Parameters
        ----------

            timeout (int): The timeout to be used.
        """        
        self.timeout = timeout

    def add_question(self,question,qtype=None) -> List[dict]:
        """Adds a question to the form.

        Parameters
        ----------
        question : str
            The question as a string that should be added.

        qtype : str, optional
            The input validation to be used (incomplete), by default None

        Returns
        -------
        List[dict]
            A list of all of the questions, stored as dictionaries.

        Raises
        ------
        InvalidFormType

            Is raised when the input validation type is invalid.

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
        """Toggles the edit and delete feature.

        Parameters
        ----------
        choice : bool, optional
            Whether you want the bot to edit the prompt and delete the input or not. If none, it toggles. The default for edit and delete is off. Default input is `None`

        Returns
        -------
        bool
            The state of edit and delete (after this is completed)
        """
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
        """Sets the color of the embed used for the form's embeds.

        Parameters
        ----------
        color : discord.Color
            The color to be used.

        Raises
        ------
        InvalidColor
            Is raised if the color is invalid or incorrect.
        """
        try:
            color = await commands.ColorConverter().convert(self._ctx,color)
        except Exception as e:
            raise InvalidColor(e)
        self.color = color

    async def start(self,channel=None) -> List[dict]:
        """Starts the form in the current channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to open the form in. If none, it is gotten from the context object set during initialization.

        Returns
        -------
        List[dict]
            [description]
        """        
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
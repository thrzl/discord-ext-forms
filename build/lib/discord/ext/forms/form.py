import discord
from discord.ext import commands
import re
from typing import List
import json

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
        self._questions = {}
        self.title = title
        self.timeout = 120
        self.editanddelete = False
        self.color = None
        self._incorrectmsg = None
        self._retrymsg = None
        self._tries = None

    def set_timeout(self,timeout:int) -> None:
        """Sets the timeout for the form.

        Parameters
        ----------

            timeout (int): The timeout to be used.
        """
        self.timeout = timeout

    def set_tries(self,tries:int) -> None:
        """Set the amount of tries that are allowed during input validation. Defaults to 3.

        Parameters
        ----------
        tries : int
            The number of tries to set.
        """
        int(tries)
        self._tries = tries

    def add_question(self,question,key:str=None,qtype=None) -> List[dict]:
        """Adds a question to the form.
        The valid qtypes are:
        `invite`,`channel`,`user`,`member`,`role`, and `category`

        Parameters
        ----------
        question : str
            The question as a string that should be added.

        key : str, optional
            The prefered key to be used. If none, defaults to the to the question. By default None.

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
        if not key:
            key = question
        valid_qtypes = ['invite','channel','user','member','role','category']
        dictionary = {'res':None,'type':None,'question':question}
        if qtype:
            if qtype.lower() not in valid_qtypes:
                raise InvalidFormType(f"Type '{qtype}' is invalid!")

            dictionary['type'] = qtype
            self._tries = 3

        self._questions[key] = dictionary
        self.set_incorrect_message('You answered incorrectly too many times. Please try again.')
        self.set_retry_message(f'Please try again.')
        return self._questions

    async def __validate_input(self,qtype,answer):
        if qtype.lower() == 'invite':
            try:
                invite = await commands.InviteConverter().convert(self._ctx,answer)
                return invite
            except Exception as e:
                return False
        elif qtype.lower() == 'channel':
            try:
                channel = await commands.TextChannelConverter().convert(self._ctx,answer)
                return channel
            except:
                return False
        elif qtype.lower() == 'user':
            try:
                user = await commands.UserConverter().convert(self._ctx,answer)
                return user
            except:
                return False
        elif qtype.lower() == 'member':
            try:
                member = await commands.MemberConverter().convert(self._ctx,answer)
                return member
            except:
                return False
        elif qtype.lower() == 'role':
            try:
                role = await commands.RoleConverter().convert(self._ctx,answer)
                return role
            except:
                return False
        elif qtype.lower() == 'category':
            try:
                category = await commands.CategoryChannelConverter().convert(self._ctx,answer)
                return category
            except:
                return False
        elif qtype.lower() == 'emoji':
            try:
                emoji = await commands.EmojiConverter().convert(self._ctx,answer)
                return emoji
            except:
                return False
        else:
            self._tries -= 1
            raise InvalidFormType(f"Type '{qtype}' is invalid!")

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

    def set_retry_message(self,message:str):
        """Sets the message to send if input validation fails.

        Parameters
        ----------
        message : str
            The message to be set.
        """
        self._retrymsg = message

    def set_incorrect_message(self,message:str):
        """Sets the message to send if input validation fails and there are no more tries left..

        Parameters
        ----------
        message : str
            The message to be set.
        """
        self._incorrectmsg = message


    async def set_color(self,color:str) -> None:
        """Sets the color of the form embeds."""
        match = re.match(r'(0x|#)(\d|(f|F|d|D|a|A|c|C)){6}', str(color))
        if not match:
            raise InvalidColor(f"{color} is invalid. Be sure to use colors such as '0xffffff'")
        if color.startswith("#"):
            newclr = color.replace("#","")
            color = f"0x{newclr}"
        color = await commands.ColourConverter().convert(self._ctx,color)
        self._color = color

    async def start(self,channel=None) -> dict:
        """Starts the form in the current channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to open the form in. If none, it is gotten from the context object set during initialization.

        Returns
        -------
        dict
            A dictionary containing each question and its data.
            Example:
            ::

            {'Key Specified':{
                    'res':'answer goes here',
                    'type':'input validation type'
                    'question':'Question here'
                },
            'Next Key Specified':{
                'res':'answer goes here',
                'type':'input validation type'
                'question':'Question here'
            }
        """
        elist = []

        if not channel:
            channel = self._ctx.channel

        qlist = []
        for n, q in enumerate(self._questions.values()):
            embed=discord.Embed(description=q['question'],color=self._color)

            embed.set_author(name=f"{self.title}: {n+1}/{len(self._questions)}",icon_url=self._bot.user.avatar_url)

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
            question = None
            for x in self._questions.keys():
                nx = self._questions[x]
                if nx['question'] == embed.description:
                    question = x


            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
            ans = msg.content
            if self.editanddelete:
                await msg.delete()
            if self._tries:
                print("Tries found...")
                key = question
                question = self._questions[question]
                if 'type' in question.keys():
                    while True:
                        result = await self.__validate_input(question['type'],ans)
                        if result:
                            print("Input validation worked!")
                            nx = question
                            nx['res'] = result
                            self._questions[key] = nx
                            print(self._questions)
                                    #self._questions[x] = ans
                            #self._questions[question] = ans
                            break
                        else:
                            await channel.send(self._retrymsg+f" You have `{self._tries}` remaining.")
                            print("Input validation failed...")
                            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
                            ans = msg.content
                            if self.editanddelete:
                                await msg.delete()
            else:
                self._questions[question] = ans
        for i in self._questions.keys():
            self._questions[i] = self._questions[i]
        return self._questions

class InvalidColor(Exception):
    pass

class InvalidFormType(Exception):
    """The exception raised when a form type is invalid."""
    pass
import discord
import discord.ext.commands as commands
import re
import aiohttp
from typing import List
import typing
import json
from emoji import UNICODE_EMOJI

class FormResponse:
    def __init__(self,data:dict) -> None:
        for d in data.keys():
            if isinstance(data[d], dict):
                setattr(self,d,data[d]['res'])
            else:
                setattr(self,d,data[d])

class Form:
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
        self.color = 0x2F3136
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

        key : str
            What the attribute containing the answer should be called.

        qtype : str, optional
            The input validation to be used, by default None

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
        valid_qtypes = ['invite','channel','user','member','role','category','emoji']
        dictionary = {'res':None,'question':question}
        if qtype:
            dictionary['type'] = None
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
        elif qtype.lower() == 'category':
            try:
                category = await commands.CategoryChannelConverter().convert(self._ctx, answer)
                return category
            except Exception:
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
                try:
                    assert answer in UNICODE_EMOJI
                except:
                    return False
                return answer
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
        self.color = color

    async def start(self,channel=None) -> dict:
        """Starts the form in the current channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to open the form in. If none, it is gotten from the context object set during initialization.

        Returns
        -------
        FormResponse
            An object containing all of your keys as attributes.
        """
        elist = []

        if not channel:
            channel = self._ctx.channel

        qlist = []
        for n, q in enumerate(self._questions.values()):
            embed=discord.Embed(description=q['question'],color=self.color)

            embed.set_author(name=f"{self.title}: {n+1}/{len(self._questions)}",icon_url=self._bot.user.avatar_url)

            if self.color:
                embed.color=self.color

            elist.append(embed)


        prompt = None

        for embed in elist:
            ot = self._tries
            if self.editanddelete:
                if not prompt:
                    prompt = await channel.send(embed=embed)
                else:
                    await prompt.edit(embed=embed)

            else:
                prompt = await channel.send(embed=embed)

            def check(m):
                return m.channel == prompt.channel and m.author == self._ctx.author
            question = None
            for x in self._questions.keys():
                if self._questions[x]['question'].lower() == embed.description.lower():
                    question = x
                    nx = self._questions[x]

            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
            ans = msg.content
            if self.editanddelete:
                await msg.delete()
            key = question
            if 'type' in self._questions[question].keys():
                question = self._questions[question]
                if 'type' in question.keys():
                    while True:
                        result = await self.__validate_input(question['type'],ans)
                        if result:
                            nx = question
                            nx['res'] = result
                            self._questions[key] = nx
                                    #self._questions[x] = ans
                            #self._questions[question] = ans
                            break
                        else:
                            self._tries -= 1
                            await channel.send(self._retrymsg+f" You have `{self._tries}` remaining.",delete_after=3)
                            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
                            ans = msg.content
                            if self.editanddelete:
                                await msg.delete()
                else:
                    nx['res'] = ans
                    self._questions[key] = nx
            else:
                nx['res'] = ans
                self._questions[key] = nx
        for i in self._questions.keys():
            self._questions[i] = self._questions[i]
        return FormResponse(self._questions)

class ContextAndChannelMissing(Exception):
    pass

class NaiveForm:
    """The basic form object with naive validation. Should be used in scenarios where there is no context, such as reactions.

    Parameters:
    -----------

        title (str): The title of the form.

        channel (discord.TextChannel): The channel that the form should be sent to.

        bot (discord.ext.commands.Bot): The bot that will be running the form.
    """
    def __init__(self,  title, channel: typing.Union[discord.abc.PrivateChannel, discord.abc.GuildChannel], bot: commands.Bot):
        self._channel = channel
        self._bot = bot
        self._questions = {}
        self.title = title
        self.timeout = 120
        self.editanddelete = False
        self.color = 0x2F3136
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
        `invite`,`channel`,`member`,`role`, and `emoji`

        Parameters
        ----------
        question : str
            The question as a string that should be added.

        key : str
            What the attribute containing the answer should be called.

        qtype : str, optional
            The input validation to be used, by default None

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
        valid_qtypes = ['invite','channel', 'member', 'role', 'category', 'emoji']
        dictionary = {'res':None,'question':question}
        if qtype:
            dictionary['type'] = None
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
            with aiohttp.ClientSession() as session:
                r = await session.get(f'https://discord.com/api/invites/{answer}')
                return r.status == 200
        elif qtype.lower() == 'channel':
            return bool(re.match(r'<#\d{18}>', answer))
        elif qtype.lower() == 'member':
            return bool(re.match(r'<@!\d{18}>', answer))
        elif qtype.lower() == 'role':
            return bool(re.match(r'<@&\d{18}>', answer))
        elif qtype.lower() == 'emoji':
            return bool(re.match(r'<@&\d{18}>', answer)) or answer in UNICODE_EMOJI
        else:
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
        self.color = color

    async def start(self,channel=None) -> dict:
        """Starts the form in the current channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to open the form in. If none, it is gotten from the context object set during initialization.

        Returns
        -------
        FormResponse
            An object containing all of your keys as attributes.
        """
        elist = []

        if not channel:
            channel = self._ctx.channel

        qlist = []
        for n, q in enumerate(self._questions.values()):
            embed=discord.Embed(description=q['question'],color=self.color)

            embed.set_author(name=f"{self.title}: {n+1}/{len(self._questions)}",icon_url=self._bot.user.avatar_url)

            if self.color:
                embed.color=self.color

            elist.append(embed)


        prompt = None

        for embed in elist:
            ot = self._tries
            if self.editanddelete:
                if not prompt:
                    prompt = await channel.send(embed=embed)
                else:
                    await prompt.edit(embed=embed)

            else:
                prompt = await channel.send(embed=embed)

            def check(m):
                return m.channel == prompt.channel and m.author == self._ctx.author
            question = None
            for x in self._questions.keys():
                if self._questions[x]['question'].lower() == embed.description.lower():
                    question = x
                    nx = self._questions[x]

            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
            ans = msg.content
            if self.editanddelete:
                await msg.delete()
            key = question
            if 'type' in self._questions[question].keys():
                question = self._questions[question]
                if 'type' in question.keys():
                    while True:
                        result = await self.__validate_input(question['type'],ans)
                        if result:
                            nx = question
                            nx['res'] = result
                            self._questions[key] = nx
                                    #self._questions[x] = ans
                            #self._questions[question] = ans
                            break
                        else:
                            self._tries -= 1
                            await channel.send(self._retrymsg+f" You have `{self._tries}` remaining.",delete_after=3)
                            msg = await self._bot.wait_for('message',check=check,timeout=self.timeout)
                            ans = msg.content
                            if self.editanddelete:
                                await msg.delete()
                else:
                    nx['res'] = ans
                    self._questions[key] = nx
            else:
                nx['res'] = ans
                self._questions[key] = nx
        for i in self._questions.keys():
            self._questions[i] = self._questions[i]
        return FormResponse(self._questions)


class InvalidColor(Exception):
    pass

class InvalidFormType(Exception):
    """The exception raised when a form type is invalid."""
    pass

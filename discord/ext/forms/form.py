import discord
import discord.ext.commands as commands
import re
import aiohttp
from typing import List
import typing
from .helpers import funcs
import json
from emoji import UNICODE_EMOJI

def Validator(qtype: str):
    try:
        return funcs[qtype]
    except KeyError:
        raise InvalidFormType(f'Type {qtype} is invalid!')

class FormResponse:
    def __init__(self, data:list) -> None:
        for d in data:
            if isinstance(data[d], dict):
                setattr(self, d, data[d]['res'])
            else:
                setattr(self, d, data[d])

class Form:
    """The basic form object.

    Parameters:
    -----------

        ctx (discord.ext.commands.Context): The context of the form.

        title (str): The title of the form.

        cleanup (bool): Whether to cleanup and delete the form after finishing or not.
    """
    def __init__(self, ctx:commands.Context, title, cleanup=False):
        self._ctx = ctx
        self._bot = ctx.bot
        self._questions = []
        self.title = title
        self.timeout = 120
        self.editanddelete = False
        self.color = 0x2F3136
        self._incorrectmsg = None
        self._retrymsg = "You have answered incorrectly."
        self._tries = None
        self.cancelkeywords = ['cancel', 'stop', 'quit']
        self.cleanup = cleanup

    def set_timeout(self, timeout:int) -> None:
        """Sets the timeout for the form.

        Parameters
        ----------

            timeout (int): The timeout to be used.
        """
        self.timeout = timeout

    def set_tries(self, tries:int) -> None:
        """Set the amount of tries that are allowed during input validation. Defaults to 3.

        Parameters
        ----------
        tries : int
            The number of tries to set.
        """
        int(tries)
        self._tries = tries

    def enable_cancelkeywords(self, enabled: bool):
        """Enables or disables the cancellation of the form.

        Parameters
        ----------
        enabled : bool
            Whether the form is enabled or disabled.
        """
        if enabled:
            self.cancelkeywords = ['cancel', 'stop', 'quit']
        else:
            self.cancelkeywords = []

    def add_cancelkeyword(self, word: str):
        """Adds a word that will cancel the form.

        Parameters
        ----------
        word : str
            The word to listen for.
        """
        self.cancelkeywords.append(word.lower())
        return True

    def add_question(self, question, key:str=None, qtype: List[typing.Union[Validator, typing.Callable]] = []) -> List[dict]:
        """Adds a question to the form.
        The valid qtypes are:
        `invite`, `channel`, `user`, `member`, `role`, and `category`

        Parameters
        ----------
        question : str
            The question as a string that should be added.

        key : str
            What the attribute containing the answer should be called.

        qtype : List[Validator, function], optional
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
        if not isinstance(qtype, list):
            qtype = [qtype]
        if not key:
            key = question
        dictionary = {'res':None, 'question':question}
        print(dictionary)
        dictionary['type'] = qtype
        print(dictionary)
        self._tries = 3

        self._questions[key] = dictionary
        print(self._questions)
        self.set_incorrect_message('You answered incorrectly too many times. Please try again.')
        self.set_retry_message(f'Please try again.')
        print('-------------------------------------------')
        return self._questions

    def edit_and_delete(self, choice:bool=None) -> bool:
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

    def set_retry_message(self, message:str):
        """Sets the message to send if input validation fails.

        Parameters
        ----------
        message : str
            The message to be set.
        """
        self._retrymsg = message

    def set_incorrect_message(self, message:str):
        """Sets the message to send if input validation fails and there are no more tries left..

        Parameters
        ----------
        message : str
            The message to be set.
        """
        self._incorrectmsg = message

    async def set_color(self, color:str) -> None:
        """Sets the color of the form embeds."""
        match = re.match(r'(0x|#)(\d|(f|F|d|D|a|A|c|C|E|e|b|B)){6}', str(color))
        if not match:
            raise InvalidColor(f"{color} is invalid. Be sure to use colors such as '0xffffff'")
        if color.startswith("#"):
            newclr = color.replace("#", "")
            color = f"0x{newclr}"
        color = await commands.ColourConverter().convert(self._ctx, color)
        self.color = color

    async def start(self, channel=None) -> dict:
        """Starts the form in the current channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to open the form in. If none, it is gotten from the context object set during initialization.

        cleanup : bool
            Whether to cleanup and delete the form after finishing or not.

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
            embed=discord.Embed(description=q['question'], color=self.color)

            embed.set_author(name=f"{self.title}: {n+1}/{len(self._questions)}", icon_url=self._bot.user.avatar_url)

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
            while True:
                msg = await self._bot.wait_for('message', check=check, timeout=self.timeout)
                ans = msg.content
                if ans.lower() in self.cancelkeywords:
                    if self.cleanup:
                        try:
                            await msg.delete()
                        except Exception:
                            pass
                        await prompt.delete()
                    return None
                if self.editanddelete:
                    await msg.delete()
                key = question
                if 'type' in self._questions[question].keys():
                    qinfo = self._questions[question]
                    print(self._questions)
                    for func in qinfo['type']:
                        correct = False
                        print(qinfo)
                        print(type(func), func)
                        result = await func(self._ctx, msg)
                        print(bool(result is not None), result)
                        if bool(result) is False:
                            print('here')
                            ot -= 1
                            if ot <= 0:
                                await channel.send(self._incorrectmsg)
                                return None
                            await channel.send(self._retrymsg + f" You have `{ot}` remaining.", delete_after=3)
                        else:
                            print('else')
                            nx = qinfo
                            nx['res'] = result
                            self._questions[key] = nx
                            correct=True
                else:
                    nx['res'] = ans
                    self._questions[key] = nx
                    break
                if correct:
                    break
        for i in self._questions.keys():
            self._questions[i] = self._questions[i]
        if self.cleanup:
            try:
                await msg.delete()
            except Exception:
                pass
            await prompt.delete()
        return FormResponse(self._questions)


class MissingRequiredArgument(Exception):
    pass

class NaiveForm:
    """The basic form object with naive validation. Should be used in scenarios where there is no context, such as reactions.

    Parameters:
    -----------

        title (str): The title of the form.

        channel (discord.TextChannel): The channel that the form should be sent to.

        bot (discord.ext.commands.Bot): The bot that will be running the form.
    """
    def __init__(self,  title, channel: typing.Union[discord.abc.PrivateChannel, discord.abc.GuildChannel], bot: commands.Bot, author: typing.Union[discord.Member, discord.User], cleanup=False):
        self._channel = channel
        self._bot = bot
        self._questions = {}
        self.title = title
        self._author = author
        self.timeout = 120
        self.editanddelete = False
        self.color = 0x2F3136
        self._incorrectmsg = None
        self._retrymsg = None
        self._tries = None
        self.cancelkeywords = ['cancel', 'stop', 'quit']
        self.cleanup=cleanup

    def enable_cancelkeywords(self, enabled: bool):
        """Enables or disables the cancellation of the form.

        Parameters
        ----------
        enabled : bool
            Whether the form is enabled or disabled.
        """
        if enabled:
            self.cancelkeywords = ['cancel', 'stop', 'quit']
        else:
            self.cancelkeywords = []

    def add_cancelkeyword(self, word: str):
        """Adds a word that will cancel the form.

        Parameters
        ----------
        word : str
            The word to listen for.
        """
        self.cancelkeywords.append(word.lower())

    def set_timeout(self, timeout:int) -> None:
        """Sets the timeout for the form.

        Parameters
        ----------

            timeout (int): The timeout to be used.
        """
        self.timeout = timeout

    def set_tries(self, tries:int) -> None:
        """Set the amount of tries that are allowed during input validation. Defaults to 3.

        Parameters
        ----------
        tries : int
            The number of tries to set.
        """
        int(tries)
        self._tries = tries

    def add_question(self, question, key:str=None, qtype=None) -> List[dict]:
        """Adds a question to the form.
        The valid qtypes are:
        `invite`, `channel`, `member`, `role`, and `emoji`

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
        valid_qtypes = ['invite', 'channel', 'member', 'role', 'category', 'emoji', 'file']
        dictionary = {'res':None, 'question':question}
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

    async def __validate_input(self, qtype, message):
        answer = message.content
        if qtype.lower() == 'invite':
            async with aiohttp.ClientSession() as session:
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
        elif qtype.lower() == "file":
            try:
                return message.attachments[0]
            except IndexError:
                return False
        else:
            raise InvalidFormType(f"Type '{qtype}' is invalid!")


    def edit_and_delete(self, choice:bool=None) -> bool:
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

    def set_retry_message(self, message:str):
        """Sets the message to send if input validation fails.

        Parameters
        ----------
        message : str
            The message to be set.
        """
        self._retrymsg = message

    def set_incorrect_message(self, message:str):
        """Sets the message to send if input validation fails and there are no more tries left..

        Parameters
        ----------
        message : str
            The message to be set.
        """
        self._incorrectmsg = message


    async def set_color(self, color:str) -> None:
        """Sets the color of the form embeds."""
        if isinstance(color, discord.Color): self.color = color
        else: raise InvalidColor("This color is invalid! It should be a `discord.Color` instance.")

    async def start(self, channel=None) -> dict:
        """Starts the form in the current channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to open the form in. If none, it is gotten from the context object set during initialization.

        cleanup : bool
            Whether to cleanup and delete the form after finishing or not.

        Returns
        -------
        FormResponse
            An object containing all of your keys as attributes.
        """
        elist = []

        if not channel:
            channel = self._channel

        qlist = []
        for n, q in enumerate(self._questions.values()):
            embed=discord.Embed(description=q['question'], color=self.color)

            embed.set_author(name=f"{self.title}: {n+1}/{len(self._questions)}", icon_url=self._bot.user.avatar_url)

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

            def check(m: discord.Message):
                return m.channel == prompt.channel and m.author == self._author
            question = None
            for x in self._questions.keys():
                if self._questions[x]['question'].lower() == embed.description.lower():
                    question = x
                    nx = self._questions[x]
            while True:
                msg = await self._bot.wait_for('message', check=check, timeout=self.timeout)
                ans = msg.content
                if ans.lower() in self.cancelkeywords:
                    if self.cleanup:
                        try:
                            await msg.delete()
                        except Exception:
                            pass
                        await prompt.delete()
                    return None
                if self.editanddelete:
                    await msg.delete()
                key = question
                if 'type' in self._questions[question].keys():
                    qinfo = self._questions[question]
                    print(self._questions)
                    for func in qinfo['type']:
                        correct = False
                        print(qinfo)
                        print(type(func), func)
                        result = await func(self._channel, msg)
                        print(bool(result is not None), result)
                        if bool(result) is False:
                            print('here')
                            ot -= 1
                            if ot <= 0:
                                await channel.send(self._incorrectmsg)
                                return None
                            await channel.send(self._retrymsg + f" You have `{ot}` remaining.", delete_after=3)
                        else:
                            print('else')
                            nx = qinfo
                            nx['res'] = result
                            self._questions[key] = nx
                            correct=True
                else:
                    nx['res'] = ans
                    self._questions[key] = nx
                    break
                if correct:
                    break
        for i in self._questions.keys():
            self._questions[i] = self._questions[i]
        if self.cleanup:
            try:
                await msg.delete()
            except Exception:
                pass
            await prompt.delete()
        return FormResponse(self._questions)


class InvalidColor(Exception):
    pass

class InvalidFormType(Exception):
    """The exception raised when a form type is invalid."""
    pass

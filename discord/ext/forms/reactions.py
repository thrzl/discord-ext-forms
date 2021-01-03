import typing
from discord.ext import commands
import discord
from typing import List
import asyncio
import re
class ReactionForm(object): # I don't like subclassing shut up
    """
    The Reaction input object.

    ...

    Parameters
    ----------
    message : discord.Message
        The message of the reaction form object.

    bot : typing.Union[discord.CLient, discord.ext.commands.Bot]
        The bot being used for the form.

    user : typing.Union[discord.Member, discord.User]
        The member or user who should be able to use the form. If none, the form will be open to anyone.
    """
    def __init__(self, message:discord.Message, bot: typing.Union[discord.Client, commands.Bot],user:typing.Union[discord.Member, discord.User]=None):
        self._msg = message
        self._bot = bot
        self._reactions = {}
        self.timeout = 120
        self.persist = False
        self._user = user

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

    async def set_color(self,color:str) -> None:
        """Sets the color of the form embeds."""
        match = re.search(r'0x(\d|f){6}', str)
        if not match:
            raise InvalidColor(f"{color} is invalid. Be sure to use colors such as '0xffffff'")
        self._color = color

    async def start(self) -> dict:
        """Starts the form in the specified channel. If none is specified, the channel will be fetched from the `context` parameter of the form's initialization."""
        message = self._msg
        rl = []
        for i in self._reactions.keys():
            await message.add_reaction(str(i))
            rl.append(str(i))

        await asyncio.sleep(0.5)
        for i in message.reactions:
            rl.append(str(i.emoji))

        def check(r):
            if self._user is not None:
                print("There was a user")
                print(r.message_id == message.id)
                print(str(r.emoji) in rl)
                print(r.user_id == self._user.id)
                return r.message_id == message.id and str(r.emoji) in rl and r.user_id == self._user.id
            else:
                print("There was no user")
                return r.message_id == message.id and str(r.emoji) in rl

        try:
            r = await self._bot.wait_for('raw_reaction_add',check=check,timeout=self.timeout)
        except:
            return await message.edit("Timeout!")
        return self._reactions[str(r.emoji)]

class InvalidColor(Exception):
    pass
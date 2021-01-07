from discord.ext import commands
import discord
from typing import Any, List, Union
from emoji import UNICODE_EMOJI
import typing
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

    bot : typing.Union[discord.Client, discord.ext.commands.Bot]
        The bot being used for the form.

    user : typing.Union[discord.Member, discord.User]
        The member or user who should be able to use the form. If none, the form will be open to anyone.
    """
    def __init__(self, message:discord.Message, bot: Union[discord.Client, commands.Bot],user:Union[discord.Member, discord.User]=None):
        self._msg = message
        self._bot = bot
        self._reactions = {}
        self.timeout = 120
        self.persist = False
        self._user = user

    def set_timeout(self,timeout:int) -> None:
        """Set the timeout for the form. Defaults to 120 seconds.

        Parameters
        ----------
        timeout : int
            The timeout in seconds.
        """
        self.timeout = timeout

    def add_reaction(self,reaction:str,result) -> dict:
        """Adds a question to the form.

        Returns the full list of questions the form has, including the newly added one. The questions are held
        in dictionaries containing the `question` and optionally `type` keys. The `question` key contains the
        question as a string, and the `type` key contains the input validation (if any is specified)

        Parameters
        ----------
        reaction : str
            The emoji to add.
        """

        assert reaction in UNICODE_EMOJI
        self._reactions[reaction] = result
        return self._reactions

    async def start(self) -> Any:
        """Starts the reaction form on the given message.

        Returns
        -------
        Any
            Whatever the given reaction was set to return.
        """
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
                return r.message_id == message.id and str(r.emoji) in rl and r.user_id == self._user.id
            else:
                return r.message_id == message.id and str(r.emoji) in rl

        try:
            r = await self._bot.wait_for('raw_reaction_add',check=check,timeout=self.timeout)
        except:
            return await message.edit("Timeout!")
        return self._reactions[str(r.emoji)]

class ReactionMenu(object):
    def __init__(self, ctx:discord.ext.commands.Context, embeds:List[discord.Embed]):
        self._ctx = ctx
        self._embeds = embeds
        self.timeout = 120
        self._mappings = {}
        self.removereaction = True

    def set_timeout(self, timeout:int):
        """Sets the timeout for the menu.

        Parameters
        ----------
        timeout : int
            The timeout to be set in seconds.
        """        
        int(timeout)
        self._timeout = timeout

    def remove_reactions(self,bool:bool=True):
        """Sets whether the bot should remove reactions or not. Useful if the bot doesn't have `Manage Messages`

        Parameters
        ----------
        choice : bool, optional
            Whether to remove reactions or not., by default True
        """

    def addemoji(self, emoji:str, page:int) -> bool:
        """Adds an emoji/page mapping to your menu.

        Parameters
        ----------
        emoji : str
            The emoji to be used as a string. Custom emoji are supported.
        page : int
            The page to be mapped. Uses normal indexing (e.g. 1 is the first page)

        Returns
        -------
        bool :
            The result of the emoji being added. False means
            an error occurred (most likely you tried to add
            an emoji that was already set) and True means
            that everything was successful.
        """
        int(page)
        if emoji in ["◀","⏹","▶"]:
            return False
        self._mappings[emoji] = page
        return True



    async def start(self, channel=None):
        """Starts the menu in the given channel.

        Parameters
        ----------
        channel : discord.TextChannel, optional
            The channel to send the menu to. If none is specified, it uses the context's channel object.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If channel isn't specified and ctx wasn't set on initialization, the form cannot continue.
        """        
        current = 0
        ctx = self._ctx
        embeds = self._embeds
        cemojis = self._mappings
        if not channel:
            if not ctx:
                raise TypeError("start() missing 1 required positional argument: 'channel' or class 'ctx'")
            channel = ctx.channel
        msg = await ctx.send(embed=embeds[0])
        await msg.add_reaction("◀")
        await msg.add_reaction("⏹")
        await msg.add_reaction("▶")
        emojis = ["◀","⏹","▶"]
        for e in cemojis.keys():
            await msg.add_reaction()
        while True:
            def check(r):
                return str(r.emoji) in emojis and r.user_id == ctx.author.id
            try:
                r = await ctx.bot.wait_for('raw_reaction_add',check=check,timeout=self.timeout)
            except asyncio.TimeoutError:
                return await msg.edit("Timeout!")
            if str(r.emoji) in emojis:
                if str(r.emoji) == emojis[0]:
                    if current != 0:
                        await msg.edit(embed=embeds[current-1])
                        current = current-1
                if str(r.emoji) == emojis[1]:
                    await msg.clear_reactions()
                    break
                if str(r.emoji) == emojis[2]:
                    if current != len(embeds)-1:
                        await msg.edit(embed=embeds[current+1])
                        current += 1
            if str(r.emoji) in cemojis.keys():
                await msg.edit(embed=embeds[cemojis[str(r.emoji)]]-1)
                current = cemojis[str(r.emoji)]
            if self.removereaction:
                await msg.remove_reaction(r.emoji,ctx.author)

""" # Soon...
class NeoPaginator(object):
    def __init__(self, limit_per_page:int, entries:List):
        self._limit = limit_per_page
        self._entries = entries
        self.pages = []
        page = []
        for i in entries:
            if (entries.index(i)+1) % limit_per_page == 0:
                self.pages.append(page)
                page = []
            else:
                page.append(i)
"""

class InvalidColor(Exception):
    pass
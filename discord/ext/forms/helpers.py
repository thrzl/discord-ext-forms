from discord.ext import commands
from discord.ext.commands.errors import CommandError
from emoji import UNICODE_EMOJI as __UNICODE_EMOJI__
import discord

async def invite(ctx: commands.Context,message: discord.Message):
    try:
        invite = await commands.InviteConverter().convert(ctx,message.content)
        return invite
    except CommandError:
        return False

async def category(ctx: commands.Context,message: discord.Message):
    try:
        category = await commands.CategoryChannelConverter().convert(ctx,message.content)
        return category
    except CommandError:
        return False

async def channel(ctx: commands.Context,message: discord.Message):
    try:
        channel = await commands.TextChannelConverter().convert(ctx,message.content)
        return channel
    except CommandError:
        return False

async def user(ctx: commands.Context,message: discord.Message):
    try:
        user = await commands.UserConverter().convert(ctx,message.content)
        return user
    except CommandError:
        return False

async def member(ctx: commands.Context,message: discord.Message):
    try:
        member = await commands.MemberConverter().convert(ctx,message.content)
        return member
    except CommandError:
        return False

async def role(ctx: commands.Context,message: discord.Message):
    try:
        role = await commands.RoleConverter().convert(ctx,message.content)
        return role
    except CommandError:
        return False

async def emoji(ctx: commands.Context,message: discord.Message):
    try:
        emoji = await commands.EmojiConverter().convert(ctx,message.content)
        return emoji
    except:
        try:
            assert message.content in __UNICODE_EMOJI__['en']
        except CommandError:
            return False
        return message.content

async def file(ctx: commands.Context,message: discord.Message):
    try:
        return message.attachments[0]
    except IndexError:
        return False

funcs = {
    'invite': invite,
    'category': category,
    'channel': channel,
    'user': user,
    'member': member,
    'role': role,
    'emoji': emoji,
    'file': file
}
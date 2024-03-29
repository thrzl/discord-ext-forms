Quickstart Guide
================
These examples are to help you with your development in discord.ext.forms! They are well commented and will help you out a lot! If you ever need more help, join the `Discord Server! <https://discord.gg/bNtj2nFnYA>`_

Making a Basic Text Form
========================

::

    from discord.ext.forms import Form
    from discord.ext import commands
    bot = commands.Bot(command_prefix="!")

    @bot.command()
    async def testform(ctx):
        """Creates a basic form using discord.ext.forms!"""
        form = forms.Form(ctx,'Title') # Initialize our form with the title "Title"

        form.add_question('Give me an invite link!','invite','invite') # Add question "Give me an invite link" that should be called 'invite' and the type is an invite.
        form.add_question('Mention a Channel','channel','channel') # Question: Mention a channel; Name: 'channel'; Type: Channel        form.add_question('Ping a User!','member','member')
        form.add_question('Ping a User!','member','member') # Question: Ping a user; Name: 'member'; Type: member

        form.edit_and_delete(True) # The form will now edit the existing embed and delete the response.

        form.set_timeout(60) # Set the timeout to 60s
        await form.set_color("#7289DA") # Set the color of the form's embeds

        result = await form.start() # Run the form!
        """
        The form returned a FormResponse object with the attributes 'invite', 'channel', and 'member'. They return a discord.Invite, discord.TextChannel, and discord.Member respectively.
        """
        embed=discord.Embed(title="Data",description=f"Invite: {result.invite.guild}\nChannel: {result.channel.mention}\nMember: {result.member.mention}")
        await ctx.send(embed=embed)

This results in a form with 3 questions, as shown below (The output is not sent to the channel in the code above):

Making a Basic Reaction Form
============================

::

    @bot.command()
    async def reactionform(ctx):
        embed=discord.Embed(title="Reaction Menu Test",description="Delete 20 messages?") # Let's make our embed here...
        message = await ctx.send(embed=embed) # And send it! But we want to capture it as a variable!
        form = ReactionForm(message,bot,ctx.author) # Initialize the reaction form...
        form.add_reaction("✅",True) # Add the ✅ reaction which will return True.
        form.add_reaction("❌",False) # Add the ❌ reaction which will return False.
        choice = await form.start() # Start the form! Choice will be True or False based on the input.
        if choice: # If choice is true:
            await ctx.channel.purge(limit=20) # delete 20 messages!

Making a Basic Reaction Menu
============================

::

    @bot.command()
    async def menu(ctx):
        embed1=discord.Embed(description="This is embed1")
        embed2=discord.Embed(description="This is embed2")
        embed3=discord.Embed(description="This is embed3")
        rmenu = forms.ReactionMenu(ctx,[embed1,embed2,embed3])
        await rmenu.start()

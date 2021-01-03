Quickstart Guide and Examples:
==============================
Making a Basic Text Form
^^^^^^^^^^^^^^^^^^^^^^^^

::

    from discord.ext.forms import Form
    from discord.ext import commands
    bot = commands.Bot(command_prefix="!")

    @bot.command()
    async def testform(ctx):
        """Creates a basic form using discord.ext.forms!"""
        form = Form(ctx,'Title') # Let's initialize our Form object!

        form.add_question('Question 1') # Adding question 'Question 1'
        form.add_question('Question 2') # So on...
        form.add_question('Question 3')
        result = await form.start() # Let's start the form in the context's channel!
        """
        Result is a list of dictionaries containing each question and its answer.
        """
        return result

    >> [{'Question 1','user input'},{'Question 2','user input'},{'Question 3','user input'}].

This results in a form with 3 questions, as shown below (The output is not sent to the channel in the code above):

.. image:: https://mikey.has-no-bra.in/eWrLkN.gif

Making a Basic Reaction Form
============================

::

    @bot.command()
    async def reactionform(ctx):
        embed=discord.Embed(title="Reaction Menu Test",description="Delete 20 messages?")
        message = await ctx.send(embed=embed)
        form = ReactionForm(message,bot,ctx.author)
        form.add_reaction("✅",True)
        form.add_reaction("❌",False)
        choice = await form.start()
        if choice:
            await ctx.channel.purge(limit=20)



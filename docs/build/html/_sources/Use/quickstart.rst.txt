Quickstart
==========

Making a Basic Text Form
^^^^^^^^^^^^^^^^^^^^^^^^
::

    from discord.ext.forms import Form
    from discord.ext import commands
    bot = commands.Bot(command_prefix="!")

    @bot.command()
    async def testform(ctx):
        """Creates a basic form using discord.ext.forms!"""
        form = Form(ctx,'Title')
        form.add_question('Question 1')
        form.add_question('Question 2')
        form.add_question('Question 3')
        result = await form.start()
        return result

    >> [{'Question 1','user input'},{'Question 2','user input'},{'Question 3','user input'}].

This results in a form with 3 questions, as shown below (The output is not sent to the channel in the code above):

.. image:: https://mikey.has-no-bra.in/eWrLkN.gif


=================
Validation Guide
=================

To use custom validation, you need to use either the `Validator` method, or pass in your own.
An example custom validator would be:

::

    async def greaterthanone(ctx, message):
        try:
            number = int(message.content)
            return number > 1
        except:
            return False

We can then pass it into our form!
::

    ...
    @bot.command()
    async def testform(ctx):
        form = forms.Form(ctx,'Title')
        form.add_question('Give us a number greater than 1', 'number, greaterthanone') # Will only validate if the number is greater than one
        ...

Using Built-Ins for Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use the :code:`Validator` method to access the built-in validators!

::

    ...
    @bot.command()
    async def testform(ctx):
        form = forms.Form(ctx,'Title')
        form.add_question('Send an invite link!', 'invite', Validator('invite'))
        ...

.. image:: https://mikey.has-no-bra.in/0ODqXf.gif

Using multiple validators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using multiple validators for one question is now possible! You can just pass in a list made up of validators!

::

    ...

    @bot.command()
    async def testform(ctx):
        form = forms.Form(ctx,'Title')
        form.add_question('Give us a number greater than 1 and less than 100', 'number', [greaterthanone, lessthanonehundred])
        ...
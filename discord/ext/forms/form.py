from discord import (
    Interaction,
    Invite,
    TextChannel,
    Member,
    CategoryChannel,
    Role,
    Emoji,
    File,
    TextStyle,
)
from discord.ui import Modal, TextInput
from typing import List, Union
import typing
from .helpers import funcs


def Validator(name: str):
    try:
        return funcs[name]
    except KeyError:
        raise InvalidFormType(f"Type {name} is invalid!")


class Question:
    """a question to be asked in a form

    parameters
    ----------
    name : str
        the name of the question
    validator : typing.Union[typing.Callable, str], optional
        the validator of the question, by default None
    answer : Union[Invite, TextChannel, Member, CategoryChannel, Role, Emoji, File], optional
        the answer, shouldn't be set manually, by default None
    placeholder : str, optional
        the placeholder of the question, by default None
    required : bool, optional
        whether or not the question should be required, by default True
    min_length : int, optional
        the minimum length of the question, by default None
    max_length : int, optional
        the maximum length of the question, by default None
    style : TextStyle, optional
        whether the question should have one line (short), or multiple (paragraph), by default TextStyle.short
    """

    def __init__(
        self,
        name: str,
        validator: typing.Union[typing.Callable, str] = None,
        answer: Union[
            Invite, TextChannel, Member, CategoryChannel, Role, Emoji, File
        ] = None,
        placeholder: str = None,
        required: bool = True,
        min_length: int = None,
        max_length: int = None,
        style: TextStyle = TextStyle.short,
    ):
        self.name = name
        self.validator = validator
        self.answer = answer
        self.placeholder = placeholder
        self.required = required
        self.style = style
        self.min_length = min_length
        self.max_length = max_length

    def validate(self) -> bool:
        return self.validator(self.answer)


class Form:
    """the basic form object.

    Parameters:
    -----------

        interaction (discord.Interaction): the interaction object of the form.

        title (str): the title of the form.

        cleanup (bool): whether to cleanup and delete the form after finishing or not.
    """

    def __init__(self, interaction: Interaction, title: str):
        self._interaction: Interaction = interaction
        self._questions: List[Question] = []
        self.title: str = title

    def add_question(
        self,
        question: str,
        placeholder: str = None,
        required: bool = True,
        min_length: int = None,
        max_length: int = None,
        style: TextStyle = TextStyle.short,
        validator: typing.Union[Validator, typing.Callable] = None,
    ) -> List[dict]:
        """adds a question to the form.
        the valid qtypes are:
        `invite`, `channel`, `user`, `member`, `role`, and `category`

        Parameters
        ----------
        question : str
            the question as a string that should be added.

        key : str
            what the attribute containing the answer should be called.

        validator : List[Validator, function], optional
            the input validation to be used, by default None

        Returns
        -------
        List[dict]
            a list of all of the questions, stored as dictionaries.

        Raises
        ------
        InvalidFormType

            is raised when the input validation type is invalid.

        """
        self._questions.append(
            Question(
                name=question,
                validator=validator,
                answer=None,
                placeholder=placeholder,
                required=required,
                min_length=min_length,
                max_length=max_length,
                style=style,
            )
        )

        return self._questions

    async def start(self) -> List[Question]:
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

        modal = Modal(title=self.title)
        for i in self._questions:
            modal.add_item(
                TextInput(
                    label=i.name,
                    placeholder=i.placeholder,
                    required=i.required,
                    min_length=i.min_length,
                    max_length=i.max_length,
                )
            )
        answers: List[TextInput] = None
        incorrect = True
        while incorrect:
            await self._interaction.response.send_modal(modal)
            answers = modal.children
            for i, q in enumerate(self._questions):
                q.answer = answers[i].value
            if all(q.validate() for q in self._questions):
                incorrect = False
            else:
                await self._interaction.response.send_message(
                    "One or more of your answers were invalid!"
                )
        return self._questions


class MissingRequiredArgument(Exception):
    pass


class InvalidColor(Exception):
    pass


class InvalidFormType(Exception):
    """The exception raised when a form type is invalid."""

    pass

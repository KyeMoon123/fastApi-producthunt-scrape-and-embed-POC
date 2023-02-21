from functools import partial
from types import SimpleNamespace
from typing import Type

from pydantic import BaseModel, Extra, ValidationError


class ModelBuilder(object):
    """
    The Pydantic Model Builder class. Initialize the Builder with
    a custom Pydantic Model to get a Builder object for the particular model.
    You can set a field in the model in any of 2 ways below.
    1. builder.customField = customValue
    2. builder = builder.customField(customValue)
    The 2nd way above allows to chain the method calls.
    Examples:
        ```python
        model = builder.customField1(customValue1).customField2(customValue2).build()
        ```
    You can also turn off the field value validation by passing `validation=False`
    to the constructor.
    """

    __slots__ = ("__model__", "__values__", "__builder_config__")

    def __init__(self, model: Type[BaseModel], **kwargs) -> None:
        """
        Construct a Builder object for a Pydantic Model class
        Args:
            model: The Pydantic Model Class
            **kwargs: Keyword Arguments
        Keyword Args:
            validation (bool):
                Turn off field validation during setting. This ensures the model gets `construct`ed
                when `build()` method is called.
        """
        object.__setattr__(self, "__model__", model)
        object.__setattr__(self, "__values__", dict())

        # Builder configuration
        object.__setattr__(
            self,
            "__builder_config__",
            SimpleNamespace(validation=kwargs.pop("validation", True)),
        )

    def __getattr__(self, name: str):
        return partial(self.set_field, name=name)

    def __setattr__(self, key, value):
        self.set_field(value, key)

    def set_field(self, value: object, name: str, by_alias=False) -> "ModelBuilder":
        """
        Set the Pydantic field attribute. The value of the attribute can be another instance
        of `ModelBuilder`. The `build` method is called to update the fields
        Args:
            value:
                The value of the field. Value can be another builder.
                The `build` method will be called if the value is a subclass of ModelBuilder
            name: The name of the field
            by_alias: Setting field by alias
        Returns:
            The Builder object
        """
        # Check if the value is an instance of `ModelBuilder` call `build()` method to update value
        if issubclass(value.__class__, self.__class__) and hasattr(value, "build"):
            return self.set_field(value.build(), name)  # type: ignore

        if name not in self.__model__.__fields__:

            # If name is one of the aliases
            for field in self.__model__.__fields__.values():
                if field.alias == name:
                    return self.set_field(value, field.name, by_alias=True)

            if self.__model__.__config__.extra == Extra.forbid:
                raise KeyError(
                    f"'{name}' is not a valid field in '{self.__model__.__name__}'."
                )
            elif self.__model__.__config__.extra == Extra.ignore:
                return self
            elif self.__model__.__config__.extra == Extra.allow:
                self.__values__[name] = value
                return self

        known_field = self.__model__.__fields__[name]

        if not by_alias:
            if (
                known_field.alt_alias
                and not self.__model__.__config__.allow_population_by_field_name
                and name == known_field.name
            ):
                return self

        if self.__builder_config__.validation:
            _values_dict_excluding_alias = {
                k: v for k, v in self.__values__.items() if k != known_field.alias
            }
            value, error_ = known_field.validate(
                value,
                _values_dict_excluding_alias,
                loc=known_field.alias,
                cls=self.__model__.__class__,
            )
            if error_:
                raise ValidationError(
                    [
                        error_,
                    ],
                    self.__model__,
                )

        self.__values__[known_field.alias] = value
        return self

    def build(self) -> Type[BaseModel]:
        """
        Builds the Model. Calling this method returns a Model object with all the values
        passed to it.
        Returns:
            The Model object
        """
        if self.__builder_config__.validation:
            return self.__model__(**self.__values__)
        return self.__model__.construct(**self.__values__)


class BuildableBaseModel(BaseModel):
    """
    Adds capability to build a Pydantic model step by step instead of generating
    the entire object by passing the values to the constructor. Get the Model builder by calling the
    `Builder` method which in turn constructs an object of ModelBuilder type.
    """

    @classmethod
    def Builder(cls, **kwargs):
        return ModelBuilder(cls, **kwargs)
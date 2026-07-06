import json

from py_api_wbgeo import nodesapi

import typing

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing_extensions import TypeVar

"""
This class describes control form elements
"""


class CtrlLabel(BaseModel):
    """
    A label, showing the user some text
    """
    label: str
    smart_type: str = "label"


class ACtrlInput(BaseModel):
    """
    Abstract superclass for any input with a label, id and optional description
    """
    label: str
    description: typing.Optional[str] = None
    id: str


class CtrlSelect(ACtrlInput):
    """
    A choice
    """
    options: typing.List[str]
    defaultValue: typing.Optional[str] = None
    smart_type: str = "select"


class CtrlInt(ACtrlInput):
    """
    A numeric intput
    """
    defaultValue: typing.Optional[int]
    smart_type: str = "int"

class CtrlFloat(ACtrlInput):
    """
    A numeric input, supporting comma numbers
    """
    defaultValue: typing.Optional[float]
    smart_type: str = "float"

class CtrlText(ACtrlInput):
    """
    A text input
    """
    defaultValue: typing.Optional[str]
    smart_type: str = "text"


class CtrlIf(BaseModel):
    """
    Displays an area depending on the selection of another (smart) input
    Example condition: If an abstract Input with the id "type" equals "Add"
    \'$.type\' == "Add"
    """
    condition: str
    when_true: typing.List["ASmartControl"]
    when_false: typing.List["ASmartControl"]
    smart_type: str = "if"


class CtrlOrderedGrouping(ACtrlInput):
    """
    Drag and drop of items into group-columns.
    Returns an object
    """
    groups: typing.List[str]
    items: typing.List[str]
    defaultValue: typing.Optional[typing.Dict[str, typing.List[str]]] = None
    smart_type: str = "order"

@nodesapi.wbgeo_type(name='Internal CtrlGroup', color='black',
                     identifier='__internal::smart_ctr-group')
@dataclass()
class CtrlGroup:
    """
    A hierarchical group of other smart inputs
    """
    id: str
    inner: typing.List["ASmartControl"]
    smart_type: str = "group"


class CtrlFromType(BaseModel):
    """
    unsupported
    """
    id: str
    type: str
    smart_type: str = "fromtype"


ASmartControl = typing.Union[CtrlLabel, CtrlSelect, CtrlInt, CtrlFloat, CtrlIf, CtrlGroup, CtrlFromType, CtrlOrderedGrouping, CtrlText]

CtrlIf.model_rebuild()


class SmartInput(BaseModel):
    """
    Decorator information on smart inputs.
    Use this together with typing.Annotated to annotate a type as a smart input type (showing a form)
    """
    inputs: typing.List[str]
    to_form: typing.Callable[[typing.Any], typing.Any]
    to_data: typing.Callable[[typing.Any], typing.Any]


# the parameter as used in functions/components
SmartInputFormData = typing.Annotated[
    str, nodesapi.AnnotatedScriptType(name='SmartInputFormData', color='aqua',
                                      identifier='__internal:SmartInputFormData')]

# ================
#  Utility Code
# ===============


def smart_group_from_type(type: type[BaseModel], t_inst: typing.Any = None) -> list[
    ASmartControl]:
    ret = []

    for name, field in type.model_fields.items():
        field_type = field.annotation
        default_value = field.default
        current_value = getattr(t_inst, name) if t_inst is not None and hasattr(t_inst,
                                                                                name) else default_value
        description = field.description

        if field_type == int:
            ret.append(CtrlInt(id=name, label=name, description=description,
                               defaultValue=int(current_value) if current_value is not None else None))
        elif field_type == typing.Optional[int]:
            ret.append(CtrlInt(id=name, label=f'({name})', description=description,
                               defaultValue=int(current_value) if current_value is not None else None))
        elif field_type == float:
            ret.append(CtrlFloat(id=name, label=name, description=description, defaultValue=float(
                current_value) if current_value is not None else None))
        elif field_type == typing.Optional[float]:
            ret.append(CtrlFloat(id=name, label=f'({name})', description=description, defaultValue=float(
                current_value) if current_value is not None else None))
        elif field_type == str:
            ret.append(CtrlText(id=name, label=name, description=description, defaultValue=current_value))
        elif field_type == typing.Optional[str]:
            ret.append(
                CtrlText(id=name, label=f'({name})', description=description, defaultValue=current_value))
        else:
            ret.append(CtrlLabel(label=description + f": Unhandled `{str(name)}: {str(field_type)}`"))

    return ret

T = TypeVar('T')


def form_data_to_wbgeo_type_data(form_data: SmartInputFormData, type: typing.Type[T]) -> T:
    data = form_data_as_dict(form_data)
    # and convert it to our StructuralFrameInputOptions type
    return type(**data)


def form_data_as_dict(form_data: SmartInputFormData) -> typing.Dict[str, typing.Any]:
    data = json.loads(form_data)  # the input is a json dict
    data = form_data_unflatten_dict(
        {k: v for k, v in data.items() if v is not None})  # unflatten it and remove nulls
    return data


def form_data_unflatten_dict(d):
    """
    Turn the flattened dict into a multi-level dict
    """
    ret = dict()
    for key, vlaue in d.items():
        parts = key.split(".")
        d = ret
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = vlaue
    return ret

import typing
from enum import Enum

from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar, TypedDict, Type, Any, Union, Annotated, Callable, Tuple

# Type definitions exposed via an API

DataT = TypeVar('DataT')


class ScriptType(TypedDict, total=False):
    """
    The (super) type of connections between nodes
    """
    id: str
    """
    The id of this type
    """
    real_type: Union[Type[Any], Any]
    """
    The python type of parameters of this type
    """
    name: str
    """
    A human readable name
    """
    color: str
    """
    A color for this type, shown in the visualizer
    """
    ser: typing.Any
    deSer: typing.Any
    controlled: str
    """
    If this type should be controlled
    """

class TypeCapability(BaseModel):
    id: str


class GeoType(BaseModel):
    capabilities: List[TypeCapability]


class RegisterScriptBlockInputParamsReq(TypedDict, Generic[DataT]):
    param: str
    type: ScriptType


class RegisterScriptBlockInputParamsOpt(TypedDict, Generic[DataT], total=False):
    default: Optional[DataT]
    is_object_type: bool
    cap_requirements: List[Any]
    data_requirements: List[Any]


class RegisterScriptBlockInputParams(RegisterScriptBlockInputParamsReq, RegisterScriptBlockInputParamsOpt):
    pass


class RegisterScriptBlockOutputParamsReq(TypedDict, Generic[DataT]):
    param: str
    type: ScriptType


class RegisterScriptBlockOutputParamsOpt(TypedDict, Generic[DataT], total=False):
    caps: Optional[Any]


class RegisterScriptBlockOutputParams(RegisterScriptBlockOutputParamsReq, RegisterScriptBlockOutputParamsOpt):
    pass


class RegisterScriptBlockRequiredParams(TypedDict):
    identifier: str
    outputs: List[Any]
    inputs: List[RegisterScriptBlockInputParams]
    execute: Any


class RegisterScriptBlockOptParams(TypedDict, total=False):
    input_checks: List[Callable]
    description: str
    color: str
    border_color: str
    title: str
    group: str
    tags: List[str]
    is_visualizer: bool
    requires_package: List[str]
    requires_capabilities: List[Tuple[str, Optional[str]]]


class RegisterScriptBlockParams(RegisterScriptBlockRequiredParams, RegisterScriptBlockOptParams):
    pass


class RegisterVisualizerParams(TypedDict):
    identifier: str
    type: ScriptType
    visualize: Any
    title: Optional[str]

class APIScriptBlockDefinition(BaseModel, Generic[DataT]):
    pass

class GeoExecuteAPI(BaseModel):
    pass

class ComponentDecoratorReqParams(TypedDict):
    identifier: str
    title: str


class ComponentDecoratorOptParams(TypedDict, total=False):
    input_checks: List[Callable]
    color: str
    border_color: str
    group: str
    tags: List[str]
    return_name: str
    is_object_type: bool
    description: str    # by default: docstring
    requires_package: List[str]
    requires_capabilities: List[Tuple[str, Optional[str]]]


class ComponentDecoratorParams(ComponentDecoratorReqParams, ComponentDecoratorOptParams):
    pass


class ScriptTypeParams(TypedDict, total=False):
    identifier: str
    color: str
    name: str
    controlled: str

class InspectorParams(TypedDict, total=False):
    type: Type

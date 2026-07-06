import collections
import io
from typing import Unpack, Optional, Generic, TypeVar, Annotated, Union
import tempfile
import os
from py_api_wbgeo.apitypes import *

__instance = None


def set_instance(_i):
    global __instance
    __instance = _i


def register_script_block(**kwargs: Unpack[RegisterScriptBlockParams]) -> APIScriptBlockDefinition:
    return __instance.register_script_block(**kwargs)


def register_visualizer(**kwargs: Unpack[RegisterVisualizerParams]):
    return __instance.register_visualizer(**kwargs)


def create_geo_execute(exec: Any) -> GeoExecuteAPI:
    return __instance.create_geo_execute(exec)


# Decorator
def wbgeo_component(**kwargs: Unpack[ComponentDecoratorParams]):
    """
    This decorator declares a function as WBGeo component.

    Args:
        **kwargs: Parameters defined by `ComponentDecoratorParams`.

            identifier (str):
                Unique identifier of the component.
            title (str):
                Human readable title of the component.
            color (str, optional):
                Color of the component.
            ...
    """
    if __instance is None:
        return lambda f: f
    return __instance.wbgeo_component_decorator(**kwargs)


def wbgeo_type(**kwargs: Unpack[ScriptTypeParams]):
    if __instance is None:
        return lambda c: c
    return __instance.wbgeo_type_decorator(**kwargs)


# Added in 0.4: decorator for inspector components
def wbgeo_inspector(**kwargs: Unpack[InspectorParams]):
    """
    This decorator annotates a component as inspecting a type.
    """
    op = getattr(__instance, "wbgeo_inspector_decorator", None)
    if __instance is None or not callable(op):
        return lambda c: c
    return __instance.wbgeo_inspector_decorator(**kwargs)


class AnnotatedScriptType():
    def __init__(self, **kwargs: Unpack[ScriptTypeParams]):
        self.kwargs = kwargs


T = TypeVar('T')


class InspectorData(Generic[T]):
    async def get_value(self) -> T:
        pass


class InspectorHelper:
    async def trace(self, geotype: Type[T]) -> Optional[InspectorData[T]]:
        pass


def wbgeo_register_runner_capability(capability_name: str, capability_value: Optional[str] = None):
    """
    Register a capability as present.
    """
    if __instance is not None:
        __instance.wbgeo_register_runner_capability(capability_name, capability_value)


_INTERNAL_BYTE_BUFFER_NAME = '__internal::file_buffer'


class GeoTempFile(os.PathLike):
    """
    A to-be-downloaded temporary file, backed by a real file, which can be used like a buffer
    """
    name: str
    fd: int

    def __init__(self):
        super().__init__()
        self.fd, self.name = tempfile.mkstemp()

    def __fspath__(self):
        """

        :return:
        """
        return self.name

    def __str__(self):
        return self.name

    def close_and_remove(self):
        os.close(self.fd)
        os.remove(self.name)


# E.g., an io.BytesIO or anything accepted by open(...)
BasicallyABufferedFile = Annotated[
    Union[io.IOBase, GeoTempFile], AnnotatedScriptType(name=_INTERNAL_BYTE_BUFFER_NAME, color='aqua',
                                                       identifier=_INTERNAL_BYTE_BUFFER_NAME,
                                                       controlled='file_import_export')]

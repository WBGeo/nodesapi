import enum
import json
import os
import typing

"""
Example usage:
* Download geores from the webinterface
* Call the function:
mesh_results = load_computation(MeshResults, 'C:\\Users\\username\\Downloads\\134MeshResults.geores') 
"""

T = typing.TypeVar("T")


def load_computation(geo_type: typing.Type[T],
                     file_path: typing.Union[os.PathLike | str | bytes]) -> T:
  """
  Import the result of a computation of the workbench
  :param geo_type: the type of the computation
  :param file_path: the path to the serialized result
  :return: the concrete execution result
  """

  def get_real_type(input_type: typing.Type) \
      -> typing.Tuple[typing.Union[typing.Type, typing.ParamSpec], typing.Type]:
    # remove all typing.annotated stuff
    args = input_type,
    while typing.get_origin(args[0]) is typing.Annotated:
      args = typing.get_args(args[0])
    origin_type = typing.get_origin(args[0])
    if origin_type is not None:
      return origin_type, args[0]
    return args[0], args[0]

  with open(file_path, 'r') as f:
    i = f.read()

  if i.startswith("WBGEO_DATA"):
    # skip the header
    magic_len = len("WBGEO_DATA")
    pos = i.find("WBGEO_DATA", magic_len)
    header_len = int(i[magic_len:pos])
    header = i[pos + magic_len:pos + magic_len + header_len]
    i = i[(pos + magic_len + header_len + magic_len):]

  real_type, _ = get_real_type(geo_type)
  if real_type is str:
    return i
  elif real_type is int:
    return int(i)
  elif real_type is float:
    return float(i)
  elif real_type is bool:
    return i.lower() in ("1", "true", "yes", "True")
  elif real_type is list or real_type is tuple:
    return real_type(json.loads(i))
  elif issubclass(real_type, enum.Enum):
    return real_type[i]
  return real_type(**json.loads(i))


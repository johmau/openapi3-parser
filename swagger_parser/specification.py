from enum import Enum, unique
from typing import List, Optional, Tuple


class Specification:
    version: str
    info: 'Info'
    servers: Tuple['Server']
    tags: Tuple['Tag']
    paths: Tuple['Path']

    def __init__(self,
                 version: str,
                 info: 'Info',
                 servers: Tuple['Server'],
                 tags: Tuple['Tag'],
                 paths: Tuple['Path']) -> None:
        self.version = version
        self.info = info
        self.servers = servers
        self.tags = tags
        self.paths = paths

    def __repr__(self) -> str:
        return f"{self.info.title}: {self.info.description} <OpenAPI v{self.version}>"


class Info:
    title: str
    version: str
    description: str
    license: 'License'
    contact: 'Contact'

    def __init__(self,
                 title: str,
                 version: str,
                 description: str,
                 license_item: 'License',
                 contact_item: 'Contact') -> None:
        self.title = title
        self.version = version
        self.description = description
        self.license = license_item
        self.contact = contact_item


class License:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class Contact:
    name: str
    email: str

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class Server:
    url: str
    description: str

    def __init__(self, url: str, description: str) -> None:
        self.url = url
        self.description = description


class Tag:
    name: str
    description: str

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class Path:
    url: str
    operations: Tuple['Operation']

    def __init__(self, url: str, operations: Tuple['Operation']) -> None:
        self.url = url
        self.operations = operations


@unique
class OperationMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'


class Operation:
    method: OperationMethod
    tags: List[str]
    summary: str
    operation_id: str
    parameters: Tuple['Parameter']
    request_body: 'RequestBody'
    responses: Tuple['Response']

    def __init__(self,
                 method: str,
                 tags: List[str],
                 summary: str,
                 operation_id: str,
                 parameters: Tuple['Parameter'],
                 request_body: 'RequestBody',
                 responses: Tuple['Response']) -> None:
        self.method = OperationMethod(method)
        self.tags = tags
        self.summary = summary
        self.operation_id = operation_id
        self.parameters = parameters
        self.request_body = request_body
        self.responses = responses


@unique
class ParameterLocation(Enum):
    QUERY = 'query'
    HEADER = 'header'
    PATH = 'path'
    COOKIE = 'cookie'


class Parameter:
    name: str
    location: ParameterLocation
    description: str
    required: bool
    deprecated: bool
    allow_empty: bool
    schema: 'Schema'

    def __init__(self,
                 name: str,
                 location: ParameterLocation,
                 description: str,
                 required: bool,
                 deprecated: bool,
                 allow_empty: bool,
                 schema: 'Schema') -> None:
        self.name = name
        self.location = location
        self.description = description
        self.required = required
        self.deprecated = deprecated
        self.allow_empty = allow_empty
        self.schema = schema


class RequestBody:
    description: str
    required: bool
    contents: Tuple['Content']

    def __init__(self,
                 description: str,
                 required: bool,
                 contents: Tuple['Content']) -> None:
        self.description = description
        self.required = required
        self.contents = contents


class Response:
    code: int
    description: str
    contents: Tuple['Content']

    def __init__(self, code: int, description: str, contents: Tuple['Content']) -> None:
        self.code = code
        self.description = description
        self.contents = contents


@unique
class ContentType(Enum):
    APPLICATION_JSON = 'application/json'
    # TODO: support other types


class Content:
    type: ContentType
    schema: 'Schema'

    def __init__(self, content_type: ContentType, schema: 'Schema') -> None:
        self.type = content_type
        self.schema = schema


@unique
class DataType(Enum):
    int = 'integer'
    number = 'number'
    string = 'string'
    bool = 'boolean'
    array = 'array'
    object = 'object'


class Schema:
    type: DataType
    title: Optional[str]
    deprecated: Optional[bool]
    nullable: Optional[bool]
    description: Optional[str]
    format: Optional[str]
    required: bool

    def __init__(self, data_type: DataType, **kwargs) -> None:
        self.type = data_type
        self.title = kwargs['title']
        self.deprecated = kwargs['deprecated']
        self.nullable = kwargs['nullable']
        self.description = kwargs['description']
        self.format = kwargs['format']
        self.required = False


class IntSchema(Schema):
    example: Optional[int]
    minimum: Optional[int]
    maximum: Optional[int]
    default: Optional[int]
    enum: List[int]

    def __init__(self,
                 example: Optional[int] = None,
                 minimum: Optional[int] = None,
                 maximum: Optional[int] = None,
                 default: Optional[int] = None,
                 enum: List[int] = None,
                 **kwargs) -> None:
        if enum is None:
            enum = []

        self.example = example
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.enum = enum

        super().__init__(DataType.int, **kwargs)


class NumberSchema(Schema):
    example: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]
    default: Optional[float]
    enum: List[float]

    def __init__(self,
                 example: Optional[float] = None,
                 minimum: Optional[float] = None,
                 maximum: Optional[float] = None,
                 default: Optional[float] = None,
                 enum: List[float] = None,
                 **kwargs) -> None:
        if enum is None:
            enum = []

        self.example = example
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.enum = enum

        super().__init__(DataType.number, **kwargs)


class StringSchema(Schema):
    example: Optional[str]
    min_length: Optional[int]
    max_length: Optional[int]
    default: Optional[str]
    enum: List[str]

    def __init__(self,
                 example: Optional[str] = None,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 default: Optional[str] = None,
                 enum: List[str] = None,
                 **kwargs) -> None:
        if enum is None:
            enum = []

        self.example = example
        self.min_length = min_length
        self.max_length = max_length
        self.default = default
        self.enum = enum

        super().__init__(DataType.string, **kwargs)


class BooleanSchema(Schema):
    example: Optional[bool]
    default: Optional[bool]

    def __init__(self,
                 example: Optional[bool] = None,
                 default: Optional[bool] = None,
                 **kwargs) -> None:
        self.example = example
        self.default = default

        super().__init__(DataType.bool, **kwargs)


class ArraySchema(Schema):
    items_schema: Schema
    min_items: Optional[int]
    max_items: Optional[int]

    def __init__(self,
                 items_schema: Schema,
                 min_items: Optional[int] = None,
                 max_items: Optional[int] = None,
                 **kwargs) -> None:
        self.items_schema = items_schema
        self.min_items = min_items
        self.max_items = max_items

        super().__init__(DataType.array, **kwargs)


class ObjectSchema(Schema):
    properties: Tuple['Schema']

    def __init__(self,
                 properties: Tuple['Schema'],
                 **kwargs) -> None:
        self.properties = properties

        super().__init__(DataType.object, **kwargs)

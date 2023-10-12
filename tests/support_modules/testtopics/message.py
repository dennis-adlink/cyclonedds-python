from dataclasses import dataclass

from cyclonedds.idl import IdlStruct
from cyclonedds.idl.annotations import key, keylist, appendable, mutable
from cyclonedds.idl.types import array, uint8, int8, int16, int32, int64


@dataclass
class Message(IdlStruct):
    message: str


@dataclass
class MessageAlt(IdlStruct):
    user_id: int
    message: str


@dataclass
@keylist(["user_id"])
class MessageKeyed(IdlStruct):
    user_id: int
    message: str


@dataclass
@keylist(["arr1a", "arr2a", "arr3a"])
class KeyedArrayType(IdlStruct):
    arr1a: array[int8, 3]
    arr1b: array[int8, 3]
    arr2a: array[int64, 3]
    arr2b: array[int16, 3]
    arr3a: array[int32, 3]
    arr3b: array[int64, 3]


@dataclass
@appendable
class XMessage(IdlStruct):
    message: str

@dataclass
@mutable
class KeyedNestedImplicit(IdlStruct):
    x: uint8
    y: uint8

@dataclass
@mutable
class KeyedNestedExplicit(IdlStruct):
    x: uint8
    key("x")
    y: uint8

@dataclass
class KeyedImplicit(IdlStruct):
    a: KeyedNestedImplicit
    key("a")
    b: KeyedNestedImplicit
    c: KeyedNestedExplicit
    key("c")
    d: KeyedNestedExplicit
    e: uint8
    key("e")

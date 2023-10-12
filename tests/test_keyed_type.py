import pytest

from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from cyclonedds.pub import DataWriter

from support_modules.testtopics import KeyedArrayType, KeyedImplicit, KeyedNestedImplicit, KeyedNestedExplicit


def test_keyed_type_alignment():
    dp = DomainParticipant()
    tp = Topic(dp, "Test", KeyedArrayType)
    dw = DataWriter(dp, tp)
    dr = DataReader(dp, tp)

    samp1 = KeyedArrayType(
        [-1] * 3,
        [-1] * 3,
        [-1] * 3,
        [-1] * 3,
        [-1] * 3,
        [-1] * 3
    )

    dw.write(samp1)
    samp2 = dr.read()[0]
    assert KeyedArrayType.__idl__.serialize_key_normalized(samp1) == KeyedArrayType.__idl__.serialize_key_normalized(samp2)


def test_keyed_implicit():
    s1 = KeyedImplicit(a=KeyedNestedImplicit(0x11, 0x22), b=KeyedNestedImplicit(0x33, 0x44), c=KeyedNestedExplicit(0x55, 0x66), d=KeyedNestedExplicit(0x77, 0x88), e=0x99 )
    b = s1.serialize()
    s2 = KeyedImplicit.deserialize(b)
    assert s1 == s2
    assert KeyedImplicit.__idl__.serialize_key(s1) == KeyedImplicit.__idl__.serialize_key(s2)
    assert KeyedImplicit.__idl__.serialize_key_normalized(s1) == KeyedImplicit.__idl__.serialize_key_normalized(s2)

    #                                                                DHDR(a)____ MEMBID(a.x) x_ pad_____ MEMBID(a.y) y_ pad_____ DHDR(c)____ MEMBID(c.x) x_ e_
    assert KeyedImplicit.__idl__.serialize_key(s2) == bytes.fromhex('0d 00 00 00 00 00 00 80 11 00 00 00 01 00 00 80 22 00 00 00 05 00 00 00 00 00 00 80 55 99')

    #                                                            CDR-HDR____ DHDR(a)____ MEMBID(a.x) x_ pad_____ MEMBID(a.y) y_ pad_____ DHDR(b)____ MEMBID(a.x) x_ pad_____ MEMBID(a.y) y_ pad_____ DHDR(c)____ MEMBID(c.x) x_ pad_____ MEMBID(c.y) y_ pad_____ DHDR(c)____ MEMBID(d.x) x_ pad_____ MEMBID(d.x) y_ MEMBID(c.y) y_ e_
    assert KeyedImplicit.__idl__.serialize(s2) == bytes.fromhex('00 07 00 00 0d 00 00 00 00 00 00 80 11 00 00 00 01 00 00 80 22 00 00 00 0d 00 00 00 00 00 00 80 33 00 00 00 01 00 00 80 44 00 00 00 0d 00 00 00 00 00 00 80 55 00 00 00 01 00 00 00 66 00 00 00 0d 00 00 00 00 00 00 80 77 00 00 00 01 00 00 00 88 99')

def test_keyed_must_understand():
    s1 = KeyedNestedExplicit(0x11, 0x22)
    b = s1.serialize()
    s2 = KeyedNestedExplicit.deserialize(b)
    assert s1 == s2
    assert KeyedNestedExplicit.__idl__.serialize_key(s1) == KeyedNestedExplicit.__idl__.serialize_key(s2)
    assert KeyedNestedExplicit.__idl__.serialize_key_normalized(s1) == KeyedNestedExplicit.__idl__.serialize_key_normalized(s2)
    #                                                                DHDR_______ MEMBID(x)__ x_
    assert KeyedNestedExplicit.__idl__.serialize_key(s2) == bytes.fromhex('05 00 00 00 00 00 00 80 11')
    #                                                                  CDR-HDR____ DHDR_______ MEMBID(x)__ x_ pad_____ MEMBID(x)__ y_
    assert KeyedNestedExplicit.__idl__.serialize(s2) == bytes.fromhex('00 0b 00 00 0d 00 00 00 00 00 00 80 11 00 00 00 01 00 00 00 22')

def test_keyed_must_understand_nokey():
    s1 = KeyedNestedImplicit(0x11, 0x22)
    b = s1.serialize()
    s2 = KeyedNestedImplicit.deserialize(b)
    assert s1 == s2
    #                                                                  CDR-HDR____ DHDR_______ MEMBID(x)__ x_ pad_____ MEMBID(x)__ y_
    assert KeyedNestedImplicit.__idl__.serialize(s2) == bytes.fromhex('00 0b 00 00 0d 00 00 00 00 00 00 80 11 00 00 00 01 00 00 80 22')
    #FIXME: should not have must-understand bits set:
    #   assert KeyedNestedImplicit.__idl__.serialize(s2) == bytes.fromhex('00 0b 00 00 0d 00 00 00 00 00 00 00 11 00 00 00 01 00 00 00 22')

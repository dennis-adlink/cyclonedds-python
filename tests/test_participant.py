import pytest

from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.util import isgoodentity

from support_modules.testtopics import Message


def test_create_participant():
    dp = DomainParticipant(0)
    assert isgoodentity(dp)


def test_find_topic():
    dp = DomainParticipant(0)
    tp = Topic(dp, "Message", Message)

    assert isgoodentity(tp)
    xtp = dp.find_topic(0, "Message", tp.data_type.__idl__.get_type_info(), 0)

    assert xtp.typename == tp.typename
    assert xtp.name == tp.name

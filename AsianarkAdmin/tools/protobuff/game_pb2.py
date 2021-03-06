# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='game.proto',
  package='protofile.game',
  serialized_pb=_b('\n\ngame.proto\x12\x0eprotofile.game\"5\n\x11startGameResponse\x12\x0f\n\x07videoid\x18\x01 \x02(\x05\x12\x0f\n\x07\x62\x65ttime\x18\x02 \x02(\x05\"A\n\nbetRequest\x12\x11\n\troundcode\x18\x01 \x02(\t\x12\x10\n\x08playtype\x18\x02 \x02(\x05\x12\x0e\n\x06\x61mount\x18\x03 \x02(\x02\"\x1b\n\x0b\x62\x65tResponse\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\"A\n\x10tablePotResponse\x12\x10\n\x08playtype\x18\x01 \x02(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x02(\x05\x12\x0b\n\x03num\x18\x03 \x02(\x02\"P\n\x16tablePotDetailsRequest\x12\x11\n\ttablecode\x18\x01 \x02(\x05\x12\x10\n\x08playtype\x18\x02 \x02(\x05\x12\x11\n\troundcode\x18\x03 \x02(\t\"e\n\x17tablePotDetailsResponse\x12\x10\n\x08playtype\x18\x01 \x02(\x05\x12\x0b\n\x03num\x18\x02 \x02(\x05\x12+\n\x07\x64\x65tails\x18\x03 \x03(\x0b\x32\x1a.protofile.game.PotDetails\"b\n\nPotDetails\x12\x11\n\tloginname\x18\x01 \x02(\t\x12\x10\n\x08nickname\x18\x02 \x02(\t\x12\x11\n\ttablecode\x18\x03 \x02(\x05\x12\x0c\n\x04seat\x18\x04 \x02(\x05\x12\x0e\n\x06\x61mount\x18\x05 \x02(\x02\"\x81\x01\n\x12gameResultResponse\x12\x11\n\troundcode\x18\x01 \x02(\t\x12\x0f\n\x07videoid\x18\x02 \x02(\x05\x12\x13\n\x0b\x62\x61nkerpoint\x18\x03 \x02(\x05\x12\x13\n\x0bplayerpoint\x18\x04 \x02(\x05\x12\x0c\n\x04pair\x18\x05 \x02(\x05\x12\x0f\n\x07\x63\x61rdnum\x18\x06 \x02(\x05\"\x80\x01\n\x0ereckonResponse\x12\x11\n\troundcode\x18\x01 \x02(\t\x12\x10\n\x08totalwin\x18\x02 \x02(\x02\x12\x0c\n\x04left\x18\x03 \x02(\x02\x12\x0b\n\x03num\x18\x04 \x02(\x05\x12.\n\x07\x64\x65tails\x18\x05 \x03(\x0b\x32\x1d.protofile.game.ReckonDetails\".\n\rReckonDetails\x12\x10\n\x08playtype\x18\x01 \x02(\x05\x12\x0b\n\x03win\x18\x02 \x02(\x02\"\\\n\x17otherPlayersBetResponse\x12\x11\n\ttablecode\x18\x01 \x02(\x05\x12\x0c\n\x04seat\x18\x02 \x02(\x05\x12\x10\n\x08playtype\x18\x03 \x02(\x05\x12\x0e\n\x06\x61mount\x18\x04 \x02(\x02\"\x14\n\x12videoStatusRequest\"\x96\x01\n\x13videoStatusResponse\x12\x0f\n\x07videoid\x18\x01 \x02(\x05\x12\x10\n\x08gametype\x18\x02 \x02(\t\x12\x11\n\troundcode\x18\x03 \x02(\t\x12\x0e\n\x06status\x18\x04 \x02(\x05\x12\x13\n\x0b\x62\x61nkercards\x18\x05 \x02(\t\x12\x13\n\x0bplayercards\x18\x06 \x02(\t\x12\x0f\n\x07\x62\x65ttime\x18\x07 \x02(\x05\"5\n\x0e\x64\x65\x61lerResponse\x12\x12\n\ndealername\x18\x01 \x02(\t\x12\x0f\n\x07videoid\x18\x02 \x02(\x05\"#\n\rnoBetResponse\x12\x12\n\nroundcount\x18\x01 \x02(\x05\"Q\n\x10tableBetResponse\x12\x0b\n\x03num\x18\x01 \x02(\x05\x12\x30\n\x07\x64\x65tails\x18\x02 \x03(\x0b\x32\x1f.protofile.game.TableBetDetails\"y\n\x0fTableBetDetails\x12\x11\n\tloginname\x18\x01 \x02(\t\x12\x10\n\x08nickname\x18\x02 \x02(\t\x12\x11\n\ttablecode\x18\x03 \x02(\x05\x12\x0c\n\x04seat\x18\x04 \x02(\x05\x12\x10\n\x08playtype\x18\x05 \x02(\x05\x12\x0e\n\x06\x61mount\x18\x06 \x02(\x02\"l\n\x1aotherPlayersReckonResponse\x12\x11\n\tloginname\x18\x01 \x02(\t\x12\x0b\n\x03num\x18\x02 \x02(\x05\x12.\n\x07\x64\x65tails\x18\x03 \x03(\x0b\x32\x1d.protofile.game.ReckonDetails')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_STARTGAMERESPONSE = _descriptor.Descriptor(
  name='startGameResponse',
  full_name='protofile.game.startGameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='videoid', full_name='protofile.game.startGameResponse.videoid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bettime', full_name='protofile.game.startGameResponse.bettime', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=83,
)


_BETREQUEST = _descriptor.Descriptor(
  name='betRequest',
  full_name='protofile.game.betRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='roundcode', full_name='protofile.game.betRequest.roundcode', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.betRequest.playtype', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='protofile.game.betRequest.amount', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=85,
  serialized_end=150,
)


_BETRESPONSE = _descriptor.Descriptor(
  name='betResponse',
  full_name='protofile.game.betResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='protofile.game.betResponse.code', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=179,
)


_TABLEPOTRESPONSE = _descriptor.Descriptor(
  name='tablePotResponse',
  full_name='protofile.game.tablePotResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.tablePotResponse.playtype', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='protofile.game.tablePotResponse.amount', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='num', full_name='protofile.game.tablePotResponse.num', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=181,
  serialized_end=246,
)


_TABLEPOTDETAILSREQUEST = _descriptor.Descriptor(
  name='tablePotDetailsRequest',
  full_name='protofile.game.tablePotDetailsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tablecode', full_name='protofile.game.tablePotDetailsRequest.tablecode', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.tablePotDetailsRequest.playtype', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='roundcode', full_name='protofile.game.tablePotDetailsRequest.roundcode', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=248,
  serialized_end=328,
)


_TABLEPOTDETAILSRESPONSE = _descriptor.Descriptor(
  name='tablePotDetailsResponse',
  full_name='protofile.game.tablePotDetailsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.tablePotDetailsResponse.playtype', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='num', full_name='protofile.game.tablePotDetailsResponse.num', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='details', full_name='protofile.game.tablePotDetailsResponse.details', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=431,
)


_POTDETAILS = _descriptor.Descriptor(
  name='PotDetails',
  full_name='protofile.game.PotDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='loginname', full_name='protofile.game.PotDetails.loginname', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='protofile.game.PotDetails.nickname', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tablecode', full_name='protofile.game.PotDetails.tablecode', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat', full_name='protofile.game.PotDetails.seat', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='protofile.game.PotDetails.amount', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=433,
  serialized_end=531,
)


_GAMERESULTRESPONSE = _descriptor.Descriptor(
  name='gameResultResponse',
  full_name='protofile.game.gameResultResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='roundcode', full_name='protofile.game.gameResultResponse.roundcode', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='videoid', full_name='protofile.game.gameResultResponse.videoid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bankerpoint', full_name='protofile.game.gameResultResponse.bankerpoint', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playerpoint', full_name='protofile.game.gameResultResponse.playerpoint', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pair', full_name='protofile.game.gameResultResponse.pair', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cardnum', full_name='protofile.game.gameResultResponse.cardnum', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=534,
  serialized_end=663,
)


_RECKONRESPONSE = _descriptor.Descriptor(
  name='reckonResponse',
  full_name='protofile.game.reckonResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='roundcode', full_name='protofile.game.reckonResponse.roundcode', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='totalwin', full_name='protofile.game.reckonResponse.totalwin', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='left', full_name='protofile.game.reckonResponse.left', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='num', full_name='protofile.game.reckonResponse.num', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='details', full_name='protofile.game.reckonResponse.details', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=666,
  serialized_end=794,
)


_RECKONDETAILS = _descriptor.Descriptor(
  name='ReckonDetails',
  full_name='protofile.game.ReckonDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.ReckonDetails.playtype', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='win', full_name='protofile.game.ReckonDetails.win', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=796,
  serialized_end=842,
)


_OTHERPLAYERSBETRESPONSE = _descriptor.Descriptor(
  name='otherPlayersBetResponse',
  full_name='protofile.game.otherPlayersBetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tablecode', full_name='protofile.game.otherPlayersBetResponse.tablecode', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat', full_name='protofile.game.otherPlayersBetResponse.seat', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.otherPlayersBetResponse.playtype', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='protofile.game.otherPlayersBetResponse.amount', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=844,
  serialized_end=936,
)


_VIDEOSTATUSREQUEST = _descriptor.Descriptor(
  name='videoStatusRequest',
  full_name='protofile.game.videoStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=938,
  serialized_end=958,
)


_VIDEOSTATUSRESPONSE = _descriptor.Descriptor(
  name='videoStatusResponse',
  full_name='protofile.game.videoStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='videoid', full_name='protofile.game.videoStatusResponse.videoid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gametype', full_name='protofile.game.videoStatusResponse.gametype', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='roundcode', full_name='protofile.game.videoStatusResponse.roundcode', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='protofile.game.videoStatusResponse.status', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bankercards', full_name='protofile.game.videoStatusResponse.bankercards', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playercards', full_name='protofile.game.videoStatusResponse.playercards', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bettime', full_name='protofile.game.videoStatusResponse.bettime', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=961,
  serialized_end=1111,
)


_DEALERRESPONSE = _descriptor.Descriptor(
  name='dealerResponse',
  full_name='protofile.game.dealerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dealername', full_name='protofile.game.dealerResponse.dealername', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='videoid', full_name='protofile.game.dealerResponse.videoid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1113,
  serialized_end=1166,
)


_NOBETRESPONSE = _descriptor.Descriptor(
  name='noBetResponse',
  full_name='protofile.game.noBetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='roundcount', full_name='protofile.game.noBetResponse.roundcount', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1168,
  serialized_end=1203,
)


_TABLEBETRESPONSE = _descriptor.Descriptor(
  name='tableBetResponse',
  full_name='protofile.game.tableBetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num', full_name='protofile.game.tableBetResponse.num', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='details', full_name='protofile.game.tableBetResponse.details', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1205,
  serialized_end=1286,
)


_TABLEBETDETAILS = _descriptor.Descriptor(
  name='TableBetDetails',
  full_name='protofile.game.TableBetDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='loginname', full_name='protofile.game.TableBetDetails.loginname', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='protofile.game.TableBetDetails.nickname', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tablecode', full_name='protofile.game.TableBetDetails.tablecode', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat', full_name='protofile.game.TableBetDetails.seat', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playtype', full_name='protofile.game.TableBetDetails.playtype', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='protofile.game.TableBetDetails.amount', index=5,
      number=6, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1288,
  serialized_end=1409,
)


_OTHERPLAYERSRECKONRESPONSE = _descriptor.Descriptor(
  name='otherPlayersReckonResponse',
  full_name='protofile.game.otherPlayersReckonResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='loginname', full_name='protofile.game.otherPlayersReckonResponse.loginname', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='num', full_name='protofile.game.otherPlayersReckonResponse.num', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='details', full_name='protofile.game.otherPlayersReckonResponse.details', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1411,
  serialized_end=1519,
)

_TABLEPOTDETAILSRESPONSE.fields_by_name['details'].message_type = _POTDETAILS
_RECKONRESPONSE.fields_by_name['details'].message_type = _RECKONDETAILS
_TABLEBETRESPONSE.fields_by_name['details'].message_type = _TABLEBETDETAILS
_OTHERPLAYERSRECKONRESPONSE.fields_by_name['details'].message_type = _RECKONDETAILS
DESCRIPTOR.message_types_by_name['startGameResponse'] = _STARTGAMERESPONSE
DESCRIPTOR.message_types_by_name['betRequest'] = _BETREQUEST
DESCRIPTOR.message_types_by_name['betResponse'] = _BETRESPONSE
DESCRIPTOR.message_types_by_name['tablePotResponse'] = _TABLEPOTRESPONSE
DESCRIPTOR.message_types_by_name['tablePotDetailsRequest'] = _TABLEPOTDETAILSREQUEST
DESCRIPTOR.message_types_by_name['tablePotDetailsResponse'] = _TABLEPOTDETAILSRESPONSE
DESCRIPTOR.message_types_by_name['PotDetails'] = _POTDETAILS
DESCRIPTOR.message_types_by_name['gameResultResponse'] = _GAMERESULTRESPONSE
DESCRIPTOR.message_types_by_name['reckonResponse'] = _RECKONRESPONSE
DESCRIPTOR.message_types_by_name['ReckonDetails'] = _RECKONDETAILS
DESCRIPTOR.message_types_by_name['otherPlayersBetResponse'] = _OTHERPLAYERSBETRESPONSE
DESCRIPTOR.message_types_by_name['videoStatusRequest'] = _VIDEOSTATUSREQUEST
DESCRIPTOR.message_types_by_name['videoStatusResponse'] = _VIDEOSTATUSRESPONSE
DESCRIPTOR.message_types_by_name['dealerResponse'] = _DEALERRESPONSE
DESCRIPTOR.message_types_by_name['noBetResponse'] = _NOBETRESPONSE
DESCRIPTOR.message_types_by_name['tableBetResponse'] = _TABLEBETRESPONSE
DESCRIPTOR.message_types_by_name['TableBetDetails'] = _TABLEBETDETAILS
DESCRIPTOR.message_types_by_name['otherPlayersReckonResponse'] = _OTHERPLAYERSRECKONRESPONSE

startGameResponse = _reflection.GeneratedProtocolMessageType('startGameResponse', (_message.Message,), dict(
  DESCRIPTOR = _STARTGAMERESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.startGameResponse)
  ))
_sym_db.RegisterMessage(startGameResponse)

betRequest = _reflection.GeneratedProtocolMessageType('betRequest', (_message.Message,), dict(
  DESCRIPTOR = _BETREQUEST,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.betRequest)
  ))
_sym_db.RegisterMessage(betRequest)

betResponse = _reflection.GeneratedProtocolMessageType('betResponse', (_message.Message,), dict(
  DESCRIPTOR = _BETRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.betResponse)
  ))
_sym_db.RegisterMessage(betResponse)

tablePotResponse = _reflection.GeneratedProtocolMessageType('tablePotResponse', (_message.Message,), dict(
  DESCRIPTOR = _TABLEPOTRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.tablePotResponse)
  ))
_sym_db.RegisterMessage(tablePotResponse)

tablePotDetailsRequest = _reflection.GeneratedProtocolMessageType('tablePotDetailsRequest', (_message.Message,), dict(
  DESCRIPTOR = _TABLEPOTDETAILSREQUEST,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.tablePotDetailsRequest)
  ))
_sym_db.RegisterMessage(tablePotDetailsRequest)

tablePotDetailsResponse = _reflection.GeneratedProtocolMessageType('tablePotDetailsResponse', (_message.Message,), dict(
  DESCRIPTOR = _TABLEPOTDETAILSRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.tablePotDetailsResponse)
  ))
_sym_db.RegisterMessage(tablePotDetailsResponse)

PotDetails = _reflection.GeneratedProtocolMessageType('PotDetails', (_message.Message,), dict(
  DESCRIPTOR = _POTDETAILS,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.PotDetails)
  ))
_sym_db.RegisterMessage(PotDetails)

gameResultResponse = _reflection.GeneratedProtocolMessageType('gameResultResponse', (_message.Message,), dict(
  DESCRIPTOR = _GAMERESULTRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.gameResultResponse)
  ))
_sym_db.RegisterMessage(gameResultResponse)

reckonResponse = _reflection.GeneratedProtocolMessageType('reckonResponse', (_message.Message,), dict(
  DESCRIPTOR = _RECKONRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.reckonResponse)
  ))
_sym_db.RegisterMessage(reckonResponse)

ReckonDetails = _reflection.GeneratedProtocolMessageType('ReckonDetails', (_message.Message,), dict(
  DESCRIPTOR = _RECKONDETAILS,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.ReckonDetails)
  ))
_sym_db.RegisterMessage(ReckonDetails)

otherPlayersBetResponse = _reflection.GeneratedProtocolMessageType('otherPlayersBetResponse', (_message.Message,), dict(
  DESCRIPTOR = _OTHERPLAYERSBETRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.otherPlayersBetResponse)
  ))
_sym_db.RegisterMessage(otherPlayersBetResponse)

videoStatusRequest = _reflection.GeneratedProtocolMessageType('videoStatusRequest', (_message.Message,), dict(
  DESCRIPTOR = _VIDEOSTATUSREQUEST,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.videoStatusRequest)
  ))
_sym_db.RegisterMessage(videoStatusRequest)

videoStatusResponse = _reflection.GeneratedProtocolMessageType('videoStatusResponse', (_message.Message,), dict(
  DESCRIPTOR = _VIDEOSTATUSRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.videoStatusResponse)
  ))
_sym_db.RegisterMessage(videoStatusResponse)

dealerResponse = _reflection.GeneratedProtocolMessageType('dealerResponse', (_message.Message,), dict(
  DESCRIPTOR = _DEALERRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.dealerResponse)
  ))
_sym_db.RegisterMessage(dealerResponse)

noBetResponse = _reflection.GeneratedProtocolMessageType('noBetResponse', (_message.Message,), dict(
  DESCRIPTOR = _NOBETRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.noBetResponse)
  ))
_sym_db.RegisterMessage(noBetResponse)

tableBetResponse = _reflection.GeneratedProtocolMessageType('tableBetResponse', (_message.Message,), dict(
  DESCRIPTOR = _TABLEBETRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.tableBetResponse)
  ))
_sym_db.RegisterMessage(tableBetResponse)

TableBetDetails = _reflection.GeneratedProtocolMessageType('TableBetDetails', (_message.Message,), dict(
  DESCRIPTOR = _TABLEBETDETAILS,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.TableBetDetails)
  ))
_sym_db.RegisterMessage(TableBetDetails)

otherPlayersReckonResponse = _reflection.GeneratedProtocolMessageType('otherPlayersReckonResponse', (_message.Message,), dict(
  DESCRIPTOR = _OTHERPLAYERSRECKONRESPONSE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:protofile.game.otherPlayersReckonResponse)
  ))
_sym_db.RegisterMessage(otherPlayersReckonResponse)


# @@protoc_insertion_point(module_scope)

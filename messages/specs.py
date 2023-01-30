"""Definitions and lookup tables for MIDI messages.

TODO:

    * add lookup functions for messages definitions by type and status
      byte.
"""
# TODO: these include undefined messages.
CHANNEL_MESSAGES = set(range(0x80, 0xf0))
COMMON_MESSAGES = set(range(0xf0, 0xf8))
REALTIME_MESSAGES = set(range(0xf8, 0x100))

SYSEX_START = 0xf0
SYSEX_END = 0xf7

# Pitchwheel is a 14 bit signed integer
MIN_PITCHWHEEL = -8192
MAX_PITCHWHEEL = 8191

# Song pos is a 14 bit unsigned integer
MIN_SONGPOS = 0
MAX_SONGPOS = 16383


# 把参数整理好
def _def_msg(type_, value_names, length):
    return {
        'type': type_,
        'value_names': value_names,
        'attribute_names': set(value_names) | {'type', 'time'},
        'length': length,
    }


# TODO: 改这里的事件组
SPECS = [
    _def_msg('note_off', ('channel', 'note', 'velocity'), 3),
    _def_msg('note_on', ('channel', 'note', 'velocity'), 3),
    _def_msg('control_change', ('channel', 'control', 'value'), 3),
    _def_msg('program_change', ('channel', 'program',), 2),
]


def _make_spec_lookups(specs):
    lookup = {}
    by_status = {}
    by_type = {}

    for spec in specs:
        type_ = spec['type']
        by_type[type_] = spec

    lookup.update(by_status)
    lookup.update(by_type)

    return lookup, by_status, by_type


SPEC_LOOKUP, SPEC_BY_STATUS, SPEC_BY_TYPE = _make_spec_lookups(SPECS)

REALTIME_TYPES = {'tune_request', 'clock', 'start', 'continue', 'stop'}

DEFAULT_VALUES = {
    'channel': 0,
    'control': 0,
    'data': (),
    'frame_type': 0,
    'frame_value': 0,
    'note': 0,
    'pitch': 0,
    'pos': 0,
    'program': 0,
    'song': 0,
    'value': 0,
    'velocity': 64,

    'time': 0,
}


# TODO: should this be in decode.py?

def make_msg_dict(type_, overrides):
    """Return a new message.

    Returns a dictionary representing a message.

    Message values can be overriden.

    No type or value checking is done.  The caller is responsible for
    calling check_msg_dict().
    """
    if type_ in SPEC_BY_TYPE:
        spec = SPEC_BY_TYPE[type_]
    else:
        raise LookupError('Unknown message type {!r}'.format(type_))

    msg = {'type': type_, 'time': DEFAULT_VALUES['time']}

    for name in spec['value_names']:
        msg[name] = DEFAULT_VALUES[name]

    msg.update(overrides)

    return msg

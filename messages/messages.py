# from .specs import *
from .check import *
from .strings import msg2str, str2msg
from .encoding import *


# TODO: 优化基类
class BaseMessage(object):
    """Abstract base class for messages."""
    is_meta = False

    def __init__(self):
        self.type: str = ""

    def copy(self):
        raise NotImplementedError

    def _get_value_names(self):
        # This is overriden by MetaMessage.
        return list(SPEC_BY_TYPE[self.type]['value_names']) + ['time']

    def __repr__(self):
        items = [repr(self.type)]
        for name in self._get_value_names():
            items.append('{}={!r}'.format(name, getattr(self, name)))
        return '{}({})'.format(type(self).__name__, ', '.join(items))

    def __delattr__(self, name):
        raise AttributeError('attribute cannot be deleted')

    def __setattr__(self, name, value):
        raise AttributeError('message is immutable')

    def __eq__(self, other):
        if not isinstance(other, BaseMessage):
            raise TypeError('can\'t compare message to {}'.format(type(other)))

        # This includes time in comparison.
        return vars(self) == vars(other)


# TODO:还没有改Message类
class Message(BaseMessage):
    def __init__(self, type_, **args):
        super().__init__()
        msg_dict = make_msg_dict(type_, args)
        check_msg_dict(msg_dict)
        vars(self).update(msg_dict)

    def copy(self, **overrides):
        """Return a copy of the message.

        Attributes will be overridden by the passed keyword arguments.
        Only message specific attributes can be overridden. The message
        type can not be changed.
        """
        if not overrides:
            # Bypass all checks.
            msg = self.__class__.__new__(self.__class__)
            vars(msg).update(vars(self))
            return msg

        if 'type' in overrides and overrides['type'] != self.type:
            raise ValueError('copy must be same message type')

        if 'data' in overrides:
            overrides['data'] = bytearray(overrides['data'])

        msg_dict = vars(self).copy()
        msg_dict.update(overrides)
        check_msg_dict(msg_dict)
        return self.__class__(**msg_dict)

    @classmethod
    def from_str(cls, text):
        """Parse a string encoded message.

        This is the reverse of str(msg).
        """
        return cls(**str2msg(text))

    def __len__(self):
        return SPEC_BY_TYPE[self.type]['length']

    def __str__(self):
        return msg2str(vars(self))

    def _setattr(self, name, value):
        if name == 'type':
            raise AttributeError('type attribute is read only')
        elif name not in vars(self):
            raise AttributeError('{} message has no '
                                 'attribute {}'.format(self.type,
                                                       name))
        else:
            check_value(name, value)
            vars(self)[name] = value

    __setattr__ = _setattr

    def bytes(self):
        """Encode message and return as a list of integers."""
        return encode_message(vars(self))

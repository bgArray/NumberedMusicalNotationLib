from messages.messages import *
from messages.check import *

_META_SPEC_BY_TYPE = {}


class MetaMessage(BaseMessage):
    is_meta = True

    def __init__(self, type_, **kwargs):
        # TODO: handle unknown type?

        super().__init__()

        spec = _META_SPEC_BY_TYPE[type_]
        self_vars = vars(self)
        self_vars['type'] = type_

        for name in kwargs:
            if name not in spec.settable_attributes:
                raise ValueError(
                    '{} is not a valid argument for this message type'.format(
                        name))

        for name, value in zip(spec.attributes, spec.defaults):
            self_vars[name] = value
        self_vars['time'] = 0

        for name, value in kwargs.items():
            # Using setattr here because we want type and value checks.
            self._setattr(name, value)

    def copy(self, **overrides):
        """Return a copy of the message

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

        attrs = vars(self).copy()
        attrs.update(overrides)
        return self.__class__(**attrs)

    # FrozenMetaMessage overrides __setattr__() but we still need to
    # set attributes in __init__().
    def _setattr(self, name, value):
        spec = _META_SPEC_BY_TYPE[self.type]
        self_vars = vars(self)

        if name in spec.settable_attributes:
            if name == 'time':
                check_time(value)
            else:
                spec.check(name, value)
            self_vars[name] = value

        elif name in self_vars:
            raise AttributeError('{} attribute is read only'.format(name))
        else:
            raise AttributeError(
                '{} message has no attribute {}'.format(self.type, name))

    __setattr__ = _setattr

    def _get_value_names(self):
        """Used by BaseMessage.__repr__()."""
        spec = _META_SPEC_BY_TYPE[self.type]
        return spec.attributes + ['time']

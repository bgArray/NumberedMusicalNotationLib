


class NmnTrack(list):
    @property
    def name(self):
        """Name of the track.

        This will return the name from the first track_name meta
        message in the track, or '' if there is no such message.

        Setting this property will update the name field of the first
        track_name message in the track. If no such message is found,
        one will be added to the beginning of the track with a delta
        time of 0."""
        for message in self:
            if message.type == "track_name":
                return message.name
        else:
            return ""

    @name.setter
    def name(self, name):
        # Find the first track_name message and modify it.
        for message in self:
            if message.type == "track_name":
                message.name = name
                return
        else:
            # No track name found, add one.
            self.insert(0, MetaMessage("track_name", name=name, time=0))

    def copy(self):
        return self.__class__(self)

    def __getitem__(self, index_or_slice):
        # Retrieve item from the NmnTrack
        lst = list.__getitem__(self, index_or_slice)
        if isinstance(index_or_slice, int):
            # If an index was provided, return the list element
            return lst
        else:
            # Otherwise, construct a MidiTrack to return.
            # TODO: this make a copy of the list. Is there a better way?
            return self.__class__(lst)

    def __add__(self, other):
        return self.__class__(list.__add__(self, other))

    def __mul__(self, other):
        return self.__class__(list.__mul__(self, other))

    def __repr__(self):  # 描述自我属性方法
        if len(self) == 0:
            messages = ''
        elif len(self) == 1:
            messages = '[{}]'.format(self[0])
        else:
            messages = '[\n  {}]'.format(',\n  '.join(repr(m) for m in self))
        return '{}({})'.format(self.__class__.__name__, messages)

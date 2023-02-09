from typing import TypeVar, Union
from messages import messages
from nmn_file import meta

_T = TypeVar("_T")
_M = TypeVar(
    "_M",
    bound=Union[
        messages.BaseMessage,
        messages.Message,
        meta.MetaMessage,
        meta.UnknownMetaMessage,
    ],
)


class Measure(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measure_number: int = 0  # 小节号
        self.is_pickup: bool = False  # 是否为前奏小节

        self.message_count: int = 0  # 信息数量

    def __repr__(self):
        list_ = super().__repr__()
        return f"Measure(measure num:{self.measure_number}, {list_})"

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __eq__(self, other):
        return super().__eq__(other)  # TODO: 重写比较函数

    def __len__(self):
        return super().__len__()

    def __lt__(self, other):  # Measure对象的比较是按照小节号比较的
        return self.measure_number < other.measure_number

    def __gt__(self, other):
        return self.measure_number > other.measure_number

    def append(self, __object: _T) -> None:
        super().append(__object)

    def message_append(self, __message: _M) -> None:
        self.append(__message)
        self.message_count += 1

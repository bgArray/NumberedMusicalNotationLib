from nmn_file.nmn_pic_main import *
from nmn_file.nmn_file_main import *


class NumberedMusicalNotation(
    NumberedMusicalNotationFile,
    object,
):
    def __init__(self, file_path: str = None):
        super().__init__(file_path)

        self.file_path = file_path

    def generate_pictures(self):
        NumberedMusicalNotationPicture(self)


if __name__ == "__main__":
    NMN: NumberedMusicalNotation = NumberedMusicalNotation("./resources/goal.txt")
    print(type(NMN))
    print(NMN.get_path())
    NMN.generate_pictures()

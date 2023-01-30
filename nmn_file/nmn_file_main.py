import io


class NumberedMusicalNotationFile(object):
    def __init__(
        self,
        file_path: str,
    ):
        self.file_path: str = file_path

        if self.file_path is None:
            self.no_path = True
        else:
            self.no_path = False
            with io.open(self.file_path, "r", encoding="utf-8") as r:
                self._load(r)

    def __getitem__(self, item):
        pass

    def __eq__(self, other):
        pass

    def __len__(self):
        pass

    def get_path(self):
        return self.file_path

    def _load(self, in_file):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from abc import abstractmethod
from typing import Tuple, Union


################################################################################

class FileSystemObject(object):
    """
    Superclass for File and Directory classes. Any file system object has its
    name and a parent directory.
    """

################################################################################

    def __init__(self, name: str, parent_dir: Union["Directory", None]):
        """
        :param name: file system object name (string)
        :param parent_dir: file system object parent directory (Directory or
        None in case of the root directory)
        """

        self._name = name
        self._parent_dir = parent_dir

################################################################################

    @property
    def parent_dir(self) -> Union["Directory", None]:
        """
        :return: parent directory of this file system object (Directory or None
        in case of the root directory)
        """

        return self._parent_dir

################################################################################

    @property
    def name(self) -> str:
        """
        :return: file system object name (string)
        """

        return self._name

################################################################################

    @property
    @abstractmethod
    def size(self) -> int:
        """
        :return: file system object size (integer)
        """

        ...

################################################################################


################################################################################

class Directory(FileSystemObject):
    """
    A directory class. It has its contents - a list of both Directory and File
    class instances. Its size is defined as the sum of its contents sizes.
    """

################################################################################

    def __init__(self, name: str, parent_dir: Union["Directory", None]):
        """
        :param name: directory name (string)
        :param parent_dir: parent directory (Directory or None in case of the
        root directory)
        """

        super().__init__(name, parent_dir)
        self._contents = []

################################################################################

    @property
    def contents(self) -> Tuple[FileSystemObject, ...]:
        """
        :return: tuple of directory contents (Directory or File instances)
        """

        return tuple(self._contents)

################################################################################

    @property
    def size(self) -> int:
        """
        :return: directory size (integer)
        """

        return sum(item.size for item in self._contents)

################################################################################

    def add_content(self, content: FileSystemObject) -> None:
        """
        Adds new File or Directory instance to the directory contents.

        :param content: File or Directory instance
        """

        self._contents.append(content)

################################################################################


################################################################################

class File(FileSystemObject):
    """
    A file class. Its size is defined explicitly.
    """

################################################################################

    def __init__(self, name: str, parent_dir: Directory, size: int):
        """
        :param name: file name (string)
        :param parent_dir: parent directory (Directory)
        :param size: file size (integer)
        """

        super().__init__(name, parent_dir)
        self._size = size

################################################################################

    @property
    def size(self) -> int:
        """
        :return: file size (integer)
        """

        return self._size

################################################################################

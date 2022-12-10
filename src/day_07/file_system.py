__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from re import compile
from src.day_07.file_system_object import File, Directory


################################################################################

class FileSystem(object):
    """
    File system class; it first loads the tree structure of directories and
    files from the provided log file. Then the tree structure is searched with
    BFS algorithm and all important information for solving both puzzles are
    stored. Puzzles solutions are then provided under two property methods.
    """

    # log file that is used to create the files and directories tree structure
    INPUT_FILE_PATH = "src/day_07/input.txt"
    # max size of a directory which is a good candidate for deletion; used in
    # the puzzle 1
    SMALL_DIRECTORY_SIZE = 100000
    # total disk space available to the filesystem
    TOTAL_DISC_SPACE = 70000000
    # minimum needed unused space to run the update
    UPDATE_NEEDED = 30000000

    PROMPT = r"\$"
    PARENT_DIR = ".."
    DIR_NAME_GROUP = "dir_name"
    FILE_NAME_GROUP = "file_name"
    FILE_SIZE_GROUP = "file_size"
    CD_PATTERN = compile(r"{} cd (?P<{}>.+)".format(PROMPT, DIR_NAME_GROUP))
    DIR_PATTERN = compile(r"dir (?P<{}>.+)".format(DIR_NAME_GROUP))
    FILE_PATTERN = compile(r"(?P<{}>\d+) (?P<{}>.+)".format(FILE_SIZE_GROUP,
                                                            FILE_NAME_GROUP))

################################################################################

    def __init__(self):
        """
        Load the file system from the provided log file, then search the tree
        structure and store all information needed to solve the puzzles.
        """

        self._root_dir = Directory("/", None)
        self._load_file_system()
        self._small_directories = []
        self._removal_candidates = []
        self._bfs()

################################################################################

    def _load_file_system(self) -> None:
        """
        Loads the file system tree structure from the provided log file.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            lines = f.readlines()
            current_dir = None

            for line in lines:
                result = self.CD_PATTERN.search(line)
                if result is not None:
                    # the command is cd [dirname]
                    dir_name = result.group(self.DIR_NAME_GROUP)
                    if dir_name == self.PARENT_DIR:
                        # move up one level
                        current_dir = current_dir.parent_dir
                    else:
                        # move down to the specified directory
                        try:
                            current_dir = next(filter(
                                lambda item: item.name == dir_name,
                                current_dir.contents))
                        except AttributeError:
                            # at the beginning, there is no current directory
                            # set; set it to the root directory; this is the
                            # first command in the log file anyway
                            current_dir = self._root_dir

                else:
                    result = self.DIR_PATTERN.search(line)
                    if result is not None:
                        # the current directory contains a directory with a
                        # specified name
                        dir_name = result.group(self.DIR_NAME_GROUP)
                        # update the tree structure
                        current_dir.add_content(
                            Directory(dir_name, current_dir))
                    else:
                        result = self.FILE_PATTERN.search(line)
                        if result is not None:
                            # the current directory contains a file with a
                            # specified size and name
                            file_name = result.group(self.FILE_NAME_GROUP)
                            file_size = int(result.group(self.FILE_SIZE_GROUP))
                            # update the tree structure
                            current_dir.add_content(
                                File(file_name, current_dir, file_size))

################################################################################

    def _bfs(self) -> None:
        """
        Search the file system tree structure using BFS algorithm.
        """

        # free space left on the file system
        free_space = self.TOTAL_DISC_SPACE - self._root_dir.size
        # space that needs to be further freed for the update procedure to work
        to_free = self.UPDATE_NEEDED - free_space
        # unprocessed directories
        queue = [self._root_dir]

        while len(queue) > 0:
            fs_object = queue.pop(0)
            try:
                queue += fs_object.contents
                # fs_object is a directory
                if fs_object.size <= self.SMALL_DIRECTORY_SIZE:
                    # store removal candidates for puzzle 1
                    self._small_directories.append(fs_object)
                if fs_object.size >= to_free:
                    # store removal candidates for puzzle 2
                    self._removal_candidates.append(fs_object)
            except AttributeError:
                # fs_object is a file; no need to do anything
                pass

################################################################################

    @property
    def small_directories_sizes_sum(self) -> int:
        """
        :return: the sum of the total sizes of directories with a total size of
        at most 100000
        """

        return sum(directory.size for directory in self._small_directories)

################################################################################

    @property
    def smallest_directory_size_to_remove(self) -> int:
        """
        :return: size of the smallest directory that, if deleted, would free up
        enough space on the filesystem to run the update
        """

        return min(directory.size for directory in self._removal_candidates)

################################################################################

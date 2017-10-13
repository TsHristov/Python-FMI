class NodeDoesNotExistError(Exception):
    pass


class DestinationNodeDoesNotExistError(Exception):
    pass


class NotEnoughSpaceError(Exception):
    pass


class DestinationNodeExistError(Exception):
    pass


class NonExplicitDirectoryDeletionError(Exception):
    pass


class NonEmptyDirectoryDeletionError(Exception):
    pass


class FileSystem:
    def __init__(self, size):
        """Initialize a FileSystem object.

        Args:
            size: The initial file system size in bytes.
        """
        self._size = size
        self._available_size = size  # remaining size
        self._file_system = {'/': {}}

    @property
    def size(self):
        """Return file system`s size in bytes."""
        return self._size

    @property
    def available_size(self):
        """Return remaining file system`s size in bytes."""
        return self._available_size

    def get_node(self, path):
        """Return File/Directory object found at path.

        Args:
            path: Path to file/directory.

        Raises:
            NodeDoesNotExistError: If no file/directory at path is found.
        """
        pass

    def create(self, path, directory=False, content=''):
        """Creates file or directory at the given path.

        Args:
            content: Describes file`s content if file is to be created.
                     Does not apply, if directory is to be created.
        Raises:
            DestinationNodeDoesNotExistError: When path does not exist.

            NotEnoughSpaceError:
                When an attempt to create a file/directory
                larger than the available space is made.

            DestinationNodeExistError: When file/directory already exist.
        """
        pass

    def remove(self, path, directory=False, force=True):
        """Deletes file/directory at path.

        Raises:
            NonExplicitDirectoryDeletionError:
                When path points to a directory, but
                directory is not explicitly set to True.

            NonEmptyDirectoryDeletionError:
                When directory is empty and directory=True, but
                force is not explicitly set to True.

            NodeDoesNotExistError:
                When the file/directory to be deleted
                does not exist.
        """
        pass

    def move(self, source, destination):
        """ Moves the file/directory from source to destination.

        Raises:
            SourceDoesNotExistError:
                When source does not exists in the file system.

            DestinationNodeDoesNotExistError:
                When destination does not exist in the file system.

            DestinationNotADirectoryError:
                When destination exists, but is not a directory.

            DestinationNodeExistError:
                When destination is a directory, but already contains
                file/directory with name of source.
        """
        pass

    def link(self, source, destination, symbolic=True):
        """Creates link with path destination pointing to source.

        Args:
            symbolic: Determines whether the created link to be soft
                      or hard.

        Raises:
            NodeDoesNotExistsError:
                When source does not exists and symbolic=True.

            SourceNodeDoesNotExistError:
                When an attempt to create a hard link to
                non-existent file is made.
        """
        pass

    def mount(self, file_system, path):
        """Mounts file_system to path.

        Args:
            file_system:
                The file system to be mounted to the current.
            path:
                The path on which the file_system should be mounted.

        Raises:
            MountPointNotEmptyError:
                When path points to non-empty directory.

            MountPointNotADirectoryError:
                When path is not a directory.

            MountPointDoesNotExistError:
                When path does not exist.
        """
        pass

    def unmount(self, path):
        """Unmounts mounted file system.

        Raises:
            NodeDoesNotExistError:
                When path does not exist.

            NotAMountPointError:
                When path does not contain mounted file system.
        """
        pass

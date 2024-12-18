# -*- coding: utf-8 -*-
"""The gzip file-like object."""

from dfvfs.file_io import file_object_io
from dfvfs.lib import errors
from dfvfs.lib import gzipfile
from dfvfs.resolver import resolver


class GzipFile(file_object_io.FileObjectIO):
  """File input/output (IO) object of a gzip file."""

  @property
  def comments(self):
    """Retrieves the comments.

    Returns:
      list[str]: comments of the members.
    """
    return [member.comment for member in self._file_object.members]

  @property
  def modification_times(self):
    """Retrieves the modification times.

    Returns:
      list[str]: modification times of the members.
    """
    return [member.modification_time for member in self._file_object.members]

  @property
  def original_filenames(self):
    """Retrieves the original filenames.

    Returns:
      list[str]: original filenames of the members.
    """
    return [member.original_filename for member in self._file_object.members]

  @property
  def operating_systems(self):
    """Retrieves the operating system values.

    Returns:
      list[str]: operating system values of the members.
    """
    return [member.operating_system for member in self._file_object.members]

  @property
  def uncompressed_data_size(self):
    """Retrieves the uncompressed data size.

    Returns:
      int: uncompressed data size.
    """
    return self._file_object.uncompressed_data_size

  def _OpenFileObject(self, path_spec):
    """Opens the file-like object defined by path specification.

    Args:
      path_spec (PathSpec): path specification.

    Returns:
      pyvde.volume: gzip file-like object.

    Raises:
      PathSpecError: if the path specification is incorrect.
    """
    if not path_spec.HasParent():
      raise errors.PathSpecError(
          'Unsupported path specification without parent.')

    file_object = resolver.Resolver.OpenFileObject(
        path_spec.parent, resolver_context=self._resolver_context)

    gzip_compressed_stream = gzipfile.GzipCompressedStream()
    gzip_compressed_stream.Open(file_object)

    return gzip_compressed_stream

  # Note: that the following functions do not follow the style guide
  # because they are part of the file-like object interface.
  # pylint: disable=invalid-name

  def get_size(self):
    """Retrieves the size of the file-like object.

    Returns:
      int: size of the file-like object data.

    Raises:
      IOError: if the file-like object has not been opened.
      OSError: if the file-like object has not been opened.
    """
    if not self._is_open:
      raise IOError('Not opened.')

    return self._file_object.uncompressed_data_size

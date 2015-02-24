
import os
import struct
import zlib

from pysword import books


class Module(object):


  def __init__(self, module, path='./modules'):
    self.module = module
    self.path = path
    self.files = {
      'ot': self.__get_files('ot'),
      'nt': self.__get_files('nt')
    }

    if not self.files['ot'] and not self.files['not']:
      raise ValueError("Could not find module in %s" % self.path)


  def read(self, book, chapter, verse=None):
    text = []
    book = books.get_book(book)
    for verse in range(book['chapters'][chapter-1]):
      verse = verse + 1
      text.append(self.__read_index(book['testament'], books.get_index(book, chapter, verse)))
    return ' '.join(text)


  def __get_files(self, testament):
    try:
      v_path = os.path.join(self.path, self.module, '%s.bz%s' % (testament, 'v'))
      s_path = os.path.join(self.path, self.module, '%s.bz%s' % (testament, 's'))
      z_path = os.path.join(self.path, self.module, '%s.bz%s' % (testament, 'z'))
      return [open(name, 'rb') for name in (v_path, s_path, z_path)]
    except OSError:
      return []


  def __read_index(self, testament, index):
    verse_to_buf, buf_to_loc, text = self.files[testament]
    verse_to_buf.seek(10*index)
    buf_num, verse_start, verse_len = struct.unpack('<IIH', verse_to_buf.read(10))
    __uncompress = self.__uncompress(testament, buf_num)
    return __uncompress[verse_start:verse_start+verse_len].replace("<q", "<q class=\"q\"").replace("<lb", "<div").replace("type=", "class=")


  def __uncompress(self, testament, buf_num):
    verse_to_buf, buf_to_loc, text = self.files[testament]
    buf_to_loc.seek(buf_num*12)
    offset, size, uc_size = struct.unpack('<III', buf_to_loc.read(12))
    text.seek(offset)
    compressed_data = text.read(size)
    return zlib.decompress(compressed_data)

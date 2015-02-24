#!/usr/bin/env python

import os
import struct
import zlib


class ZModule(object):

  def __init__(self, module, path='./modules'):
    self.module = module
    self.path = path
    self.files = {
      'ot': self.get_files('ot'),
      'nt': self.get_files('nt')
    }

    if not self.files['ot'] and not self.files['not']:
      raise ValueError("Could not find module in %s" % self.path)

  def get_files(self, testament):
    try:
      v_path = os.path.join(self.path, self.module, '%s.bz%s' % (testament, 'v'))
      s_path = os.path.join(self.path, self.module, '%s.bz%s' % (testament, 's'))
      z_path = os.path.join(self.path, self.module, '%s.bz%s' % (testament, 'z'))
      return [open(name, 'rb') for name in (v_path, s_path, z_path)]
    except OSError:
      return []

  def text_for_index(self, testament, index):
    verse_to_buf, buf_to_loc, text = self.files[testament]

    verse_to_buf.seek(10*index)
    buf_num, verse_start, verse_len = struct.unpack('<IIH', verse_to_buf.read(10))

    uncompressed_text = self.uncompressed_text(testament, buf_num)
    return uncompressed_text[verse_start:verse_start+verse_len].replace("<q", "<q class=\"q\"").replace("<lb", "<div").replace("type=", "class=")

  def uncompressed_text(self, testament, buf_num):
    verse_to_buf, buf_to_loc, text = self.files[testament]

    buf_to_loc.seek(buf_num*12)
    offset, size, uc_size = struct.unpack('<III', buf_to_loc.read(12))

    text.seek(offset)
    compressed_data = text.read(size)
    return zlib.decompress(compressed_data)

  def text_for_ref(self, book, chapter, verse):
    """Get the text for a given reference"""
    chapter, verse = int(chapter), int(verse)
    idx = books.get_index(book, chapter, verse)
    return self.text_for_index(book['testament'], idx)

  def all_verses_in_book(self, book, chapter):
    text = []
    book = books.get_book(book)
    for verse in range(book['chapters'][chapter-1]):
      verse = verse + 1
      text.append(self.text_for_index(book['testament'], books.get_index(book, chapter, verse)))

    return ' '.join(text)

class Books(object):

  def __init__(self):
    self.ot_books = []
    self.nt_books = []

    self.ot_offset = 1
    self.nt_offset = 1

  def add_ot_book(self, name, chapters):
    offset = 1
    offsets = []

    for length in chapters:
      offset += 1
      offsets.append(offset)
      offset += length

    self.ot_books.append({
      'testament': 'ot',
      'name': name,
      'chapters': chapters,
      'offset': self.ot_offset,
      'offsets': offsets
    })

    self.ot_offset = self.ot_offset + offset

  def add_nt_book(self, name, chapters):
    offset = 1
    offsets = []

    for length in chapters:
      offset = offset + 1
      offsets.append(offset)
      offset = offset + length

    self.nt_books.append({
      'testament': 'nt',
      'name': name,
      'chapters': chapters,
      'offset': self.nt_offset,
      'offsets': offsets
    })

    self.nt_offset = self.nt_offset + offset

  def get_book(self, name):
    name = name.lower()

    for book in self.ot_books:
      if name in book['name']:
        return book

    for book in self.nt_books:
      if name in book['name']:
        return book

  def get_index(self, book, chapter, verse):
    return book['offset'] + book['offsets'][chapter-1] + verse

books = Books()

books.add_ot_book('genesis', [31, 25, 24, 26, 32, 22, 24, 22, 29, 32, 32, 20, 18, 24, 21, 16, 27, 33, 38, 18, 34, 24, 20, 67, 34, 35, 46, 22, 35, 43, 55, 32, 20, 31, 29, 43, 36, 30, 23, 23, 57, 38, 34, 34, 28, 34, 31, 22, 33, 26])
books.add_ot_book('exodus', [22, 25, 22, 31, 23, 30, 25, 32, 35, 29, 10, 51, 22, 31, 27, 36, 16, 27, 25, 26, 36, 31, 33, 18, 40, 37, 21, 43, 46, 38, 18, 35, 23, 35, 35, 38, 29, 31, 43, 38])
books.add_ot_book('leviticus', [17, 16, 17, 35, 19, 30, 38, 36, 24, 20, 47, 8, 59, 57, 33, 34, 16, 30, 37, 27, 24, 33, 44, 23, 55, 46, 34])
books.add_ot_book('numbers', [54, 34, 51, 49, 31, 27, 89, 26, 23, 36, 35, 16, 33, 45, 41, 50, 13, 32, 22, 29, 35, 41, 30, 25, 18, 65, 23, 31, 40, 16, 54, 42, 56, 29, 34, 13])
books.add_ot_book('deuteronomy', [46, 37, 29, 49, 33, 25, 26, 20, 29, 22, 32, 32, 18, 29, 23, 22, 20, 22, 21, 20, 23, 30, 25, 22, 19, 19, 26, 68, 29, 20, 30, 52, 29, 12])
books.add_ot_book('joshua', [18, 24, 17, 24, 15, 27, 26, 35, 27, 43, 23, 24, 33, 15, 63, 10, 18, 28, 51, 9, 45, 34, 16, 33])
books.add_ot_book('judges', [36, 23, 31, 24, 31, 40, 25, 35, 57, 18, 40, 15, 25, 20, 20, 31, 13, 31, 30, 48, 25])
books.add_ot_book('ruth', [22, 23, 18, 22])
books.add_ot_book('1 samuel', [28, 36, 21, 22, 12, 21, 17, 22, 27, 27, 15, 25, 23, 52, 35, 23, 58, 30, 24, 42, 15, 23, 29, 22, 44, 25, 12, 25, 11, 31, 13])
books.add_ot_book('2 samuel', [27, 32, 39, 12, 25, 23, 29, 18, 13, 19, 27, 31, 39, 33, 37, 23, 29, 33, 43, 26, 22, 51, 39, 25])
books.add_ot_book('1 kings', [53, 46, 28, 34, 18, 38, 51, 66, 28, 29, 43, 33, 34, 31, 34, 34, 24, 46, 21, 43, 29, 53])
books.add_ot_book('2 kings', [18, 25, 27, 44, 27, 33, 20, 29, 37, 36, 21, 21, 25, 29, 38, 20, 41, 37, 37, 21, 26, 20, 37, 20, 30])
books.add_ot_book('1 chronicles', [54, 55, 24, 43, 26, 81, 40, 40, 44, 14, 47, 40, 14, 17, 29, 43, 27, 17, 19, 8, 30, 19, 32, 31, 31, 32, 34, 21, 30])
books.add_ot_book('2 chronicles', [17, 18, 17, 22, 14, 42, 22, 18, 31, 19, 23, 16, 22, 15, 19, 14, 19, 34, 11, 37, 20, 12, 21, 27, 28, 23, 9, 27, 36, 27, 21, 33, 25, 33, 27, 23])
books.add_ot_book('ezra', [11, 70, 13, 24, 17, 22, 28, 36, 15, 44])
books.add_ot_book('nehemiah', [11, 20, 32, 23, 19, 19, 73, 18, 38, 39, 36, 47, 31])
books.add_ot_book('esther', [22, 23, 15, 17, 14, 14, 10, 17, 32, 3])
books.add_ot_book('job', [22, 13, 26, 21, 27, 30, 21, 22, 35, 22, 20, 25, 28, 22, 35, 22, 16, 21, 29, 29, 34, 30, 17, 25, 6, 14, 23, 28, 25, 31, 40, 22, 33, 37, 16, 33, 24, 41, 30, 24, 34, 17])
books.add_ot_book('psalms', [6, 12, 8, 8, 12, 10, 17, 9, 20, 18, 7, 8, 6, 7, 5, 11, 15, 50, 14, 9, 13, 31, 6, 10, 22, 12, 14, 9, 11, 12, 24, 11, 22, 22, 28, 12, 40, 22, 13, 17, 13, 11, 5, 26, 17, 11, 9, 14, 20, 23, 19, 9, 6, 7, 23, 13, 11, 11, 17, 12, 8, 12, 11, 10, 13, 20, 7, 35, 36, 5, 24, 20, 28, 23, 10, 12, 20, 72, 13, 19, 16, 8, 18, 12, 13, 17, 7, 18, 52, 17, 16, 15, 5, 23, 11, 13, 12, 9, 9, 5, 8, 28, 22, 35, 45, 48, 43, 13, 31, 7, 10, 10, 9, 8, 18, 19, 2, 29, 176, 7, 8, 9, 4, 8, 5, 6, 5, 6, 8, 8, 3, 18, 3, 3, 21, 26, 9, 8, 24, 13, 10, 7, 12, 15, 21, 10, 20, 14, 9, 6])
books.add_ot_book('proverbs', [33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33, 33, 28, 24, 29, 30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31])
books.add_ot_book('ecclesiastes', [18, 26, 22, 16, 20, 12, 29, 17, 18, 20, 10, 14])
books.add_ot_book('song of solomon', [17, 17, 11, 16, 16, 13, 13, 14])
books.add_ot_book('isaiah', [31, 22, 26, 6, 30, 13, 25, 22, 21, 34, 16, 6, 22, 32, 9, 14, 14, 7, 25, 6, 17, 25, 18, 23, 12, 21, 13, 29, 24, 33, 9, 20, 24, 17, 10, 22, 38, 22, 8, 31, 29, 25, 28, 28, 25, 13, 15, 22, 26, 11, 23, 15, 12, 17, 13, 12, 21, 14, 21, 22, 11, 12, 19, 12, 25, 24])
books.add_ot_book('jeremiah', [19, 37, 25, 31, 31, 30, 34, 22, 26, 25, 23, 17, 27, 22, 21, 21, 27, 23, 15, 18, 14, 30, 40, 10, 38, 24, 22, 17, 32, 24, 40, 44, 26, 22, 19, 32, 21, 28, 18, 16, 18, 22, 13, 30, 5, 28, 7, 47, 39, 46, 64, 34])
books.add_ot_book('lamentations', [22, 22, 66, 22, 22])
books.add_ot_book('ezekiel', [28, 10, 27, 17, 17, 14, 27, 18, 11, 22, 25, 28, 23, 23, 8, 63, 24, 32, 14, 49, 32, 31, 49, 27, 17, 21, 36, 26, 21, 26, 18, 32, 33, 31, 15, 38, 28, 23, 29, 49, 26, 20, 27, 31, 25, 24, 23, 35])
books.add_ot_book('daniel', [21, 49, 30, 37, 31, 28, 28, 27, 27, 21, 45, 13])
books.add_ot_book('hosea', [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9])
books.add_ot_book('joel', [20, 32, 21])
books.add_ot_book('amos', [15, 16, 15, 13, 27, 14, 17, 14, 15])
books.add_ot_book('obadiah', [21])
books.add_ot_book('jonah', [17, 10, 10, 11])
books.add_ot_book('micah', [16, 13, 12, 13, 15, 16, 20])
books.add_ot_book('nahum', [15, 13, 19])
books.add_ot_book('habakkuk', [17, 20, 19])
books.add_ot_book('zephaniah', [18, 15, 20])
books.add_ot_book('haggai', [15, 23])
books.add_ot_book('zechariah', [21, 13, 10, 14, 11, 15, 14, 23, 17, 12, 17, 14, 9, 21])
books.add_ot_book('malachi', [14, 17, 18, 6])

books.add_nt_book('matthew', [25, 23, 17, 25, 48, 34, 29, 34, 38, 42, 30, 50, 58, 36, 39, 28, 27, 35, 30, 34, 46, 46, 39, 51, 46, 75, 66, 20])
books.add_nt_book('mark', [45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72, 47, 20])
books.add_nt_book('luke', [80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59, 35, 35, 32, 31, 37, 43, 48, 47, 38, 71, 56, 53])
books.add_nt_book('john', [51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31, 27, 33, 26, 40, 42, 31, 25])
books.add_nt_book('acts', [26, 47, 26, 37, 42, 15, 60, 40, 43, 48, 30, 25, 52, 28, 41, 40, 34, 28, 41, 38, 40, 30, 35, 27, 27, 32, 44, 31])
books.add_nt_book('romans', [32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 23, 33, 27])
books.add_nt_book('1 corinthians', [31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40, 58, 24])
books.add_nt_book('2 corinthians', [24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14])
books.add_nt_book('galatians', [24, 21, 29, 31, 26, 18])
books.add_nt_book('ephesians', [23, 22, 21, 32, 33, 24])
books.add_nt_book('philippians', [30, 30, 21, 23])
books.add_nt_book('colossians', [29, 23, 25, 18])
books.add_nt_book('1 thessalonians', [10, 20, 13, 18, 28])
books.add_nt_book('2 thessalonians', [12, 17, 18])
books.add_nt_book('1 timothy', [20, 15, 16, 16, 25, 21])
books.add_nt_book('2 timothy', [18, 26, 17, 22])
books.add_nt_book('titus', [16, 15, 15])
books.add_nt_book('philemon', [25])
books.add_nt_book('hebrews', [14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25])
books.add_nt_book('james', [27, 26, 18, 17, 20])
books.add_nt_book('1 peter', [25, 25, 22, 19, 14])
books.add_nt_book('2 peter', [21, 22, 18])
books.add_nt_book('1 john', [10, 29, 24, 21, 21])
books.add_nt_book('2 john', [13])
books.add_nt_book('3 john', [14])
books.add_nt_book('jude', [25])
books.add_nt_book('revelations', [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21, 18, 24, 21, 15, 27, 21])

import re

class LetterMatrix:
  """
  Represents a two-dimensional array in which each element is either
  a single letter or the empty string.
  """
  LETTER_REGEX = re.compile('^[A-Za-z]?$')

  NEIGHBOR_TRANSFORMS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
  ]

  def __init__(self, matrix):
    LetterMatrix.validate(matrix)
    self.matrix = matrix

  @staticmethod
  def validate(matrix):
    """
    Throw an exception if the given array doesn't meet our 
    requirements:
     - Must be a two-dimensional array with each row having 
       the same length
     - Each element of each row must be a string of length 0
       or 1. If length 1, single character must be a letter A-Z
       (case insensitive).
    """
    row_lengths = set(map(lambda x: len(x), matrix))
    if len(row_lengths) > 1:
      raise InvalidLetterMatrixException("All rows must be the same length.")

    for row in matrix:
      # Guard against `row` being a multi-character string
      if not isinstance(row, list):
        raise InvalidLetterMatrixException("Matrix must be a list of lists.")
      for elm in row:
        if not LetterMatrix.LETTER_REGEX.match(elm):
          raise InvalidLetterMatrixException(
            "Only single letters are permitted, {} is invalid.".format(elm)
          )
    return True

  def row_count(self):
    """Returns the number of rows in the matrix."""
    return len(self.matrix)

  def column_count(self):
    """Returns the number of columns in the matrix."""
    return len(self.matrix[0])

  def element(self, r, c):
    """Return the element at the given coordinates."""
    return self.matrix[r][c]

  def exists(self, r, c):
    """Return True if an element exists at the given coordinates, that
    is, if the given coordinates are within the matrix."""
    return r >= 0 and r < self.row_count() and \
           c >= 0 and c < self.column_count()

  def is_letter(self, r, c):
    """True if the given element exists and is a letter, False otherwise."""
    return self.exists(r, c) and self.element(r, c) != ""

  def neighbors(self, r, c):
    """
    Return an array of tuples (row, column) representing elements adjacent to 
    the one at the given coordinates. Empty elements are not included.
    Adjacent elements include those diagonal to the given one, so each
    element has a minimum of 0 and a maximum of 8 neightbors.
    """
    neighbors_arr = []
    for t in LetterMatrix.NEIGHBOR_TRANSFORMS:
      candidate = (r + t[0], c + t[1])
      if self.is_letter(candidate[0], candidate[1]):
        neighbors_arr.append(candidate)
    return neighbors_arr

  def find_words(self, length, prefix=""):
    """
    Return a sorted list of all strings of the given length that can be 
    made by combining the letters in the matrix, following these rules:
     - The first letter in the word can be any element in the matrix
     - Adjacent letters in the word must be neighbors in the matrix
     - Each element in the matrix can be used only once
     - The word must begin with the given prefix. If the prefix is 
       longer than the desired word length no solutions will exist.
    """
    words = set()
    for row in range(self.row_count()):
      for col in range(self.column_count()):
        if self.is_letter(row, col):
          words |= self._rec_find_words(length, row, col, {(row, col)}, prefix)
    return sorted(list(words))

  def _rec_find_words(self, length, start_row, start_col, used_coords, prefix):
    """
    Find words in 

    length (int) -- Return words of exactly this length
    start_row (int), start_col (int) -- the coordinates of the letter
      to start the word with. We assume this element contains a valid 
      letter.
    used_coords (set of (int, int)) -- Contains the coordinates used 
      already in this word, which shouldn't be reused.
    prefix (str) -- words must begin with this prefix. If the prefix
      is longer than the desired word length, no solutions will exist.
    """
    words = set()
    head = self.element(start_row, start_col)

    if len(prefix) > length:
      # Short circuit if prefix length means there are no valid solutions
      pass
    elif prefix and prefix[0] != head:
      # Short circuit if this path doesn't result in words that 
      # match our prefix
      pass
    elif length == 1:
      words.add(head)
    elif length > 1:
      for (r, c) in self.neighbors(start_row, start_col):
        if (r, c) not in used_coords:
          tails = self._rec_find_words(
            length - 1, 
            r, c, 
            used_coords | {(r, c)}, 
            prefix[1:]
          )
          words |= { head + tail for tail in tails }
    
    return words


class InvalidLetterMatrixException(Exception):
  pass

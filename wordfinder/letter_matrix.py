import re
import copy

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
    # TODO control whether columns are collapsed at an instance level?

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

  def elements(self, coords):
    """Given a list of coordinates, return a list containing the values
    in the matrix they correspond to."""
    return [self.element(r, c) for (r, c) in coords]

  def word_at(self, coords):
    """Given a list of coordinates, return the string made from joining
    the letters at those locations."""
    return "".join(self.elements(coords))

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

  def find_words(self, length, prefix="", dictionary=None):
    """
    Return a sorted list of all strings of the given length that can be 
    made by combining the letters in the matrix, following these rules:
     - The first letter in the word can be any element in the matrix
     - Adjacent letters in the word must be neighbors in the matrix
     - Each element in the matrix can be used only once
     - The word must begin with the given prefix. If the prefix is 
       longer than the desired word length no solutions will exist.
     - If a dictionary is given, the word must appear in it.
    """
    return sorted(
      [self.word_at(w) for w in self.find_word_coords(length, prefix, dictionary)]
    )

  def find_word_coords(self, length, prefix="", dictionary=None):
    """
    Return a list of coordinate lists of the given length that correspond
    to words that can be made by combining the letters in the matrix, 
    following these rules:
     - The first element in the word can be any element in the matrix
     - Adjacent elements in the word must be neighbors in the matrix
     - Each element in the matrix can be used only once
     - The word must begin with the given prefix. If the prefix is 
       longer than the desired word length no solutions will exist.
     - If a dictionary is given, the word must appear in it.

    This is similar to finding words in the matrix, but we return the
    locations of the letters in the word rather than the letters 
    themselves. This is useful because there can be multiple ways to
    make a given word. 
    """
    word_coords = []
    for row in range(self.row_count()):
      for col in range(self.column_count()):
        if self.is_letter(row, col):
          potential_word_coords = self._rec_find_word_coords(
            length, row, col, {(row, col)}, prefix
          )
          if dictionary:
            potential_word_coords = [ 
              w for w in potential_word_coords if dictionary.contains(self.word_at(w)) 
            ]
          word_coords += potential_word_coords
    return word_coords

  def _rec_find_word_coords(
      self, length, start_row, start_col, used_coords, prefix
  ):
    """
    Find word locations in the matrix as described in `find_word_coords` 
    matching the given requirements.

    length (int) -- Return words of exactly this length
    start_row (int), start_col (int) -- the coordinates of the letter
      to start the word with. We assume this element contains a valid 
      letter.
    used_coords (set of (int, int)) -- Contains the coordinates used 
      already in this word, which shouldn't be reused.
    prefix (str) -- words must begin with this prefix. If the prefix
      is longer than the desired word length, no solutions will exist.
    """
    word_coords = []
    head_letter = self.element(start_row, start_col)

    if len(prefix) > length:
      # Short circuit if prefix length means there are no valid solutions
      pass
    elif prefix and prefix[0].upper() != head_letter.upper():
      # Short circuit if this path doesn't result in words that 
      # match our prefix
      pass
    elif length == 1:
      word_coords += [[(start_row, start_col)]]
    elif length > 1:
      for (r, c) in self.neighbors(start_row, start_col):
        if (r, c) not in used_coords:
          tails = self._rec_find_word_coords(
            length - 1, 
            r, c, 
            used_coords | {(r, c)}, 
            prefix[1:]
          )
          word_coords += [[(start_row, start_col)] + tail for tail in tails ]
    
    return word_coords

  def remove_word(self, coords, collapse=True):
    """
    Remove the letters at the given coordinates (replace with the 
    empty string). If `collapse` is True, we also collapse each column 
    of letters down so that no letter is "above" an empty string. 
    """
    for (r, c) in coords:
      self.matrix[r][c] = ''

    if collapse:
      self.collapse_columns()

  def collapse_columns(self):
    """
    Shift the elements in the matrix so that each column is "collapsed."
    Within each column, all empty elements should be in rows higher 
    than all letters. To achieve this, we shift letters down to lower 
    rows in each column. No letter changes column, and letters retain
    their ordering within each column. 
    """
    for col in range(self.column_count()):
      for row in range(self.row_count() - 1):
        if self.element(row, col) == '':
          next_letter_coord = self._next_letter_above(row, col)
          if next_letter_coord:
            (ltr_row, ltr_col) = next_letter_coord
            self.matrix[row][col] = self.element(ltr_row, ltr_col)
            self.matrix[ltr_row][ltr_col] = ''


  def _next_letter_above(self, row, col):
    """Return the (row, col) of the letter with the same col and lowest
    row above this one, or None if no such letter exists."""
    ret_coords = None
    this_row = row + 1
    while this_row < self.row_count() and ret_coords is None:
      if self.is_letter(this_row, col):
        ret_coords = (this_row, col)
      this_row += 1
    return ret_coords


class InvalidLetterMatrixException(Exception):
  pass

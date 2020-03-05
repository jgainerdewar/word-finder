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

  def element(self, r, c):
    """Return the element at the given coordinates."""
    return self.matrix[r][c]

  def exists(self, r, c):
    """Return True if an element exists at the given coordinates, that
    is, if the given coordinates are within the matrix."""
    return r >= 0 and r < len(self.matrix) and \
           c >= 0 and c < len(self.matrix[r])

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
    

class InvalidLetterMatrixException(Exception):
  pass
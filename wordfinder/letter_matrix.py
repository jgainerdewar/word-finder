import re

class LetterMatrix:
  """
  Represents a two-dimensional array in which each element is either
  a single letter or the empty string.
  """
  LETTER_REGEX = re.compile('^[A-Za-z]?$')

  def __init__(self, matrix):
    validate_matrix(matrix)
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
    

class InvalidLetterMatrixException(Exception):
  pass
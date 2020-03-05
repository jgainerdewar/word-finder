from wordfinder import LetterMatrix, InvalidLetterMatrixException
from nose.tools import assert_raises

class TestLetterMatrix():

  def test_validate_row_length(self):
    cases = [
      (True, []),
      (True, [[]]),
      (True, [['']]),
      (True, [
        ['', '', ''],
        ['', '', ''],
        ['', '', ''],
      ]),
      (False, [
        [''],
        []
      ]),
      (False, [
        [''],
        [''],
        ['', '']
      ]),
    ]
    for (passes, matrix) in cases:
      yield self.letter_matrix_validation, matrix, passes

  def test_validate_contents(self):
    cases = [
      (True, []),
      (True, [['A', 'a']]),
      (True, [
        ['A', 'a'],
        ['', ''],
        ['B', 'Z']
      ]),
      (False, [[' ']]),
      (False, [['9']]),
      (False, [['.']]),
      (False, [['ABC']]),
      (False, ['ABC']),
    ]
    for (passes, matrix) in cases:
      yield self.letter_matrix_validation, matrix, passes

  def letter_matrix_validation(self, matrix, passes):
    if passes:
      assert LetterMatrix.validate(matrix)
    else:
      assert_raises(InvalidLetterMatrixException, LetterMatrix.validate, matrix)
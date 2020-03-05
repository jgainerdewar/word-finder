from wordfinder import LetterMatrix, InvalidLetterMatrixException
from nose.tools import assert_raises, assert_equal

class TestLetterMatrix():

  fixture = LetterMatrix([
    ['' , 'A', 'B', 'C', 'D'],
    ['E', 'F', '' , 'G', '' ],
    ['H', 'I', 'J', 'K', 'L'],
    ['' , '' , '' , '' , '' ],
    ['M', '' , 'N', '' , 'O'],
    ['P', 'Q', 'R', 'S', 'T'],
  ])

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

  def test_element(self):
    assert_equal(self.fixture.element(1, 2), '')
    assert_equal(self.fixture.element(1, 3), 'G')
    assert_equal(self.fixture.element(5, 0), 'P')
    assert_raises(IndexError, self.fixture.element, 6, 0)
    assert_raises(IndexError, self.fixture.element, 0, 5)

  def test_exists(self):
    assert self.fixture.exists(0, 0)
    assert self.fixture.exists(5, 4)
    assert not self.fixture.exists(6, 4)
    assert not self.fixture.exists(5, 5)
    assert not self.fixture.exists(-1, 0)
    assert not self.fixture.exists(0, -1)

  def test_neighbors(self):
    assert_equal(
      self.fixture.neighbors(0, 0),
      [(0, 1), (1, 0), (1, 1)]
    )
    assert_equal(
      self.fixture.neighbors(2, 1),
      [(1, 0), (1, 1), (2, 0), (2, 2)]
    )

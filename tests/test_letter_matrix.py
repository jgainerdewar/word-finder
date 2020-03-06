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

  def test_rec_find_words_no_prefix(self):
    # If no words of the given length can be made, the empty list 
    # is returned
    assert_equal(
      sorted(list(self.fixture._rec_find_words(100, 4, 0, {(4, 0)}, ""))),
      []
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(0, 4, 0, {(4, 0)}, ""))),
      []
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(-6, 4, 0, {(4, 0)}, ""))),
      []
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(1, 4, 0, {(4, 0)}, ""))),
      ["M"]
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(2, 4, 0, {(4, 0)}, ""))),
      ["MP", "MQ"]
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(3, 4, 0, {(4, 0)}, ""))),
      ["MPQ", "MQN", "MQP", "MQR"]
    )

  def test_rec_find_words_with_prefix(self):
    assert_equal(
      sorted(list(self.fixture._rec_find_words(1, 4, 0, {(4, 0)}, "MP"))),
      []
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(1, 4, 0, {(4, 0)}, "K"))),
      []
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(1, 4, 0, {(4, 0)}, "M"))),
      ["M"]
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(3, 4, 0, {(4, 0)}, "MQ"))),
      ["MQN", "MQP", "MQR"]
    )
    assert_equal(
      sorted(list(self.fixture._rec_find_words(3, 4, 0, {(4, 0)}, "MQR"))),
      ["MQR"]
    )

  def test_find_words_no_prefix(self):
    small_matrix = LetterMatrix([
      ['A', 'B'],
      ['' , 'C']
    ])
    assert_equal(small_matrix.find_words(0), [])
    assert_equal(small_matrix.find_words(1), ['A', 'B', 'C'])
    assert_equal(
      small_matrix.find_words(2), 
      ['AB', 'AC', 'BA', 'BC', 'CA', 'CB']
    )
    assert_equal(
      small_matrix.find_words(3), 
      ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
    )
    assert_equal(small_matrix.find_words(4), [])

  def test_find_words_with_prefix(self):
    row_matrix = LetterMatrix([
      ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'A', 'I', 'J']
    ])

    assert_equal(row_matrix.find_words(1, 'Z'), [])
    assert_equal(row_matrix.find_words(1, 'AB'), [])
    assert_equal(row_matrix.find_words(1, 'B'), ['B'])
    assert_equal(row_matrix.find_words(2, 'C'), ['CB', 'CD'])
    assert_equal(row_matrix.find_words(3, 'A'), ['ABC', 'AHG', 'AIJ'])
    assert_equal(row_matrix.find_words(3, 'AI'), ['AIJ'])

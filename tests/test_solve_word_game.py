from nose.tools import assert_equal
import wordfinder
from wordfinder import LetterMatrix

class TestSolveWordGame:

  def test_empty(self):
    matrix = LetterMatrix([[]])
    solutions = wordfinder.solve_word_game(matrix, [5], None)
    assert_equal([], solutions)

  def test_single(self):
    matrix = LetterMatrix([['A','B','C']])
    solutions = sorted(wordfinder.solve_word_game(matrix, [3], None))
    assert_equal([['ABC'], ['CBA']], solutions)

  def test_two_by_two(self):
    matrix = LetterMatrix([['A','B'],['C', 'D']])
    assert_equal(
      [
        ['AB', 'CD'],
        ['AB', 'DC'],
        ['AC', 'BD'],
        ['AC', 'DB'],
        ['AD', 'BC'],
        ['AD', 'CB'],
        ['BA', 'CD'],
        ['BA', 'DC'],
        ['BC', 'AD'],
        ['BC', 'DA'],
        ['BD', 'AC'],
        ['BD', 'CA'],
        ['CA', 'BD'],
        ['CA', 'DB'],
        ['CB', 'AD'],
        ['CB', 'DA'],
        ['CD', 'AB'],
        ['CD', 'BA'],
        ['DA', 'BC'],
        ['DA', 'CB'],
        ['DB', 'AC'],
        ['DB', 'CA'],
        ['DC', 'AB'],
        ['DC', 'BA'],
      ], 
      sorted(wordfinder.solve_word_game(matrix, [2, 2], None))
    )

    assert_equal(
      [
        ['A', 'BC'],
        ['A', 'BD'],
        ['A', 'CB'],
        ['A', 'CD'],
        ['A', 'DB'],
        ['A', 'DC'],
        ['B', 'AC'],
        ['B', 'AD'],
        ['B', 'CA'],
        ['B', 'CD'],
        ['B', 'DA'],
        ['B', 'DC'],
        ['C', 'AB'],
        ['C', 'AD'],
        ['C', 'BA'],
        ['C', 'BD'],
        ['C', 'DA'],
        ['C', 'DB'],
        ['D', 'AB'],
        ['D', 'AC'],
        ['D', 'BA'],
        ['D', 'BC'],
        ['D', 'CA'],
        ['D', 'CB'],
      ], 
      sorted(wordfinder.solve_word_game(matrix, [1, 2], None))
    )
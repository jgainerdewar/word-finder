import copy

def solve_word_game(matrix, word_lengths, dictionary):
  solutions = []
  # Get all possible solutions for the first word
  subsolns = matrix.find_word_coords(word_lengths[0], dictionary=dictionary)
  for s in subsolns:
    word = matrix.word_at(s)
    remaining_word_lengths = word_lengths[1:]

    if not remaining_word_lengths:
      # We found all the words!
      solutions += [[word]]
    else:
      # There are more words to find, look for the next one
      reduced_matrix = copy.deepcopy(matrix)
      reduced_matrix.remove_word(s)
      remaining_solutions = solve_word_game(
        reduced_matrix, 
        remaining_word_lengths,
        dictionary
      )
      solutions += [[word] + r  for r in remaining_solutions]

  return solutions

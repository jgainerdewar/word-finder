import os

class Dictionary:
  """
  Represents a set of known words to compare solutions against.
  """

  # If not using a custom dictionary path, attempt to use these
  # files in this order.
  CANDIDATES = [
    "/usr/share/dict/words",
    "/usr/dict/words",
    os.path.join(
      os.path.abspath(os.path.dirname(__file__)),
      "../dictionaries/scrabble_2019.txt"
    )
  ]

  def __init__(self, file_path=""):
    words_on_disk = file_path
    if not words_on_disk:
      for c in Dictionary.CANDIDATES:
        if os.path.exists(c):
          words_on_disk = c
          break

    with open(words_on_disk) as f:
      self.dictionary_words = { w.upper() for w in f.read().splitlines()}

  def contains(self, word):
    return word.upper() in self.dictionary_words

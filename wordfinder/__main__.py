import csv
import sys
from argparse import ArgumentParser
from wordfinder import LetterMatrix, Dictionary

def construct_matrix(input_csv):
  letter_array = []
  try:
    with open(input_csv) as csv_file:
      reader = csv.reader(csv_file)
      for row in reader:
        letter_array.append(row)
    return LetterMatrix(letter_array)
  except Exception as e:
    print("Encountered error when constructing matrix: {}".format(e))
    sys.exit(1)

def main(args=None):
  if args is None:
    args = sys.argv[1:]

  parser = ArgumentParser("wordfinder", 
                          description="Find a word of a specified length " +
                          "in a 2D array of letters")
  parser.add_argument("input_csv", type=str,
                      help="Path to a CSV file containing letter matrix. " +
                      "Each element in CSV must either be empty, or contain " +
                      "a single letter A-Z or a-z. All rows must be the " +
                      "same length.")
  parser.add_argument("word_length", type=int,
                      help="The length of the word to find.")
  parser.add_argument("--prefix", "-p", type=str, default="", 
                      help="If provided, only words with this prefix " +
                      "will be returned. Can be any length up to word length.")
  parser.add_argument("--raw_results", dest="use_dict", action="store_false",
                      help="By default we return only words that appear in " +
                      "the configured dictionary. Use this option to return " +
                      "every possible solution instead.")
  parser.add_argument("--dictionary_path", type=str, default="",
                     help="Use this option to define a custom dictionary to " +
                     "pull solutions from. If not set, we attempt to use " +
                     "the system dictionary, and fall back to the 2019 " +
                     "Scrabble dictionary, which is packaged with this module.")

  parsed_args = parser.parse_args(args)

  dictionary = None
  if parsed_args.use_dict:
    dictionary = Dictionary(parsed_args.dictionary_path)

  matrix = construct_matrix(parsed_args.input_csv)
  words = matrix.find_words(
    parsed_args.word_length, 
    parsed_args.prefix, 
    dictionary
  )

  if not words:
    print("No results")
  for word in words:
    print(word.upper())

    
if __name__ == "__main__":
  main()
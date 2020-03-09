import sys
from argparse import ArgumentParser

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

  parsed_args = parser.parse_args(args)
    
if __name__ == "__main__":
  main()
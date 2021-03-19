import argparse
from tournament_score import get_score

parser = argparse.ArgumentParser(description='Count bowling score')
parser.add_argument('input_file', type=str, help='файл протокола турнира')
parser.add_argument('output_file', type=str, help='файл результатов турнира')
parser.add_argument('rules', type=str, help='Введите "old", если хотите играть по старым правилам '
                                            'или "new" - если по новым')

if __name__ == '__main__':
    args = parser.parse_args('tournament.txt tournament_result.txt new'.split())
    print(get_score(args.input_file, args.output_file, args.rules))

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', nargs='?',
                    type=argparse.FileType('r', encoding="utf-8"),
                    default=open('input.txt', 'r', encoding="utf-8"),
                    help='Input file')
parser.add_argument('--model', nargs='?',
                    type=argparse.FileType('w', encoding="utf-8"),
                    default=sys.stdout,
                    help='Output file')
parser.add_argument('--lc', nargs='?', const=True, default=False,
                    help='To lowercase')


args = parser.parse_args()

ins = vars(args).get('input_dir')
outs = vars(args).get('model')
lc = vars(args).get('lc')

# import argparse
#
# parser = argparse.ArgumentParser(
#     prog= 'Parser Trainer',
#     description= 'This is a simple test program that will help me to understand and train ARGPARSER possibilities',
#     epilog='Some text that should be printed at the end of the help file'
# )
#
# parser.add_argument()


import argparse


parser = argparse.ArgumentParser(
    prog='PROG',
    usage='%(prog)s [options]')
parser.add_argument('--foo', nargs='?', help='foo help')
parser.add_argument('bar', nargs='+', help='bar help message')
parser.print_help()
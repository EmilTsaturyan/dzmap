import argparse


parser = argparse.ArgumentParser(
                prog='dzmap.py',
                description='Scanning ports')
parser.add_argument('ip')
parser.add_argument('-r', '--range', default='1-1023')   
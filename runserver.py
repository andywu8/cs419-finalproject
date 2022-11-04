#! /usr/bin/env python
from sys import exit, stderr
from regapp import app
import argparse

def main():
    parser = argparse.ArgumentParser(
                    description = 'The registrar application',
                    add_help=True)

    parser.add_argument('port', help='the port at which the server should listen', type=int)
    results = parser.parse_args()
    port = results.port

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
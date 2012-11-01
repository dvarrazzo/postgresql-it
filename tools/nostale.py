#!/usr/bin/env python
"""Remove the stale translations from a messages catalog.

Also remove the blank lines before the deleted entry.
"""

import sys

def main():
    line = None
    it = iter(sys.stdin)

    try:
        while 1:

            buf = []
            # start from the whiteline found at the previous round
            if line is not None:
                buf.append(line)

            # step 1: read the blanks
            while 1:
                line = it.next()
                buf.append(line)
                if not line.isspace():
                    break

            # step 2: read the non-blanks:
            while 1:
                line = it.next()
                if line.isspace():
                    break

                buf.append(line)

            if not isstale(buf):
                sys.stdout.write(''.join(buf))

    except StopIteration:
        # last group of lines
        if not isstale(buf):
            sys.stdout.write(''.join(buf))

def isstale(lines):
    for line in lines:
        if line.startswith('msgid'):
            return False
        elif line.startswith('#~ msgid'):
            return True

    return False    # not a translation

if __name__ == '__main__':
    sys.exit(main())


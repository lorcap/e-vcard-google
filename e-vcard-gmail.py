#!/usr/bin/env python3

import argparse
import base64
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--dry-run", help="do not download anything", action="store_true")
parser.add_argument("-p", "--with-photo", help="filter out contacts without photo", action="store_true")
parser.add_argument("filein", help="input vCard file")
parser.add_argument("fileout", help="output vCard file")
args = parser.parse_args()

with open(args.filein, 'r') as fin,\
     open(args.fileout, 'w') as fout:

    last_line = fin.readline()
    while True:
        if not last_line:
            break

        lines = [last_line, ]
        last_line = fin.readline()
        while last_line.startswith(' '):
            lines.append(last_line)
            last_line = fin.readline()
        line = ''.join(l.strip() for l in lines)

        field, value = line.split(':', 1)
        filed, *prop = field.split(';', 1)

        if field == 'BEGIN' and value == 'VCARD':
            FN = ''
            PHOTO = ''
            vcard = []

        elif field == 'FN':
            FN = value

        elif field == 'PHOTO':
            PHOTO = value
            if not args.dry_run:
                with urllib.request.urlopen(PHOTO) as photo:
                    photo64 = base64.b64encode(photo.read())
                lines = ["PHOTO;TYPE=jpeg;ENCODING=b;VALUE=BINARY:\n", ]
                for i in range(0, len(photo64), 74):
                    lines.append(' ' + photo64[i:i+74].decode('ascii') + '\n')
                del photo64

        vcard.extend(lines)

        if field == 'END' and value == 'VCARD':
            if args.with_photo == False or PHOTO:
                with_photo = f" with photo:\n {PHOTO}" if PHOTO else ""
                print(f'Found {FN}{with_photo}')
                for line in vcard:
                    fout.write(line)

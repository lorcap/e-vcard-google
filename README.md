# e-vcard-gmail

This simple Python script allows you to import
[Google Contacts](https://contacts.google.com/) into your
[/e/ cloud](https://ecloud.global/apps/contacts/) account while preserving
contact photos.


## How to migrate your Google Contacts

1. Go to your [Google Contacts](https://contacts.google.com/).
2. Export your contacts as *vCard (for iOS Contacts)* into `contacts.vcf`.
3. Run this script as `e-vcard-gmail.py contacts.vcf contacts-e.vcf`.
4. Go to your [/e/ cloud](https://ecloud.global/apps/contacts/) and import
   `contacts-e.vcf`.


## How to update your /e/ contacts

If you already migrated your contacts, you can convert only those contacts
that have a photo on Google Contacts. Use option `--with-photo`. After
importing, contacts have to be merged manually.

## Usage
```
usage: e-vcard-gmail.py [-h] [-n] [-p] filein fileout

positional arguments:
  filein            input vCard file
  fileout           output vCard file

optional arguments:
  -h, --help        show this help message and exit
  -n, --dry-run     do not download anything
  -p, --with-photo  filter out contacts without photo
```


## Technical details

Google vCards provides contact photos as URLs which can be downloaded
without any account login.  On the other hand, /e/ accepts photos encoded
with Base64.

For each vCard, this script downloads the photo, encodes it, and writes
it to the output file, properly handling long lines (which start with a
blank).

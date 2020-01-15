# Holiday Hack 2019 - Objective 10 - Document Decryption

### Intro
This code forms part of my solution to the 2019 SANS Holiday Hack. See the main video for details: (http://www.youtube.com/watch?v=_n-fCrh3Nb0)

## Contents
* brute_force.py - generate all possible (insecure!) crypto keys for the elfscrow.exe software and attempt to decrypt the first 8 bytes of the target document.

```
./brute_force.py
```

Parse via grep to identify which key successfully decrypts the target document as a PDF:

```
./brute_force.py | grep "25504446"
```

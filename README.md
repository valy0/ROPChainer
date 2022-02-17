# ROPChainer
ROPChainer is a simple python script to parse rp gadget output files using regex for quick gadget filtering.

Default usage:
`python3 ROPChainer.py -f rp_output.txt`

<br>

```text
usage: ROPChainer.py [-h] -f FILE [-t TYPE] [-b BAD] [-F]

Script to quickly parse rp output files to easily find gadgets

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Filename of the rp output file to parse.
  -t TYPE, --type TYPE  Type to search for, default=ALL (ADD SUB MOV SET XOR XCHG POP PUSH PPR DEREF INC DECR)
  -b BAD, --bad BAD     Bad characters to filter out (format: '00 0a 0n 26')
  -F, --full            Display gadgets with more instructions.
```
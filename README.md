# ARM Roper [![Build Status](https://travis-ci.org/0xbadarg/armroper.svg?branch=master)](https://travis-ci.org/0xbadarg/armroper)

Tool for searching the rop gadgets for ARM. Basically, refactorisation of the MyROP project, with further plans for features like converting to python string, blah blah. 


## Installation

For deps just run: sudo pip install -r requirements.txt
Also you will need a capstone libs installed.
After that you can try roper with: ./armroper.py -h

## Usage
```
spx@galactica ~/c/armroper> ./armroper.py -h
usage: armroper.py [-h] [-f FILENAME] [-d DEPTH] [-m]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
  -d DEPTH, --depth DEPTH
  -m, --mode
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :)

## Credits

All the credits goes to the MyRop, and  Jonathan Salwan from the shell-storm.org

## License

Check the LICENCE file.

# Installation
## Prerequisites
You need:

 * a version of python (I have 2.6.2, versions close to that should work)
 * mpmath (optional, but 10x faster than python's built in decimal module)
          http://code.google.com/p/mpmath/, 
          packaged as python-mpmath in debian based distros
          (bundled with sympy in fedora?)

## Installing

Run `sudo python setup.py install` or `python setup.py install --user`. The later option
installs without sudo into your user Python directories. If you use it, make sure that
`$HOME/.local/bin` is in your `$PATH`.


# First run

Run `bbchop`. Please refer to the `README` in the root of this repository.



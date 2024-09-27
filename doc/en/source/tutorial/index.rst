.. 2dmat documentation master file, created by
   sphinx-quickstart on Tue May 26 18:44:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorials
================================

``odatse-SXRD`` provides a direct problem solver for ODAT-SE that uses ``sxrdcalc`` to calculate the Rocking curve by giving atomic positions :math:`x` , atomic occupancies, and Debye-Waller factor, and returnes the deviation :math:`f(x)`  from the experimental Rocking curve.

In this tutorial, we will instruct how to perform analyses of SXRD data using Nelder-Mead method.
Hereinafter, we use ``odatse-SXRD`` program included in odatse-SXRD with input files in TOML format.
Next, we will explain how to write your own main program for analyses.


.. toctree::
   :maxdepth: 1

   minsearch
   user_program

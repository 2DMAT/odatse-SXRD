Installation of odatse-SXRD
================================================================

Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Python3 (>=3.6.8)

  - The following Python packages are required.

    - tomli >= 1.2
    - numpy >= 1.14

  - ODAT-SE version 3.0 and later

  - sxrdcalc

    - C compiler and GNU Scientific Library are required.


How to download and install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install ODAT-SE

   - From source files:

     Download source files of ODAT-SE from the repository as follows:

     .. code-block:: bash

	$ git clone https://github.com/issp-center-dev/ODAT-SE.git

     Install ODAT-SE using ``pip`` command:

     .. code-block:: bash

	$ cd ODAT-SE
	$ python3 -m pip install .

     You may add ``--user`` option to install ODAT-SE locally (in ``$HOME/.local``).

     If you run the following command instead, optional packages will also be installed at the same time.

     .. code-block:: bash

	$ python3 -m pip install .[all]

2. Install sxrdcalc

   - sxrdcalc is available from the official site at: `https://github.com/sxrdcalc/sxrdcalc <https://github.com/sxrdcalc/sxrdcalc>`_

     The source package can be downloaded from the web site by pressing "Code" button and choosing "Download ZIP", or by the following command.

     .. code-block:: bash

	$ wget -O sxrdcalc.zip https://github.com/sxrdcalc/sxrdcalc/archive/refs/heads/main.zip

   - Unpack the source package, and compile the source. Edit Makefile in sxrdcalc-main as needed. GNU Scientific Library is required for the compilation.

     .. code-block:: bash

	$ unzip sxrdcalc.zip
	$ cd sxrdcalc-main
	$ make

     The executable file ``sxrdcalc`` will be generated.
     Put ``sxrdcalc`` in a directory listed in the PATH environment variable, or specify the paths to these commands at run time.
     
3. Install odatse-SXRD

   - From source files:

     The source files of odatse-SXRD are available from the GitHub repository. After obtaining the source files, install odatse-SXRD using ``pip`` command as follows:

     .. code-block:: bash

	$ git clone https://github.com/2DMAT/odatse-SXRD.git
	$ cd odatse-SXRD
	$ python3 -m pip install .

     You may add ``--user`` option to install the package locally (in ``$HOME/.local``).

     Then, the library of odatse-SXRD and the command ``odatse-SXRD`` wil be installed.


How to run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In ODAT-SE, the analysis is done by using a predefined optimization algorithm and a direct problem solver.
There are two ways to do analyses of SXRD:

1. Use odatse-SXRD program included in this package to perform analyses.
   The users prepare an input parameter file in TOML format, and run command with it.
   The type of the inverse problem algorithms can be chosen by the parameter.

2. Write a program for the analysis with odatse-SXRD library and ODAT-SE framework.
   The type of the inverse problem algorithms can be chosen by importing the appropriate module.
   A flexible use would be possible, for example, to include data generation within the program.
   
The types of parameters and the instruction to use the library will be given in the subsequent sections.


How to uninstall
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to uninstall odatse-SXRD and ODAT-SE modules, type the following commands:

.. code-block:: bash

   $ python3 -m pip uninstall odatse-SXRD ODAT-SE

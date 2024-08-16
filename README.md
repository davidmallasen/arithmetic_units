<!--
SPDX-FileCopyrightText: 2024 David Mallasén Quintana
SPDX-License-Identifier: LGPL-3.0-or-later
Source: https://github.com/davidmallasen/arithmetic_units
-->

# Arithmetic Units
Collection of arithmetic units written in SystemVerilog.

## Setup
Tested in Ubuntu 22.04.

1. Set up the python environment using one of (a) Miniconda OR (b) pip:
    - (a) Miniconda
        1. Install [Miniconda](https://docs.anaconda.com/miniconda/).
        2. Create the environment (only the first time):

            ~~~bash
            conda env create -f environment.yml
            ~~~

        3. Activate the environment (every time you open a new terminal):

            ~~~bash
            conda activate arithmetic_units
            ~~~

    - (b) pip
        1. Check that you have the python and pip versions that are required for this project. You can find them in the `environment.yml` file. If you are unsure about this, follow the instructions for Miniconda.

        2. Create the environment (only the first time):

            ~~~bash
            python -m venv venv
            source venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
            ~~~

        3. Activate the environment (every time you open a new terminal):

            ~~~bash
            source venv/bin/activate
            ~~~

2. Install the [Icarus Verilog](https://steveicarus.github.io/iverilog/) simulator. We
currently use version 11.0. In Ubuntu, you can do this with:

    ~~~bash
    sudo apt install iverilog
    ~~~

3. Install [Verible](https://chipsalliance.github.io/verible) for SystemVerilog linting
and formatting. We currently use version `v0.0-3752-g8b64887e`. In Ubuntu, you can do
this with:

    ~~~bash
    export VERIBLE_VERSION=v0.0-3752-g8b64887e
    wget https:wget https://github.com/chipsalliance/verible/releases/download/${VERIBLE_VERSION}/verible-${VERIBLE_VERSION}-linux-static-x86_64.tar.gz
    tar -xf verible-${VERIBLE_VERSION}-linux-static-x86_64.tar.gz
    ~~~

    Then you can install it to your preferred location. For example, to install it in
    `/home/$USER/tools`, run:

    ~~~bash
    mkdir -p /home/$USER/tools/verible/${VERIBLE_VERSION}/
    mv verible-${VERIBLE_VERSION}/* /home/$USER/tools/verible/${VERIBLE_VERSION}/
    ~~~

    You can remove the previous download from the current path with:

    ~~~bash
    rm -rf verible-${VERIBLE_VERSION}*
    ~~~

    Finally, add the `/home/$USER/tools/verible/${VERIBLE_VERSION}/bin` to your `PATH`
    environment variable.

## Running the Tests
The test setup is based on [cocotb](https://www.cocotb.org/) and [pytest](https://docs.pytest.org/en/stable/). You can find all the tests in the `test` folder.

To run the tests, run:

~~~bash
pytest
~~~

If you want the detailed output, run:

~~~bash
pytest -rA -v
~~~

## Running SystemVerilog Formatting and Linting
When developing RTL code for this project, you should run Verible to check that it's
formatted correctly and that it follows the best practices. To run the Verible formatter
run:

~~~bash
make verible-format
~~~

## Bibliography
[1] J.-M. Muller et al., Handbook of Floating-Point Arithmetic. Cham: Springer International Publishing, 2018. doi: 10.1007/978-3-319-76526-6.

## License

This project is licensed under the [CERN Open Hardware Licence Version 2 - Weakly Reciprocal](https://cern.ch/cern-ohl)
or later, unless specified otherwise. The license is also included in this repository in
the `LICENSES` directory. SPDX-License-Identifier: CERN-OHL-W-2.0+

The software (i.e. all code inside the `test` directory) is licensed under the
[GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html)
or later, unless specified otherwise. The license is also included in this repository in
the `LICENSES` directory. SPDX-License-Identifier: LGPL-3.0-or-later

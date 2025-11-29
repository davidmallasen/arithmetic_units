# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

# Run all tests
.PHONY: test
test:
	pytest

# Run verible formatting of SystemVerilog files
.PHONY: sv-format
sv-format:
	find -name '*.sv*' | xargs python util/verible-format.py --inplace --files 2> /dev/zero

# Run verible linting of SystemVerilog files
.PHONY: sv-lint
sv-lint:
	find -name '*.sv*' | xargs verible-verilog-lint

# Run black formatting of python files
.PHONY: python-format
python-format:
	python -m black test/

# Run formatting for all files
.PHONY: format
format: sv-format python-format

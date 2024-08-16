# SPDX-FileCopyrightText: 2024 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

# Run verible formatting of hw files
.PHONY: verible-format
verible-format:
	find -name '*.sv*' | xargs python util/verible-format.py --inplace --files 2> /dev/zero

# SPDX-FileCopyrightText: 2025 David Mallasén Quintana
# SPDX-License-Identifier: LGPL-3.0-or-later
# Source: https://github.com/davidmallasen/arithmetic_units

import os

from fusesoc.config import Config
from fusesoc.coremanager import CoreManager
from fusesoc.librarymanager import Library
from fusesoc.vlnv import Vlnv


def get_core_files(proj_path, core_name):
    """
    Parses .core files to get the source list and include directories.

    Args:
        proj_path (Path): Path to the project directory.
        core_name (str): VLNV name of the core.
    Returns:
        A list of source files and a list of include directories.
    """
    config = Config()
    cm = CoreManager(config)

    lib = Library("lib", str(proj_path))
    cm.add_library(lib, [])

    try:
        top_vlnv = Vlnv(core_name)
    except ValueError:
        raise ValueError(f"Invalid VLNV: {core_name}")

    flags = {
        "tool": "icarus", 
        "target": "default", 
        "is_toplevel": True 
    }

    resolved_cores = cm.get_depends(top_vlnv, flags)
    top_core = cm.get_core(top_vlnv)
    resolved_cores.append(top_core)

    src_files = []
    inc_dirs = []

    for core in resolved_cores:
        try:
            core_file_list = core.get_files(flags)
        except SyntaxError:
            print(f"Warning: Target 'default' not found for {core.name}. Skipping.")
            continue
        except RuntimeError:
            continue

        for file_data in core_file_list:
            rel_path = file_data.get("name")
            if not rel_path:
                continue

            abs_path = os.path.join(core.core_root, rel_path)
            
            if file_data.get("is_include_file"):
                inc_dir = os.path.dirname(abs_path)
                if inc_dir not in inc_dirs:
                    inc_dirs.append(inc_dir)
            else:
                if abs_path not in src_files:
                    src_files.append(abs_path)

    return src_files, inc_dirs

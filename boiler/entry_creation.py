import subprocess as _subprocess
from pathlib import Path as _Path
from typing import (
    TypeAlias as _TypeAlias,
    Any as _Any
)
# FIXME: type this properly
_File: _TypeAlias = dict[str, str]
_Folder: _TypeAlias = dict[str, "_Folder"]


def create_files_from(
    entries: dict[str, _Any],
    /,
    *,
    _traversed: _Path | None = None
):
    traversed = _traversed or _Path.cwd() # start at current working directory
    for entry, structure in entries.items():
        # NOTE: (just don't have folders with dots)
        path = traversed.joinpath(entry)
        if "." not in entry: # is folder
            make_folder(path, metadata=structure)
            # recursivly add the rest
            create_files_from(structure, _traversed=path)
            continue
        make_file(path, metadata=structure)


def make_file(
    path: _Path,
    /,
    *,
    metadata: dict[str, str]
) -> None:
    # make file
    print("FILE:", path)
    path.touch(exist_ok=False)
    if "content" in metadata:
        path.write_text(metadata["content"], encoding="utf-8")
    if "source" in metadata: # if paired with 'content', 'content' is places at top
        source = metadata["source"]
        if source == "command":
            command = metadata["command"]
            process = _subprocess.run(
                command,
                capture_output=True,
                shell=True,
                text=True
            )
            print("COMMAND:", command)
            print("RETURNCODE:", process.returncode)
            if process.returncode == 0:
                path.write_text(process.stdout, encoding="utf-8")
                return
            # error("Return code", process.returncode)


def make_folder(
    path: _Path,
    /,
    *,
    metadata: dict[str, str] # TODO: remove
) -> None:
    # make folder
    print("FOLD:", path)
    path.mkdir(exist_ok=False)

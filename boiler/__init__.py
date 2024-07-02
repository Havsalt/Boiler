"""
Boiler
-------

Creates project boilerplate from templates
"""

__version__ = "0.1.0"

import argparse
import pathlib

import tomli

from .pre_process import collect_argument_keys, expand_arguments
from .entry_creation import create_files_from


class ParserArguments(argparse.Namespace):
    # silent: bool
    # verbose: bool
    template: str
    variant: str


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="templar",
        description="Template maker for your fresh projects",
        add_help=False
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit",
        default=argparse.SUPPRESS
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s: v{__version__}",
        help="Show `%(prog)s` version number and exit"
    )
    # print_group = parser.add_mutually_exclusive_group()
    # print_group.add_argument(
    #     "--verbose",
    #     action="store_true",
    #     help="Display more info during execution"
    # )
    # print_group.add_argument(
    #     "--silent",
    #     action="store_true",
    #     help="Display less info during execution"
    # )
    template_paths = (
        pathlib.Path(__file__)
        .parent
        .joinpath("templates")
        .iterdir()
    )
    template_subparsers = parser.add_subparsers(
        # title="template",
        required=True,
        dest="template",
        help="Template to create"
    )
    # a_sub = template_subparsers.add_parser("a")
    # a_sub.add_argument("slot")
    # a_sub.add_argument("--arg", required=True)
    # b_sub = template_subparsers.add_parser("b")

    template_names: list[str] = []
    for template in template_paths:
        template_name = template.stem
        template_names.append(template_name)

        template_parser = template_subparsers.add_parser(template_name)

        raw_template_content = template.read_text(encoding="utf-8")
        for key in collect_argument_keys(raw_template_content):
            template_parser.add_argument(
                # f"-{key[0]}", f"--{key}",
                # required=True,
                key,
                help="Field value"
            )

    args = ParserArguments()
    parser.parse_args(namespace=args)

    selected_template = (
        pathlib.Path(__file__)
        .parent
        .joinpath("templates", args.template)
        .with_suffix(".toml")
    )
    assert selected_template.exists(), str(selected_template) + " does not exist"


    raw_content = selected_template.read_text(encoding="utf-8")
    
    argument_keys = collect_argument_keys(raw_content)
    argument_mapping = {
        key: getattr(args, key)
        for key in argument_keys
    }
    expanded = expand_arguments(raw_content, mapping=argument_mapping)
    print(expanded)
    data = tomli.loads(expanded)
    import rich
    rich.print(data)

    if "create" in data:
        create_files_from(data["create"])

    return 0

import re as _re
from typing import TYPE_CHECKING as _TYPE_CHECKING

if _TYPE_CHECKING:
    from .__init__ import ParserArguments as _ParserArguments


_ARGUMENT_CAPTURE_PATTERN = _re.compile(
    r"\$\[([A-Z]+)\]",
    flags=_re.RegexFlag.ASCII
)

# TODO: implement ENVIRONMENT vars and RUNTIME vars, like $[NAME] and %[YEAR]
# _ENV_VAR_CAPTURE_PATTERN = _re.compile(
#     r"\%\[([A-Z]+)\]",
#     flags=_re.RegexFlag.ASCII
# )


def collect_argument_keys(content: str) -> list[str]:
    results: list[str] = []
    for match in _ARGUMENT_CAPTURE_PATTERN.finditer(content):
        if not (keyword := match.group(1).lower()) in results:
            results.append(keyword)
    return results


def expand_arguments(
    content: str,
    /,
    *,
    mapping: dict[str, str]
) -> str:
    return _ARGUMENT_CAPTURE_PATTERN.sub(
        lambda match: (
            mapping.get(match.group(1).lower(), match.group(0))
        ),
        content
    )

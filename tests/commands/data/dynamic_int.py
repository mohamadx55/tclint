from tclint.commands.checks import CommandArgError, check_arg_spec

OPEN_BLOCK_SPEC = {
    "positionals": [
        {"name": "block_name", "required": True, "value": {"type": "any"}},
    ],
    "switches": {
        "-check": {
            "required": False,
            "repeated": False,
            "value": {"type": "any"},
        },
    },
}


def _open_block(args, parser):
    for index, arg in enumerate(args):
        if arg.contents != "-check":
            continue

        if index == len(args) - 1:
            raise CommandArgError(
                "invalid arguments for open_block: expected int value after -check"
            )

        value = args[index + 1].contents
        if value is None:
            continue

        try:
            int(value, 0)
        except ValueError as error:
            raise CommandArgError(
                f"invalid value for open_block -check: got {value}, expected int"
            ) from error

    return check_arg_spec("open_block", args, parser, OPEN_BLOCK_SPEC)


commands = {
    "open_block": _open_block,
}

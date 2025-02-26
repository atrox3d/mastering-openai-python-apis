#
#   TODO: find a way to run commands with params or globals
#
COMMANDS = {
    '/history': {'fn': None, 'args':['history']}
}


def command(prompt:str, commands:dict=COMMANDS, **kwargs):
    # if prompt.startswith('/') and any(prompt.startswith(cmd) for cmd in commands.keys()):
    for cmd in commands.keys():
        if prompt.startswith(cmd):
            # TODO: process command
            cmd, *rest = cmd.split()
            print(f'command!', cmd, rest)
            return True
    return False
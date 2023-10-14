"""This module is used to parse the arguments passed to the program."""

def parse_args(args):
    """Returns a dictionary with the arguments passed to the program."""
    toret = {}
    for arg in args:
        arg_split = arg.split('=')
        name = arg_split[0].replace('--', '')

        if len(arg_split) == 2:
            toret[name] = arg_split[1]
        else:
            toret[name] = True

        if toret[name] == '' or toret[name] is True:
            toret[name] = 'error'


    return toret


if __name__ == '__main__':
    print(parse_args(['--test=a']))
    print(parse_args(['--test=a', '--test2=b']))
    print(parse_args(['--test=a', '--test2=b', '--testFlag']))
    a = ['--test1=', '--test2=a', '--test3=b', '--testFlag']
    b = parse_args(a)
    if b['test1'] == 'error':
        print('[ERROR]')

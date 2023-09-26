

def parseArgs(args):
    toret = {}
    for arg in args:
        argSplit = arg.split('=')
        name = argSplit[0].replace('--', '')

        if len(argSplit) == 2:
            toret[name] = argSplit[1]
        else:
            toret[name] = True
        # Si se pasa un argumento mal escrito, da error
        if toret[name] == '' or toret[name] == True:
            toret[name] = 'error'
            
        
    return toret


if __name__ == '__main__':
    print(parseArgs(['--test=a']))
    print(parseArgs(['--test=a', '--test2=b']))
    print(parseArgs(['--test=a', '--test2=b', '--testFlag']))
    a = ['--test1=', '--test2=a', '--test3=b', '--testFlag']
    b = parseArgs(a)
    if b['test1'] == 'error':
        print('[ERROR]')

def ChangeStupidRules(filename,passthrough):
    with open(filename, 'U') as f:

        newText = f.read()

        while '\n\n' in newText:
            newText = newText.replace('\n\n','\n')
        newText = passthrough(newText)
        
    with open(filename, 'w') as f:
        f.write(newText)

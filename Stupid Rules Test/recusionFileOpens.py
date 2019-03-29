import os, sys
import CallonFiles
import HelloWorld


def ManipulateTxtFiles(path):
    folder = os.listdir(path)
    for thing in folder:
        if(os.path.isdir(path + '\\' + thing)):
            ManipulateTxtFiles(path + '\\' + thing)
        else:
            filename,fileExtension = os.path.splitext(path + '\\' + thing)
            if( fileExtension == '.txt'):
                CallonFiles.ChangeStupidRules(filename+fileExtension, HelloWorld.stupidRulesTxt)
                print("Changing:" + filename+fileExtension)
            if(fileExtension == ".cs"):
                CallonFiles.ChangeStupidRules(filename+fileExtension, HelloWorld.stupidRulesCS)
            if(fileExtension == ".js"):
                CallonFiles.ChangeStupidRules(filename+fileExtension, HelloWorld.stupidRulesJS)

path = 'C:\\VSCode_Python_Env' # sys.argv[1]

ManipulateTxtFiles(path)


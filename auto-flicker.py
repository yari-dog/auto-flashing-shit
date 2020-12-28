import os
from os import path
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",type=int)
    parser.add_argument("-f","-fps",nargs="?",const="8",default="8")
    parser.add_argument("-c","-conc",nargs="?",const="1",default="1")
    parser.add_argument("-o",nargs="?",const="output",default="output")
    parser.add_argument("--t","--temp",nargs="?",const="temp",default="temp")
    parser.add_argument("--fo",action="store_true")
    args = parser.parse_args()
    return args.n, int(args.f), args.o, args.t, args.fo, int(args.c)

def getPaths(n):
    paths=[]
    for i in range(0,numberOfClips):
        output = ( "input path for file " + str(i+1)+": ")
        path = input(output)
        paths.append(path)
        if paths[i][-1] == " ":
            print("path has whitespace at the end, removing")
            paths[i] = paths[i][:-1]
    print("current path list is comprised of ",len(paths)," path(s): ",paths)
    return paths

def createDirectory(directory,forceOverwrite):
    if forceOverwrite:
        deleteDirectory(directory)
    if not (checkDirExists(directory)):   # You can swap this around to get rid of the 'not'.  
        print("creating directory ",directory)
        try:
            mkdirCommand = "mkdir " + str(directory)
            os.system(mkdirCommand)
            print("Directory Created!")
        except exception as e:
            print("Failed to create directory: ",e)
    else:
        overwrite = input("Error: directory already exists, are you sure you want to overwrite? y/n").lower()
        if overwrite == 'y':
            deleteDirectory(directory)
            createDirectory(directory)

def deleteDirectory(directory):
    if checkDirExists(directory):
        command = "rm -r " + directory
        print("removing ",directory," and all of its contents")
        rmCommand = os.system(command # linux specific? there's a couple ways to do this os-agnosticly, see https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
        print("rm completed with code ",rmCommand)
        if not(rmCommand == 0):
            print("crashing")
            quit()
    else:
        print("Directory does not exist, no need for overwrite")
    
                    
def movToMp4(paths,temp):
    # You can just do `for path in paths` in python:
    # if you need the number you can do enumerate()
    for i, path in enumerate(paths):
        print("checking paths",i)
        # Use this instead:
        filename, file_extension = os.path.splitext(path)
        if (file_extension == "mov"):
            print(path," requires converting...")
            outputFileString = temp + "/" + str(i) + ".mp4"
            commandString = "ffmpeg -i " + path + " -vcodec h264 -acodec mp2 " + outputFileString
            print("executing command: " + commandString)
            command = os.system(commandString)
            if ( command == 0):
                print("Converted file ",str(i)," successfully!")
                path=(temp+"/"+str(i)+".mp4")
                print("new file path is: ",path)
            else:
                print(command)
                quit()
        if not (file_extension == "mp4"): # Why check at the end? if you want it to stop the program, you should probably put it up top.
            print("This filetype is not supported, please use mov or mp4 (it might be supported but i dont care enough to check, branch it bitch)")
          
            
                
def convertToStills(paths,output,fps,overwrite):
    # if you need the number you can do enumerate()
    for i, path in enumerate(paths):
        outputDir = output + "/" + str(i)
        createDirectory(outputDir,overwrite)
        outputFileDir= outputDir + "/%04d.png" # This change is needed, or your sorted() later on is gonna sort the files into 1,10,2,3...
        convertCommand = "ffmpeg -i " + path + " -vf fps=" + str(fps) + " " + outputFileDir
        print("executing command: ",convertCommand)
        command = os.system(convertCommand)
        if command == 0:
            print("successfully converted video ",i)
        else:
            print("conversion of ",i," failed: ",command)
        

def compileImages(tempFolder,outputFolder,paths,fps,overwrite,concurrent):
    tempfileArray = []
    print(tempfileArray,"\n")
    tempfileNumberArray = []
    for i, path in enumerate(paths):
        workingDirectory = tempFolder + "/" + str(i)
        workingList = os.listdir(workingDirectory)
        workingNumberList = []
        try:
            # Lets do a list comprehension, they're neat and the coolest thing about python ever.
            workingList = [item[:-4] for item in workingList]
            workingList = sorted(workingList)
            
            for j in range(0,len(workingList)):
                workingNumberList.append(str(j+1) + ".png")
                workingList[j]=workingDirectory + "/" + str(workingList[j]) + ".png"
        except:
            pass
        tempfileArray.append(workingList)
        tempfileNumberArray.append(workingNumberList)
        print(tempfileArray[i],"\n",i,"\n",tempfileNumberArray[i],"\n")

    n = len(tempfileArray)
    outputfileArray = []
    outputfileNumberArray = []
    for i in range(0,n):
        j=i*concurrent
        # pretty sure (j >= 0) was always true?
        while j < len(tempfileArray[i]):
            print("now j is ",j)
            for k in range(0,concurrent):
                try:
                    outputfileArray.append(tempfileArray[i][j+k])
                    outputfileNumberArray.append(tempfileNumberArray[i][j+k])
                    print("appending ",j+k)
                except:
                     pass
            j = j + (n*concurrent)
            
    print(outputfileArray)
    print(outputfileNumberArray)

    imagesOutputFolder = outputFolder + "/images/"
    createDirectory(imagesOutputFolder,overwrite)
    for i in range(0,len(outputfileArray)):
        try:
            inputFilePath = outputfileArray[i]
            outputFilePath = imagesOutputFolder + outputfileNumberArray[i]
        except:
            pass
        print("moving file ",inputFilePath," to ",outputFilePath)
        moveCommand = "mv " + inputFilePath + " " + outputFilePath
        command = os.system(moveCommand)
        if (command == 0):
            print("success")
        else:
            print("failure code: ",command)
            #quit()


    convertBackToMp4Command = "ffmpeg -r " + str(fps) + " -f image2 -s 1920x1080 -i " + outputFolder+"/images/%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p "+outputFolder+"/output.mp4"
    command = os.system(convertBackToMp4Command)
    print("exited with code: ",command)
        

def checkDirExists(directory):
    doesExist = path.exists(directory)
    print(directory,"exists? ",doesExist)
    return doesExist
        

numberOfClips,fps,outputFolder,tempFolder,overwrite,concurrent = getArgs()
print(numberOfClips,fps,outputFolder,tempFolder)
createDirectory(tempFolder,overwrite) #You can maybe use tempfile here, https://docs.python.org/3/library/tempfile.html (it'll make a temporary directory for you). Though might not be a good idea if you ask the user to delete stuff too.
createDirectory(outputFolder,overwrite)



paths = getPaths(numberOfClips)
movToMp4(paths,tempFolder)
convertToStills(paths,tempFolder,fps,overwrite)
input("you can now delete any non required images. \nsync the start of all the image sequences. \nthis can get spicy from here on out\npress enter to continue when you are ready: ")
compileImages(tempFolder,outputFolder,paths,fps,overwrite,concurrent)


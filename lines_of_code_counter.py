#!/usr/bin/env python

# This Python script counts the lines of code in the directory in which it is
# run.  It only looks at files which end in the file extensions passed to the
# script as arguments.

# It outputs counts for total lines, blank lines, comment lines and code lines
# (total lines minus blank lines and comment lines).

# Example usage and output:
# > lines_of_code_counter.py .h .cpp
# Total lines:   15378
# Blank lines:   2945
# Comment lines: 1770
# Code lines:    10663

# This version adds:
# -proper command line arguments mgmt with argparse
# -multiple comments identifier
# -multiple source directories
# -auto file-encoding determination
# -reformatted output for improved readability

# Many thanks to rrwick for the original script, quick, effective and useful 


import argparse
import os.path
import codecs


def is_comment(line_of_code):
    global commentSymbols

    result = False
    for commentSymbol in commentSymbols:
        if line_of_code.startswith(commentSymbol):
            result = True
            break
    return result


parser = argparse.ArgumentParser(description='Count lines of code')
parser.add_argument('--exts', dest='extensions', metavar='N', type=str, nargs='+', help='list of extensions of files to parse')
parser.add_argument('--comments', dest='comments', metavar='N', type=str, nargs='+', help='list of comments line indicators')
parser.add_argument('--dirs', dest='dirs', metavar='N', type=str, nargs='+', help='directories to scan. If not specified takes current dir')

args = parser.parse_args()
acceptableFileExtensions = args.extensions
commentSymbols = args.comments
currentDirs = args.dirs

if not acceptableFileExtensions:
    print('Please pass at least one file extension as an argument, or --help for help.')
    quit()

if not commentSymbols:
    print('No comments symbol specified: there will be no comments count')

if not currentDirs:
    currentDirs = [os.getcwd()]

filesToCheck = []
for currentDir in currentDirs:
    for root, _, files in os.walk(currentDir):
        for f in files:
            fullpath = os.path.join(root, f)
            if '.git' not in fullpath:
                for extension in acceptableFileExtensions:
                     if fullpath.endswith(extension):
                        filesToCheck.append(fullpath)

if not filesToCheck:
    print('No files found.')
    quit()

lineCount = 0
totalBlankLineCount = 0
totalCommentLineCount = 0

print('Checking {num} files:'.format(num=len(filesToCheck)))
print('')
print('Lines\tBlank\tComment\tCode\tFilename')
print('-------\t-------\t-------\t-------\t-------')


for fileToCheck in filesToCheck:
    # Try to determine file encoding
    # you can add additional encodings here if necessary
    encodings = ['utf-8', 'windows-1250', 'windows-1252', 'latin-1']
    for e in encodings:
        try:
            fh = codecs.open(fileToCheck, 'r', encoding=e)
            fh.readlines()
            fh.seek(0)
        except UnicodeDecodeError:
            #print('got unicode error with %s , trying different encoding' % e)
            fh.close()
        else:
            #print('opening the file with encoding:  %s ' % e)
            fh.close()
            break

    with open(fileToCheck, encoding=e) as f:

        fileLineCount = 0
        fileBlankLineCount = 0
        fileCommentLineCount = 0

        for line in f:
            lineCount += 1
            fileLineCount += 1

            lineWithoutWhitespace = line.strip()
            if not lineWithoutWhitespace:
                totalBlankLineCount += 1
                fileBlankLineCount += 1
            elif is_comment(lineWithoutWhitespace):
                totalCommentLineCount += 1
                fileCommentLineCount += 1

        print(str(fileLineCount) + \
              "\t" + str(fileBlankLineCount) + \
              "\t" + str(fileCommentLineCount) + \
              "\t" + str(fileLineCount - fileBlankLineCount - fileCommentLineCount) + \
              "\t" + fileToCheck )


print('')
print('Totals')
print('--------------------')
print('Lines:         ' + str(lineCount))
print('Blank lines:   ' + str(totalBlankLineCount))
print('Comment lines: ' + str(totalCommentLineCount))
print('Code lines:    ' + str(lineCount - totalBlankLineCount - totalCommentLineCount))

# coding=utf-8

import os

def createClientFilePath(inFolderPath):
    cFilePaths = []
    i=0
    
    while i < 100 :
        cFilePath = os.path.join(inFolderPath, 'shadow.data', 'hosts', f'client{i+1}', f'client{i+1}.tor.1000.stdout')
        cFilePaths.append(cFilePath)
        i += 1
     
    return cFilePaths
    
def createRelayFilePath(inFolderPath):
    rFilePaths = []
    i=0
    
    while i < 38:
        if i<9:
            rFilePath = os.path.join(inFolderPath, 'shadow.data', 'hosts', f'relay{i+1}exitguard', f'relay{i+1}exitguard.tor.1000.stdout')
            rFilePaths.append(rFilePath)
            i += 1
            continue
        elif i>=9 and i<12:
            i += 1
            continue
        elif i>=12 and i<38: 
            rFilePath = os.path.join(inFolderPath, 'shadow.data', 'hosts', f'relay{i+1}guard', f'relay{i+1}guard.tor.1000.stdout')
            rFilePaths.append(rFilePath)
            i += 1
            continue

    return rFilePaths 
    
def createHsFilePath(inFolderPath):
    hsFilePath = os.path.join(inFolderPath, 'shadow.data', 'hosts', 'hiddenserver', 'hiddenserver.tor.1000.stdout') 
    
    return hsFilePath
    
def getAllNodeFilePath(inFolderPath):
    cFilePath = createClientFilePath(inFolderPath)
    rFilePath = createRelayFilePath(inFolderPath)
    
    print('[4] getAllNodeFilePath2(): get file paths of both client and relay.')
    return cFilePath, rFilePath      

def getAllNodeFilePath2(inFolderPath):
    cFilePath = createClientFilePath(inFolderPath)
    rFilePath = createRelayFilePath(inFolderPath)
    hsFilePath = createHsFilePath(inFolderPath)
    
    print('[4] getAllNodeFilePath(): get file paths of client, relay and hs.')
    return cFilePath, rFilePath, hsFilePath
    
 
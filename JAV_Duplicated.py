#JAV_Duplicated V1.2 for English and Korean, Written by SangDo_Kim, a user in AVDBS.com
#V1.2 변경 사항
#- 이 프로그램(독립 실행 파일)이 실행되지 않던 문제 해결
#- 품번 인식 모듈(JAV ProdCode) 개선
#- 설정 파일(텍스트 파일)을 저장하여, 다음에 실행할 때 불러오게 함.
#- 취합된 파일 목록을 텍스트 파일로 저장

import os
import sys
import tkinter
from tkinter import filedialog
from collections import Counter
from fnMakeList import fnMakeList, ErrNoPath, dictNoJAVFiles
import datetime as dt
import time

print("""JAV_Duplicated V1.2, written by SangDo_Kim, a user in AVDBS.com.
This Python program searches user specified folders and their subfolders and find out duplicated JAV files.
Duplication is identified by a JAV Product Code found in files (e.g JUL-332), not by full file name.
Subtilte files (*.srt, *.smi) are ignored.
이 프로그램은 사용자가 지정한 한 개 이상의 폴더들과 그 하위 폴더들을 검색하여 중복된 JAV 파일들을 찾아냅니다.
중복 여부는 파일 이름에 포함된 JAV 품번(예: JUL-332)으로 판단하며, 단순히 전체 파일 이름이 같은 경우를 찾는 것은 아닙니다.
자막 파일(*.srt, *.smi)은 무시됩니다.""")

#기존 설정 변수 읽어 오기(프로그램이 실행되는 경로에 JAV_Star_Names_Config.txt 설정 파일이 있는 경우).
lWorkingPath = []
bDefaultSetting = True
lDataList = []          #경로, 파일 이름, 품번을 담을 리스트
sProgramPath = os.getcwd()
sCfgFileName = "JAV_Duplicated_Config.txt"
iWorkingPathNo = 0
if os.path.isfile(sCfgFileName):
    fileConfig = open(sCfgFileName, "r", encoding="utf-8")
    lLines = fileConfig.readlines()
    for sLine in lLines:
        sLine = sLine.strip()
        if len(sLine) >= 2 and sLine.find(":") >= 0: #문자열이 제대로된 경로 이름인지 검사
            lWorkingPath.append(sLine)
    fileConfig.close()
    if len(lWorkingPath) == 0:
        bDefaultSetting = True
    else:
        bDefaultSetting = False

#나중에 폴더를 선택할 때를 대비한 작업
root = tkinter.Tk()
root.withdraw()

#기존 작업 경로들 처리
if bDefaultSetting == False:
    print(f"Importing previous Config file(기존 설정 파일 불러 오는 중): {sCfgFileName}")

    while True:
        print("-" * 10)
        for i in range(len(lWorkingPath)):
            print(f"[{i + 1}]: {lWorkingPath[i]}")
        print("-" * 10)
        print("To keep previous paths above, type [a], To remove one of them type its number:")
        sKeepOrRemove = str(input(f"위 기존 경로들을 유지하려면 [a], 하나를 제거하려면 그 번호를 입력하십시오: ")).lower()
        if sKeepOrRemove == "a":
            break
        if sKeepOrRemove.isdecimal():
            if int(sKeepOrRemove) <= len(lWorkingPath) or int(sKeepOrRemove) >= 1:
                print(f"Path removed(경로 제거됨): {lWorkingPath[int(sKeepOrRemove)-1]}")
                lWorkingPath.remove(lWorkingPath[int(sKeepOrRemove)-1])
        if len(lWorkingPath) == 0:
            print(f"All previous paths are removed(모든 기존 경로가 제거되었습니다).")
            break

    # 기존 경로들에 대해 경로, 파일 이름, 품번을 취합
    if len(lWorkingPath) >= 1:
        print("-" * 10)
        print(f"Listing files for the path and all the subfolders. Press Enter to proceed.")
        input(f"기존 경로와 모든 하위 폴더의 파일 목록을 취합합니다. 엔터를 눌러 진행하십시오.")
        print("-" * 10)

        iDataListLenPrev = len(lDataList)       #이 단계에서는 lDataList는 비어 있을 것임. 즉, 0임.
        lDataListAdded = []
        for sWorkingPath in lWorkingPath:
            iWorkingPathNo += 1
            try:
                lDataListAdded = fnMakeList(sWorkingPath, iWorkingPathNo)
                for lDataListAddedLine in lDataListAdded:
                    lDataList.append(lDataListAddedLine)
            except ErrNoPath:
                input("Error: No paths to work. 오류: 처리할 경로가 없음. 프로그램을 종료합니다.")
                sys.exit()
        print("-" * 10)
        print(f"Number of Files added(추가된 파일 수): {len(lDataList) - iDataListLenPrev}")

#중심 프로그램(반복하여 여러 명령 실행)
print("-"*10)
while True:
    print("Add a path [a], Check duplicated files for all paths [b], Save file list to a new file and Exit [c]: ")
    sInput = str(input("경로 추가 [a], 모든 경로에 대한 중복 파일 검사 [b], 새 파일에 파일 목록 저장 및 종료 [c]: ")).lower()
    sInput = sInput.lower()
    if sInput not in ('a', 'b', 'c'):
        continue

    #경로 추가
    if sInput == "a":
        print("Select a path(경로를 선택하십시오).")
        sAddOrNot = "a"
        sAddedPath = filedialog.askdirectory(parent=root, initialdir="/", title="Select AV folder(동영상 폴더 선택)")
        if sAddedPath in lWorkingPath:         #동일한 경로를 두 번 추가할 수 있으며, 이때 경고 메시지 보냄. 중복 추가를 허용하는 이유는 외장 하드 디스크를 바꿔가며 연결하여 여러 외장 하드 디스크들을 분석할 수 있도록 하기 위함임.
            print(f"Caution: The path you've selected is already in the added paths.\n" +
                  f"주의: 방금 선택한 경로는 이미 추가된 경로에 속합니다.: {sAddedPath}")
            while True:
                print(f"Add files in this path again? (e.g External hard disk or for other reasons) Add [a], Cancel [b]")
                sAddOrNot = str(input(f"이 경로의 파일들을 다시 추가할까요? (예: 외장 하드 디스크의 경우 등) 추가 [a], 취소 [b] :")).lower()
                if sAddOrNot in ('a', 'b'):
                    break
                else:
                    continue
        if sAddOrNot == 'b':
            print("The path was canceled(그 경로는 취소되었습니다.)")
        else:
            lWorkingPath.append(sAddedPath)
            print(f"A path added(추가된 경로): {lWorkingPath[-1]}")

            # 경로에 대해 그 안의 경로, 파일 이름, 품번을 취합
            print("-" * 10)
            print(f"Listing files for the path and all the subfolders. Press Enter to proceed.")
            input(f"해당 경로와 모든 하위 폴더의 파일 목록을 취합합니다. 엔터를 눌러 진행하십시오.")

            lDataListAdded = []
            iWorkingPathNo += 1
            try:
                lDataListAdded = fnMakeList(sAddedPath, iWorkingPathNo)
                for lDataListAddedLine in lDataListAdded:
                    lDataList.append(lDataListAddedLine)
                print("-"*10)
                print(f"Number of Files added(추가된 파일 수): {len(lDataListAdded)}")
            except ErrNoPath:
                input("Error: No paths to work. 오류: 처리할 경로가 없음. 프로그램을 종료합니다.")
                sys.exit()

    #중복 분석
    if sInput == "b":
        if len(lWorkingPath) <= 0:
            print("Add at least 1 folder(검색할 폴더를 한 개 이상 추가하십시오).")
        else:
            if len(lDataList) <= 1:
                print("File with Product Code is 1 or less. Cannot analyze.\n" +
                      "품번이 있는 파일 수가 1개 이하이므로 분석할 수 없습니다.")
            else:
                lDataList.sort(key=lambda x: (x[3], x[0], x[1], x[2]))        # 품번 순으로 정렬
                print("-" * 10)
                lProdCode = list(zip(*lDataList))[3]        #다중 리스트에서 품번만 가져옴.
                dictProdCode = dict(Counter(lProdCode))     #품번의 중복 수를 계산해서 딕셔너리로 만듦.
                iPrintCounter = 0                           #중복 품번들 인쇄 후 구분 줄을 넣기 위한 변수
                iDupNoTotal = 0                             #전체 중복 수
                lNoJAVFiles = list(dictNoJAVFiles.values()) #JAV 파일이 아닌 문자열 목록
                for i in range(len(lDataList)):             #전체 리스트를 처음부터 끝까지 확인
                    iDupNo = dictProdCode[lDataList[i][3]]  #현재 품번의 중복 수
                    if iDupNo == 1:                         #현재 품번이 중복되지 않았으면 넘어감.
                        iPrintCounter = 0
                        continue
                    elif lDataList[i][3] not in lNoJAVFiles:  #JAV 파일이면서 중복인 경우
                        print(f"{lDataList[i][3]}\t{lDataList[i][0]}\t{lDataList[i][1]}\t{lDataList[i][2]}")
                        iPrintCounter += 1                  #중복 품번 인쇄 횟수 증가
                        if iPrintCounter == iDupNo:         #인쇄 횟수가 해당 품번의 중복 수와 같은 경우 구분 줄을 넣고 총 중복 수 합산
                            iDupNoTotal += iDupNo
                            print("-" * 10)
                print(
                    f"Total files with Product Code: {len(lDataList)}. Number of duplication: {iDupNoTotal}.")
                print(f"품번이 있는 파일 수: {len(lDataList)}개. 중복 건 수: {iDupNoTotal}개")
                print("-" * 10)

    # 저장 및 종료
    if sInput == "c":
        #작업 경로를 설정 파일에 기록
        os.chdir(sProgramPath)
        fileConfig = open(sCfgFileName, "w", encoding="utf-8")
        for sWorkingPath in lWorkingPath:
            fileConfig.write(sWorkingPath)
            if lWorkingPath.index(sWorkingPath) < len(lWorkingPath):   #마지막 경로가 아니라면
                fileConfig.write("\n")
        fileConfig.close()

        #품번, 파일, 경로를 새 파일에 기록
        clNow = dt.datetime.now()
        sDataListFileName = f"JAVFileList_{clNow.year}{clNow.month:0>2}{clNow.day:0>2}_{clNow.hour:0>2}{clNow.minute:0>2}{clNow.second:0>2}.txt"
        filesDataList = open(sDataListFileName, "w", encoding="utf-8")
        lDataList.sort(key=lambda x: (x[0], x[1], x[2], x[3]))  # 원래대로 정렬

        lProdCode = list(zip(*lDataList))[3]  # 다중 리스트에서 품번만 가져옴.
        dictProdCode = dict(Counter(lProdCode))  # 품번의 중복 수를 계산해서 딕셔너리로 만듦.

        filesDataList.write(f"경로 번호\t경로\t파일 이름\t품번\t중복 여부\n")
        for i in range(len(lDataList)):
            if dictProdCode[lDataList[i][3]] > 1:       # 현재 품번 중복 여부
                filesDataList.write(f"{lDataList[i][0]}\t{lDataList[i][1]}\t{lDataList[i][2]}\t{lDataList[i][3]}\t중복\n")
            else:
                filesDataList.write(f"{lDataList[i][0]}\t{lDataList[i][1]}\t{lDataList[i][2]}\t{lDataList[i][3]}\t중복 아님\n")
        print(f"Number of file names listed(목록에 저장된 파일 이름 수): {i+1}")
        print(f"List file name(목록 파일 이름): {sDataListFileName}")
        filesDataList.close()

        input("Exiting the program. Thanks! 프로그램을 종료합니다. 감사합니다!")
        sys.exit()
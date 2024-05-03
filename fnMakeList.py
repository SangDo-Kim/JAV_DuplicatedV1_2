#fnMakeList V1.2, Written by SangDo_Kim, a user in AVDBS.com

import os
from JAV_ProdCode import fnExtractProdCode, ErrNoCode, lVideoFormats
class ErrNoPath(Exception):
    pass

dictNoJAVFiles = {"NPC": "*NoProdCode", "NVD": "*NoVideo", "SUB":"*Subtitles"}
def fnMakeList(sWorkingPath, iWorkingPathNo = 1):           #경로들의 목록을 받아서 해당 경로들과 그 하위 폴더까지 파일들을 취합하여 목록을 반환
    lDataListInternal = []
    if len(sWorkingPath) <= 0:             #경로가 없을 경우 ErrNoPath 오류 발생
        raise ErrNoPath

    #경로 및 하위 폴더들을 찾아다니며 그 안의 파일들을 목록으로 취합.
    for (sPath, lSubdir, lFiles) in os.walk(sWorkingPath):
        for sFileName in lFiles:
            sExt = os.path.splitext(sFileName)[-1].lower()
            if sExt == ".srt" or sExt == ".smi" or sExt == ".vtt":          #자막 파일 무시
                sProdCode = dictNoJAVFiles["SUB"]
            elif sExt[1:] not in lVideoFormats:         #동영상이 아니면 무시함.
                sProdCode = dictNoJAVFiles["NVD"]
            else:
                try:
                    sProdCode = fnExtractProdCode(sFileName)  #현재 파일 이름에 대해 품번을 추출하는 함수 호출
                except ErrNoCode:       #품번 추출 실패 시 이 파일 건너 뜀
                    sProdCode = dictNoJAVFiles["NPC"]

            lDataListInternal.append([iWorkingPathNo, sPath, sFileName, sProdCode])
            print(f"File listed(파일을 목록에 추가):\t{sProdCode}\t{sFileName}")
    return lDataListInternal                                #[경로, 파일 이름, 품번] 리스트를 취합하여 반환.

#테스트
if __name__ == "__main__":
    sWorkingPath = "E:/OneDrive/My_Documents/Study/Python Programs/Subdirectory_Sample/SampleAV_JAV_Name_Simple"
    try:
        lDataList = fnMakeList(sWorkingPath, 1)
        print(lDataList)
#        for i in range(len(lDataList)):
#            print(f"sPath:\t{lDataList[i][0]}, sFileName:\t{lDataList[i][1]}, sProdCode:\t{lDataList[i][2]}")
    except ErrNoPath:
        print(f"오류: ErrNoPath")
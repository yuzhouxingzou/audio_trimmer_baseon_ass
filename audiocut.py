import argparse
import sys
import os
import ffmpeg
import chardet
import datetime
#参数处理
parser = argparse.ArgumentParser()
parser.add_argument('-lass',metavar='AssfilePATH', type=str, help='ass文件路径', required=False)
parser.add_argument('-lv',metavar='VideoPATH', type=str, help='视频文件路径', required=False)
parser.add_argument('-lau',metavar='AudioPATH', type=str, help='音频文件路径', required=False)
parser.add_argument('-o',metavar='OutputPATH', type=str, help='输出文件路径(不填则为ass文件的路径下的output)', required=False)
parser.add_argument('-c',metavar='TheCodingWay', type=str, help='输出文件编码方式 详见README文档', required=False)
parser.add_argument('-f',metavar='OutputFileType', type=str, help='输出文件格式 详见README文档', required=False)
TempDump = parser.parse_args()
AssPath = TempDump.lass
VideoPath = TempDump.lv
AudioPath = TempDump.lau
OutputPath = TempDump.o
CodeType = TempDump.c
if(CodeType == None):
    CodeType = "flac"
if(CodeType == "flac" or "FLAC"):
    Filetype = "flac"
else:
    Filetype = TempDump.f
    if(Filetype == None):
        Filetype = CodeType
#判断是否提供输入文件及是否冲突、确定输入文件
if((VideoPath == None and AudioPath == None) or (VideoPath != None and AudioPath != None)):
    print("请使用-lv“或”-lau参数提供视频文件“或”音频文件路径 使用-h参数运行以获取参数帮助")
    input()
    sys.exit(1)
if(AssPath == None):
    print("请使用-lass参数提供ass文件路径 输入-h获取参数帮助")
    input()
    sys.exit(1)
if(AudioPath != None):
    InputPath = str(AudioPath)
else:
    InputPath = str(VideoPath)
#转换输入素材目录
FolderClips = AssPath.split("\\")
del FolderClips[(len(FolderClips) - 1)]
AssFolder = '\\'.join(FolderClips)
#处理输出目录
if(OutputPath == None):
    ExistingTest = os.path.exists(AssFolder + "\output")
    if(ExistingTest == True):
        print("未提供输出路径且ass文件所处目录下已存在output文件夹 程序无法继续")
        input()
        sys.exit(1)
    else:
        os.mkdir(AssFolder + "\output")
        OutputPath = AssFolder + "\output"
#字幕文件编码检测
AssFile = open(AssPath,'br')
EncodingTest = AssFile.read(500)
AssEncode = chardet.detect(EncodingTest)['encoding']
#打开文件
try:
    AssFile = open(AssPath,'r',encoding = AssEncode)
except:
    print("字幕文件不存在")
#ass文件验证
Verify = str(AssFile.readline())
if(Verify != "[Script Info]\n"):
    print("输入文件不是(标准)ass文件")
    input()
    sys.exit(1)
Details = AssFile.readlines()
OutputCount = 1
LengthSummary = (datetime.datetime.strptime('0:00:00.00', '%H:%M:%S.%f'))
print((str(OutputPath) + "\\" + str(OutputCount) + "." + str(CodeType)))
for line in Details:
    if("Comment: " in line):
        LineClips = line.split(",",3)
        StartTime = LineClips[1]
        EndTime = LineClips[2]
        ClipLength = (datetime.datetime.strptime(EndTime, '%H:%M:%S.%f')) - (datetime.datetime.strptime(StartTime, '%H:%M:%S.%f'))
        ffmpeg.input(InputPath, ss=StartTime).output((str(OutputPath) + "\\" + str(OutputCount) + "." + str(CodeType)), to = ClipLength, acodec = str(Filetype)).run()
        OutputCount = OutputCount + 1
        LengthSummary = LengthSummary + ClipLength
print("运行已结束\n本次运行共裁剪音频" + str(OutputCount - 1) + "段\n裁剪总时长" + str(LengthSummary))
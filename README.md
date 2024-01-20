# audio_trimmer_baseon_ass #
使用ass字幕文件为基础的音频切片程序
## 演示视频 ##
bilibili:[https://www.bilibili.com/video/BV1Vb4y1N7H4/](https://www.bilibili.com/video/BV1Vb4y1N7H4/)

Youtube:[https://www.youtube.com/watch?v=dhfHOSZLwPw](https://www.youtube.com/watch?v=dhfHOSZLwPw)
## 程序优势 ##
相较于使用音频编辑软件，使用本程序裁剪可以在已有字幕的前提下，通过更方便的字幕处理软件，快速裁剪所需要的音频片段，大大减少声音模型的训练的准备工作(准备音频源)所需的时间
## 环境要求 ##
python 3.11 测试可用 其他版本应该也没问题

使用的库：
> argparse、ffmpeg、chardet、datetime

系统应该无需安装ffmpeg

如果无法运行可以改用编译后的版本
## 参数说明 ##
### 必选参数 ###
  -lass 输入的ass文件路径

  -lv 输入的视频文件路径

  -lau 输入的音频文件路径 

（-lv和-lau一次只能提供一个，否则会报错）
### 可选参数 ###
  -o 输出文件路径(不填则为ass文件的路径下的output。在未指定输出目录的情况下，如果已有output文件夹则会报错；如果已提供但输出文件重名，ffmpeg则会问是否要覆写)

  -c  输出文件编码方式(详见后面章节)

  -f 输出文件格式(详见后面章节)


## 编码方式与输出文件格式 ##
-c可以提供的参数值可以是ffmpeg支持编码器的任何值，建议使用flac，不填即为flac

**如果下面什么都看不懂，不填就对了**

这个所谓的编码方式指的是这个程序要如何对你的输入进行编码，而不是你的输入文件是什么编码的，更不需要重编码后再输入

上面的输出文件格式其实是指的后缀名，如果是-c的值是flac就无需填写此项(不填此选项即为flac)；如果不是的话，你提供的参数如果恰好可以作为文件名后缀，可不提供-f的值，此时-c的值将作为文件后缀

可以使用`ffmpeg configure -encoders`命令查看(查看的是本地在环境变量里的ffmpeg的支持的编码器，不过问题不大)，所有第一个字母是A的都是音频格式

常见的(不保证其正确性，且前面的参数是达到后面格式的充分不必要条件)
> flac  FLAC格式
> 
> ac3   AC-3格式
> 
> acc   ACC格式
>
> pcm_xxx   WAV格式
>
> mp3_mf   MP3格式

如果是源视频/音频是无损编码，那就无所谓了，可以转换成其他无损不压缩格式、无损压缩格式、有损压缩格式，无损的话建议flac，有损自选

如果是有损编码，就不要进行有损编码了(当然非要这样弄也不是不行，反正我是受不了)，此程序不支持复制音频流(因为就我平时使用ffmpeg来讲，在不重编码的情况下裁剪有时会发生奇奇怪怪的问题，比如最后输出的文件还是原时长但是时间的音频只有一小段，也有可能是我方法不对。总之，为了兼容性，暂不支持)，所以建议转为无损压缩格式(如flac)

## 关于ass文件 ##
ass文件开头必须是`[Script Info]`，这里是为了验证这个文件是ass文件的（但这个开头是这个文件是标准ass文件的充分不必要条件，也不能完全验证），如果开头不是`[Script Info]`，将报错

## 具体操作步骤 ##
(以aegisub作为演示软件，你可以在这里[https://aegisub.org/downloads/](https://aegisub.org/downloads/)下载它)

1.打开视频对应的ass文件，ctrl+a全选所有行，选中注释再取消(将所有行都设为对白行)

![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E6%B3%A8%E9%87%8A%E6%88%AA%E5%9B%BE.png)

2.将视频或音频文件拖入窗口中，打开参考文件

3.aegisub小技巧

a.使用前建议先将这几个选项勾上

![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E9%80%89%E9%A1%B9.png)

b.点击查看可以仅显示频谱图而不显示视频
![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E4%BB%85%E9%9F%B3%E9%A2%91.png)

c.aegisub常见快捷键:
> s/空格 播放当前行
>
> q 播放当前行的行前500ms、
> 
> w 播放当前行的行后500ms
> 
> d 播放当前行最后的500ms
> 
> g/Enter 提交当前行
> 
> 鼠标左键 设置入点
> 
> 鼠标右键 设置出点

4.将想要的内容设置为注释行，程序会裁剪所有的注释行

(下面两种方法均可，方便程度不同)
### A ###
1.用播放当前行或者看对白内容的方式，确定你要的那个人的行，调轴并**使用按钮**将其设为注释
![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E6%B3%A8%E9%87%8A%E6%88%AA%E5%9B%BE.png)
### B ###
1.选中所有行，在文字编辑框中删除
![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E5%88%A0%E9%99%A4%E6%89%80%E6%9C%89%E8%A1%8C%E5%86%85%E5%AE%B9.gif)

2.将光标放在文字框上，复制一段任意内容，如`asf54gf`，回车换行，遇到想要的行就把这段内容粘上


3.然后，字幕-选择多行，让后如图选择

![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E9%80%89%E6%8B%A9%E5%A4%9A%E8%A1%8C.png)  ![](https://raw.githubusercontent.com/yuzhouxingzou/audio_trimmer_baseon_ass/main/demoimages/%E9%80%89%E6%8B%A9%E5%A4%9A%E8%A1%8C%E8%AE%BE%E7%BD%AE.png)

4.ctrl+x剪切，选择第一行，ctrl+v粘贴，调轴并将这几行设为注释

## 后续开发计划 ##
1.-lv和-lau参数合并(我是不太知道为什么我一开始要写成分着的，好像什么用没有)

2.使用其他的Speaker Diarization程序，得到想要的人所在的时间段，再用这个结果匹配字幕文件(因为我感觉说话人分类的时间卡的准度没法符合我的要求，我用过whisper[https://huggingface.co/spaces/aadnk/whisper-webui/tree/main](https://huggingface.co/spaces/aadnk/whisper-webui/tree/main)附带的说话人分类，反正不是很准)。主要做的是匹配字幕文件这个过程
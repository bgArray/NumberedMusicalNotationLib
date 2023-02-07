# Todo and Note

随手写的，不开发的朋友们可以不需要看。

先贴几张简谱
<img src="https://foruda.gitee.com/images/1674971836981507513/94b3d440_10062986.png">
<img src="https://foruda.gitee.com/images/1674972020183061068/e051d00b_10062986.png">
<img src="https://foruda.gitee.com/images/1674972040612048151/7136d8ec_10062986.png">
(以后再加吧)

我认为主要要实现的有几个

总类下面应该还是要分轨道或者声部的

第一部分应该是简谱元事件
1. title - subtitle - lyricist - composer
2. key
3. tempo
4. time signature
5. copyright

差不多这些，以后再补充，反正就是特定事件及文本

然后第二部分应该是普通音符事件
1. note(true_pitch, show_num, pitch_dot=[], rhythm_type, rhythm_dot)
2. rest(rhythm_type, rhythm_dot)
3. bar_line(type)
4. appoggiatura(aim, direction, type, note())

再接着就是所有记号组了
1. 音符记号(颤音、重音、停止音、连音线、变音号(升降音)、奏法记号、力度记号)
2. 线性记号(颤音线、圆滑线、渐强渐弱、反复跳跃、高低八度、踏板)
3. 文本记号(任意文本、歌词文本、指法文本、呼吸和停顿记号、排练号、图片文本)
4. 排版记号(换行、换页)

差不多，感觉齐活

构思一下继承关系

`NMNFile()`负责整个简谱文件接口

`NMNPic()`负责向图片输出排版接口

----

`Event() 事件基类 `

->`MetaEvent() 元事件基类`；->音符各类事件

----

`Notation() 记号基类`

-> 各类记号

---

然后NMN()继承NMNFile()

NMN() 是简谱主类，文件流方法来自NMNFile()，图片流方法来自NMNPic()

直接包含一些MetaEvent() 主要是title那些，速度、调号可以先不要也行

然后下辖Track()类，Track()继承list()

Track()可以加许多Event()

但是Track里直接包含的应该是~~Bar()~~ Measure()类，也继承自list()

所有事件都应在~~Bar~~ Measure里面

最常见的音符可能直接在~~Bar~~ Measure里面，也有可能不是

当多个音符同时按下的时候

应该是这样（abc都是音符实参）：Chord()类，也继承自list()

`Bar[Chord[Note(a, b, c), Note(a1, b1, c1)], Chord[Note(a2, b2, c2), Note(a3, b3, c3)]]`

音符就是这样，不过chord+note的形式有待确认，是不是一个单音也要放到chord里不确定。

因为bar需要管理小节节拍，如果有chord的话就是要加上chord的时值的

等会，

我突然想到还有声部 和 第二遍旋律小改 两种恶心玩意

我先瞅一眼musescore是怎么记号声部的

我回来了，我看了一眼，我的谱子如下：

<img src="https://foruda.gitee.com/images/1674974836528358130/41be0740_10062986.png">

第一小节的xml如下：

<img src="https://foruda.gitee.com/images/1674974890365011346/87908b71_10062986.png">

~~(有点纠结到底要不要跟ms统一标签为measure，我觉得bar短一点)~~

就measure了

可以看到有一个Voice 声部类，感觉也挺好，可以在measure里加一个参数表该小节有多少声部

至于时间管理，看到ms里是chord统一管理节拍，那就跟他保持一致了

第二小节我就直接粘贴了：
```text
      <Measure>
        <voice>
          <Chord>
            <durationType>half</durationType>
            <Note>
              <Spanner type="Tie">
                <Tie>
                  </Tie>
                <next>
                  <location>
                    <fractions>1/2</fractions>
                    </location>
                  </next>
                </Spanner>
              <pitch>60</pitch>
              <tpc>14</tpc>
              </Note>
            <Note>
              <Spanner type="Tie">
                <Tie>
                  </Tie>
                <next>
                  <location>
                    <fractions>1/2</fractions>
                    </location>
                  </next>
                </Spanner>
              <pitch>64</pitch>
              <tpc>18</tpc>
              </Note>
            <Note>
              <pitch>67</pitch>
              <tpc>15</tpc>
              </Note>
            </Chord>
          <Chord>
            <durationType>quarter</durationType>
            <Note>
              <Spanner type="Tie">
                <prev>
                  <location>
                    <fractions>-1/2</fractions>
                    </location>
                  </prev>
                </Spanner>
              <pitch>60</pitch>
              <tpc>14</tpc>
              </Note>
            <Note>
              <Spanner type="Tie">
                <prev>
                  <location>
                    <fractions>-1/2</fractions>
                    </location>
                  </prev>
                </Spanner>
              <pitch>64</pitch>
              <tpc>18</tpc>
              </Note>
            <Note>
              <pitch>67</pitch>
              <tpc>15</tpc>
              </Note>
            </Chord>
          <Rest>
            <durationType>quarter</durationType>
            </Rest>
          </voice>
        </Measure>
```
可以看到ms的连音线是通过一个正负分数值来描述的，具体规则我之前研究过，晚点找出来，
但是重要的是连音线这个Notation是放在Note下的，这一点值得参考

然后是下两小节，拓展版小节线：
```text
      <Measure>
        <voice>
          <Chord>
            <durationType>quarter</durationType>
            <Note>
              <Spanner type="Tie">
                <Tie>
                  </Tie>
                <next>
                  <location>
                    <fractions>3/4</fractions>
                    </location>
                  </next>
                </Spanner>
              <pitch>69</pitch>
              <tpc>17</tpc>
              </Note>
            </Chord>
          <Rest>
            <durationType>quarter</durationType>
            </Rest>
          <Chord>
            <durationType>quarter</durationType>
            <Note>
              <pitch>71</pitch>
              <tpc>19</tpc>
              </Note>
            </Chord>
          <Chord>
            <durationType>quarter</durationType>
            <Note>
              <Spanner type="Tie">
                <Tie>
                  </Tie>
                <next>
                  <location>
                    <measures>1</measures>
                    <fractions>-3/4</fractions>
                    </location>
                  </next>
                </Spanner>
              <Spanner type="Tie">
                <prev>
                  <location>
                    <fractions>-3/4</fractions>
                    </location>
                  </prev>
                </Spanner>
              <pitch>69</pitch>
              <tpc>17</tpc>
              </Note>
            </Chord>
          </voice>
        </Measure>
      <Measure>
        <voice>
          <Chord>
            <durationType>quarter</durationType>
            <Note>
              <Spanner type="Tie">
                <prev>
                  <location>
                    <measures>-1</measures>
                    <fractions>3/4</fractions>
                    </location>
                  </prev>
                </Spanner>
              <pitch>69</pitch>
              <tpc>17</tpc>
              </Note>
            </Chord>
          <Rest>
            <durationType>quarter</durationType>
            </Rest>
          <Rest>
            <durationType>half</durationType>
            </Rest>
          </voice>
        </Measure>
```
可以看到跨小节的有单独参数控制，连两次是两个Notation。

最后一个4个声部的小节也没啥特别的了，就是4个<voice>

所以有的Notation就是放在音符底下的，有的可以放在外面。MetaEvent也是。

差不多就这样，没写的开写的时候应该我会自己处理好。

我先去把我曾经写的注释找出来。

跟金羿讨论完，决定还是叫Measure()类，别弄错了。

---
2/7 考试补充一点
自由节奏就采取mid时间，然后也允许采用mid计时，也允许采用双计时
---

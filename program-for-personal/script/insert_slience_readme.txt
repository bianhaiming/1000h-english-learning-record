1. 按句子切割,插入句子等长静音
python insert_silence.py 022901_o.mp3 022901_s.mp3 --min_silence_len 500  --silence_thresh -48

2. 按逗号或更短的停顿切割,插入等长的静音等待
python insert_silence.py 022901_o.mp3 022901_c.mp3 --min_silence_len 210  --silence_thresh -48 

3. 波形分析网站
https://audiomass.co/

4. 示例指令 python insert_silence.py Discourse_difficulties-and_20240822_074133-nova.mp3 Discourse_difficulties-and_20240822_074133-nova_s.mp3 --min_silence_len 500  --silence_thresh -48


5. 进一步解释  
 input.mp3: 输入文件。
output.mp3: 处理后输出的文件。
--min_silence_len 1500: 分割静音时间至少为 1500 毫秒的部分。
--silence_thresh -50: 静音阈值设为 -50 dB。
--silence_multiplier 2.0: 静音时长为当前音频块时长的 2 倍。
通过这种方式，你可以在运行代码时灵活设置静音时长与当前音频块时长的倍数关系。

6. python script.py input.mp3 output.mp3 --min_silence_len 1500 --silence_thresh -50 --silence_multiplier 2.0

7. 指令调试-增加静音时长 2.0 倍数
python insert_silence.py Discourse_difficulties-and_20240822_074133-nova.mp3 Discourse_difficulties-and_20240822_074133-nova_s.mp3 --min_silence_len 500  --silence_thresh -48  --silence_multiplier 2.0

8. 绝地路径调试

python /Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/insert-slience/insert_silence.py /Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/20240822/Discourse_difficulties-and_20240822_074133-nova.mp3 /Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/Discourse_difficulties-and_20240822_074133-nova_s3.mp3 --min_silence_len 500  --silence_thresh -48  --silence_multiplier 2.0


/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/insert-slience/insert_silence.py
/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/insert_silence.py 
/Users/bianhaiming/EnjoyLibrary/1000h-english-learning-record/20240822/Discourse_difficulties-and_20240822_074133-nova.mp3


 
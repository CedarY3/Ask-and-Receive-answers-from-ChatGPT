需要配置以下：

1，API key
通过下述url获取：https://platform.openai.com/account/api-keys
然后将您的API key 填写在 config.py 的第4行

2，网络代理
一般来说只需要改写端口号就行，以clash为例，主页选项的第一项即是端口。
您可以将其设为7890，或将config.py的第23行proxies的7890改为您的端口号。



另外提醒！

main.py 演示了ask函数的简单使用，main.py的运行结果.png 展示了main的运行结果。

应用示例文件夹中的 get_root.py 演示了一个案例
该案例读取考研单词，然后询问GPT每个单词的词根和前后缀，最好存储GPT的回答。
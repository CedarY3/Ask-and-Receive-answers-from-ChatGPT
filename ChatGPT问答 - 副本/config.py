# API_KEY = "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" 此key无效
# 填写您的api key，通过下述url获取：https://platform.openai.com/account/api-keys

API_KEY = "sk-0ax09iJ"  # 此api无效

API_URL = "https://api.openai.com/v1/chat/completions"

# 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

# 改为True应用代理
USE_PROXY = True
if USE_PROXY:

    # 填写格式是 [协议]://  [地址] :[端口] ，
    # 例如    "socks5h://localhost:11284"
    # [协议] 常见协议无非socks5h/http，例如 v2*** 和 s** 的默认本地协议是socks5h，cl**h 的默认本地协议是http
    # [地址] 懂的都懂，不懂就填localhost或者127.0.0.1肯定错不了（localhost意思是代理软件安装在本机上）
    # [端口] 在代理软件的设置里，不同的代理软件界面不一样，但端口号都应该在最显眼的位置上


    # 代理网络的地址，打开你的科学上网软件查看代理的协议(socks5/http)、地址(localhost)和端口(11284)
    # proxies = {"http": "socks5h://127.0.0.1:61670", "https": "socks5h://127.0.0.1:61670", }
    proxies = {"http": "http://localhost:7890", "https": "http://127.0.0.1:7890", }
    print('网络代理状态：运行。')
else:
    proxies = None
    print('网络代理状态：未配置。无代理状态下很可能无法访问。')

# 发送请求到OpenAI后，等待多久判定为超时
TIMEOUT_SECONDS = 25

# 网页的端口, -1代表随机端口
WEB_PORT = -1

# 如果OpenAI不响应（网络卡顿、代理失败、KEY失效），重试的次数限制
MAX_RETRY = 2

# 选择的OpenAI模型是（gpt4现在只对申请成功的人开放）
LLM_MODEL = "gpt-3.5-turbo"

# 设置并行使用的线程数
CONCURRENT_COUNT = 100

# 设置用户名和密码
AUTHENTICATION = [] # [("username", "password"), ("username2", "password2"), ...]

# 检查一下是不是忘了改config
if len(API_KEY) != 51:
    assert False, "正确的API_KEY密钥是51位，请在config文件中修改API密钥, 添加海外代理之后再运行。" + \
                  "（如果您刚更新过代码，请确保旧版config_private文件中没有遗留任何新增键值）"

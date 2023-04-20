# 借鉴了 https://github.com/GaiZhenbiao/ChuanhuChatGPT 项目
"""
    该文件中主要包含三个函数

    不具备多线程能力的函数：
    1. predict: 正常对话时使用，具备完备的交互功能，不可多线程

    具备多线程调用能力的函数
    2. predict_no_ui：高级实验性功能模块调用，不会实时显示在界面上，参数简单，可以多线程并行，方便实现复杂的功能逻辑
    3. predict_no_ui_long_connection：在实验过程中发现调用predict_no_ui处理长文档时，和openai的连接容易断掉，这个函数用stream的方式解决这个问题，同样支持多线程
"""

import json
import traceback
import requests

from config import proxies, API_URL, API_KEY, TIMEOUT_SECONDS, MAX_RETRY, LLM_MODEL

timeout_bot_msg = '[local] Request timeout, network error. please check proxy settings in config.py.'

def get_full_error(chunk, stream_response):
    """
        获取完整的从Openai返回的报错
    """
    while True:
        try:
            chunk += next(stream_response)
        except:
            break
    return chunk

def generate_payload(inputs, history, system_prompt, stream):
    """
        整合所有信息，选择LLM模型，生成http请求，为发送请求做准备
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    conversation_cnt = len(history) // 2

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_cnt:
        for index in range(0, 2 * conversation_cnt, 2):
            what_i_have_asked = {}
            what_i_have_asked["role"] = "user"
            what_i_have_asked["content"] = history[index]
            what_gpt_answer = {}
            what_gpt_answer["role"] = "assistant"
            what_gpt_answer["content"] = history[index + 1]
            if what_i_have_asked["content"] != "":
                if what_gpt_answer["content"] == "": continue
                if what_gpt_answer["content"] == timeout_bot_msg: continue
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
            else:
                messages[-1]['content'] = what_gpt_answer['content']

    what_i_ask_now = {}
    what_i_ask_now["role"] = "user"
    what_i_ask_now["content"] = inputs
    messages.append(what_i_ask_now)

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 1.0, #temperature,  # 1.0,
        "top_p": 1.0,# top_p,  # 1.0,
        "n": 1,
        "stream": stream,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    print(f" {LLM_MODEL} : {conversation_cnt} : {inputs}")
    return headers, payload

def predict_no_ui(inputs, history=[], sys_prompt=""):
    """
        发送至chatGPT，等待回复，一次性完成，不显示中间过程。
        predict函数的简化版。
        用于payload比较大的情况，或者用于实现多线、带嵌套的复杂功能。

        inputs 是本次问询的输入
        top_p, temperature是chatGPT的内部调优参数
        history 是之前的对话列表
        （注意无论是inputs还是history，内容太长了都会触发token数量溢出的错误，然后raise ConnectionAbortedError）
    """
    headers, payload = generate_payload(inputs, history, system_prompt=sys_prompt, stream=False)

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            response = requests.post(API_URL, headers=headers, proxies=proxies,
                                    json=payload, stream=False, timeout=TIMEOUT_SECONDS*2); break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'请求超时，正在重试 ({retry}/{MAX_RETRY}) ……')

    try:
        result = json.loads(response.text)["choices"][0]["message"]["content"]
        return result
    except Exception as e:
        if "choices" not in response.text: print(response.text)
        raise ConnectionAbortedError("Json解析不合常规，可能是文本过长" + response.text)


def predict_no_ui_long_connection(inputs, top_p, temperature, history=[], sys_prompt=""):
    """
        发送至chatGPT，等待回复，一次性完成，不显示中间过程。但内部用stream的方法避免有人中途掐网线。
    """
    headers, payload = generate_payload(inputs, top_p, temperature, history, system_prompt=sys_prompt, stream=True)

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            response = requests.post(API_URL, headers=headers, proxies=proxies,
                                    json=payload, stream=True, timeout=TIMEOUT_SECONDS); break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'请求超时，正在重试 ({retry}/{MAX_RETRY}) ……')

    stream_response =  response.iter_lines()
    result = ''
    while True:
        try: chunk = next(stream_response).decode()
        except StopIteration: break
        if len(chunk)==0: continue
        if not chunk.startswith('data:'): 
            chunk = get_full_error(chunk.encode('utf8'), stream_response)
            raise ConnectionAbortedError("OpenAI拒绝了请求:" + chunk.decode())
        delta = json.loads(chunk.lstrip('data:'))['choices'][0]["delta"]
        if len(delta) == 0: break
        if "role" in delta: continue
        if "content" in delta: result += delta["content"]; print(delta["content"], end='')
        else: raise RuntimeError("意外Json结构："+delta)
    return result


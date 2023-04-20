from config import proxies, API_URL, API_KEY, TIMEOUT_SECONDS, MAX_RETRY, LLM_MODEL
import time
from predict import predict_no_ui as ask
fast_debug = False

answer = ask('计算机考研408的具体内容有哪些？')

print(answer)

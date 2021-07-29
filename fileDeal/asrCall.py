from aip import AipSpeech
""" 你的 APPID AK SK """
APP_ID = '23838315'
API_KEY = '5zy5XtyuGFIOsSRW16up3wCQ'
SECRET_KEY = 'Y9xkygksP1YsU3hzRz9GBsd1Ih596zl6'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

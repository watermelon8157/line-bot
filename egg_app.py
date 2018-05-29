#全域參數 常常更新用
web_url = 'http://wikieggs.ddns.net'; #網站DonamName
web_image = 'https://image.ibb.co/mXNMiJ/1527430007172.jpg'; #網站用圖片
image_url = web_url + '/Images/EVENT/';

_tempList = []

import requests
import re
import json
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
# line_bot_api
line_bot_api = LineBotApi('4XZuwm1PtF5Mo9hsm9pxvVDkzB/3Hpk6guO/yR6t+lh5Bm9MAmc3zaWTZr3+oWfaItY7e2tfPxOAjGxA7MlqGFkfEBSi15Kv5zKESAJqJdMNvP7fZmZUZB53/JqHMM2S13Y/G1epWlwuFd6EYcXb/AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3e451da8bec99b211fb6142824891424')


# 監聽所有來自 /callback 的 Post Request
# @app.route('/') 為網址根目錄，當使用者瀏覽時，就會執行 index() 函式
@app.route("/callback", methods=['POST'])  
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    bodyjson=json.loads(body)
    #app.logger.error("Request body: " + bodyjson['events'][0]['message']['text'])
    app.logger.error("Request body: " + body)

    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#是否是數值
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#危雞百顆obj
class WIKI_EGG(object):
    #建構子
    #msg: 使用者輸入訊息
    #user_id: 使用者代碼
    def __init__(self,msg,user_id):
        self.msg = msg;
        self.isThisFun = False; #是否是這個fun的Key
        self.isThisNotReturn = False;#是否回傳內容
        self.user_id = user_id;#使用者ID
        self.result =  TextSendMessage(text = self.msg) #預設啞啞學語
        self.factory_fn() #工廠功能
        self._tList = [] #功能清單

    #工廠功能
    def factory_fn(self):
        self.fn_test_q();#蛋蛋測試區
        self.fn_info_q();#蛋蛋長知識
        self.fn_event_q();#食安快訊 
        self.fn_web_q();#危雞百顆  
        if not self.isThisFun:
            self.result =  TextSendMessage(text = "歡迎使用蛋BOT！請點選「查看更多資訊」選擇功能")  
        pass

   #蛋蛋測試區
    def fn_test_q(self):
        if self.isThisFun:
            return;
        #測驗選項
        self._tList = [
            ['蛋蛋測試區','新鮮度測驗','作答完4個選項，可以知道自己的蛋新不新鮮唷!'],
            ['2.購買天數','請輸入雞蛋買了幾天？格式為：半形阿拉伯數字。例：1-30\n當雞蛋從母雞的屁股出來後，新鮮度會一值下降唷!','請再回答兩個問題'],
            ['3.是否為洗選蛋','3.選擇是否為洗選蛋','是洗選蛋','我買的是洗選蛋','不是洗選蛋','我買的不是洗選蛋'],
            ['4.儲存環境', '4.選擇儲存環境', '再回答5.儲存環境','室溫','我把雞蛋放在室溫','冰箱','我把雞蛋放在冰箱'],
            ['5.看雞蛋測驗結果','5.我要看雞蛋測驗結果']
           ]
        self._tList.append([self._tList[0][0],self._tList[2][1],self._tList[3][1],self._tList[4][1],'1.選擇您所在地區'])#使用者選擇清單
        self._tList.append(['1.您所在地區?',self._tList[5][4], '北部', '我在北部', '中部', '我在中部', '南部', '我在南部']);
        self._tList.append([self._tList[2][3],self._tList[2][5],self._tList[3][4],self._tList[3][6],self._tList[6][3],self._tList[6][5],self._tList[6][7]]) #回答類別，不包含'4.我要看雞蛋測驗結果'
        
        self._actionList = [
             MessageTemplateAction(
                label=  self._tList[6][0],
                text = self._tList[6][1]
            ),   
            MessageTemplateAction(
                label=  self._tList[1][0],
                text = self._tList[1][1]
            ),                    
            MessageTemplateAction(
                label= self._tList[2][0],
                text = self._tList[2][1]
            ),                          
            MessageTemplateAction(
                label= self._tList[3][0],
                text = self._tList[3][1]
            ) 
            ]
        #選擇回答題目
        #app.logger.error("Request msg: " + self.msg)
        _isInList = False;
        if self.msg in self._tList[5]:
            #app.logger.error("Request 5: " + self.msg)
            _isInList = True;
        elif self.msg in self._tList[7]:
            #app.logger.error("Request 7: " + self.msg)
            _isInList = True;
        if _isInList:
            #app.logger.error("Request _isInList: " + self.msg)
            self.isThisFun = True;
            self._test_q_item();#測驗功能
            self._test_q_temp();#您所在地區溫度
            self._test_q_wash_egg(); #是否為洗選蛋
            self._test_q_store(); #儲存環境
            self._test_q_result();#看雞蛋測驗結果
        elif self.msg ==  self._tList[1][1]:
            #請輸入雞蛋買了幾天？格式為：半形阿拉伯數字。例：1-30
            self.isThisNotReturn= True;
        else:
            if  RepresentsInt(self.msg):  
                self._test_q_days();  #購買天數 
        #選擇答案     
        if  self.msg in self._tList[7]:
            #self.isThisNotReturn= True;#不回傳項目
            pass
        pass

    #蛋蛋長知識
    def fn_info_q(self):
        if self.isThisFun:
            return;
        if self.msg == '蛋蛋長知識':
            self.isThisFun = True;
            _info = json.loads(requests.get(web_url+'/Data/getinfo?LineID='+self.user_id).text)
            #app.logger.error("requests json: " + str(_info))
            #aa['Q_DESC'] #aa['Q_MEMO']
            self.result =  TextSendMessage(text = 'Q:'+_info['Q_DESC'] + '\n\nA;' +  _info['Q_MEMO'])        
        pass
    
    #食安快訊
    def fn_event_q(self):
        if self.isThisFun:
            return;
        if self.msg == '食安快訊':
            self.isThisFun = True;
            _info = json.loads(requests.get(web_url+'/Data/getEvent?LineID='+self.user_id).text)
            app.logger.error("requests json: " + str(_info))
            self.result = TemplateSendMessage(
                alt_text='觀看食安快訊',
                    template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/NNKBnQJ.png', #預設圖案
                            action = URITemplateAction(
                                label= '食安新聞',
                                uri=  i['EVENT_URL'] 
                            )
                        ) for i in _info
                    ]
                    )
            )
        pass
    
    #危雞百顆
    def fn_web_q(self):
        if self.isThisFun:
            return;
        if self.msg == '危雞百顆':
            self.isThisFun = True;
            self.result =  TemplateSendMessage(
                alt_text='危雞百顆',
                    template=ImageCarouselTemplate(
                    columns=[
                    ImageCarouselColumn(
                        image_url= web_image,
                        action = URITemplateAction(
                            label='危雞百顆',
                            uri= web_url
                        )
                    ) 
                    ]
                    )
            )
        pass
 
    #試區題目選單
    def _test_q_item(self):
         
        if self.msg == self._tList[5][0]:
            #取得測試區題目選單
            self.result =  TemplateSendMessage(
                    alt_text = self._tList[0][1],
                    template = ButtonsTemplate(
                        title= self._tList[0][1],
                        text=  self._tList[0][2],
                        thumbnail_image_url='https://i.imgur.com/M8u7F7a.png',
                        #image_background_color = '#FFE5CC'
                        actions=[i for i in self._actionList]
                    )
                )
        else:
            _NowAnserList = self._getNowAnserList();
            _lenNowAnserList = len(_NowAnserList);
            if _lenNowAnserList <4:
                self.result =  TemplateSendMessage(
                    alt_text = self._tList[0][1],
                    template = ButtonsTemplate(
                        label= self._tList[0][1] ,
                        text  ='請再回答'+str(4 - _lenNowAnserList)+'個問題，您目前答案\n'+ '\n'.join([ (str(int(i['q'])+1) +':' +i['a']) for i in _NowAnserList]), 
                        actions=[ self._actionList[x] for x in range(4) if x not in [ int(i['q']) for i in _NowAnserList]]
                    )
                )
            elif _lenNowAnserList == 4:
                 self.result =  TemplateSendMessage(
                    alt_text = self._tList[0][1],
                    template = ButtonsTemplate(
                        label= self._tList[0][1] ,
                        text  ='以上問題都已作答完畢，您目前答案\n'+ '\n'.join([ (str(int(i['q'])+1) +':' +i['a']) for i in _NowAnserList]), 
                        actions=[ 
                            MessageTemplateAction(
                                label=  self._tList[4][0],
                                text = self._tList[4][1]
                                )
                            ]
                    )
                ) 
    
    #選擇地區溫度...
    def _test_q_temp(self): 
        _isTemp = False;
        #app.logger.error("Request _test_q_temp: " + self.msg)
        if self.msg == self._tList[6][1]:  
            #題目選項  
            self.result = TemplateSendMessage(
                alt_text = self._tList[6][1], 
                template = ButtonsTemplate(
                    title = self._tList[6][1],
                    text = '\n當地天氣也會影響蛋的新鮮度',
                    actions=[
                        MessageTemplateAction(
                            label =self._tList[6][2],
                            text = self._tList[6][3],
                        ),
                        MessageTemplateAction(
                            label =self._tList[6][4],
                            text = self._tList[6][5],
                        ),
                        MessageTemplateAction(
                            label =self._tList[6][6],
                            text = self._tList[6][7],
                        ) 
                    ]
                )
            )
        elif self.msg == self._tList[6][3] :
            #app.logger.error("Request _tList[6][3]: " + self.msg)
            #我在北部  #我在中部  #我在南部
            _isTemp = True;
        elif self.msg == self._tList[6][5] :
            #app.logger.error("Request _tList[6][5]: " + self.msg)
            #我在北部  #我在中部  #我在南部
            _isTemp = True;
        elif self.msg == self._tList[6][7]:
            #app.logger.error("Request _tList[6][7]: " + self.msg)
            #我在北部  #我在中部  #我在南部
            _isTemp = True;
        if _isTemp:
            #app.logger.error("Request _test_getNowAnserList: " + self.msg)
            self._test_getNowAnserList(0);
            pass
    
        pass
    
    #新鮮度
    def _test_q_days(self):
        self.isThisFun = True;
        self._test_getNowAnserList(1);
         
        pass
    
    #是否為洗選蛋...
    def _test_q_wash_egg(self):
        _isTemp = False;
        if self.msg == self._tList[5][1]:  
            #題目選項  
            self.result = TemplateSendMessage(
                alt_text = self._tList[2][1], 
                template = ButtonsTemplate(
                    title = self._tList[2][1],
                    text = '\n傳統市場通常非洗選蛋，則大賣場、超商、量販店為洗選蛋',
                    actions=[
                        MessageTemplateAction(
                            label =self._tList[2][2],
                            text = self._tList[2][3],
                        ),
                        MessageTemplateAction(
                            label =self._tList[2][4],
                            text = self._tList[2][5],
                        ) 
                    ]
                )
            )
        elif self.msg == self._tList[2][3]:
            #是洗選雞蛋  #不是洗選蛋
            _isTemp = True;
        elif self.msg == self._tList[2][5]:
            #是洗選雞蛋  #不是洗選蛋
            _isTemp = True;
        if _isTemp:
            self._test_getNowAnserList(2);
            pass
 
        pass
    
    #儲存環境
    def _test_q_store(self):
        _isTemp = False;
        if self.msg == self._tList[5][2]:
             #題目選項  
            self.result = TemplateSendMessage(
                alt_text = self._tList[3][1] , 
                #在不支援按鈕的裝置上會顯示的文字 通常是電腦
                template = ButtonsTemplate(
                    text = self._tList[3][0],
                    actions=[
                        MessageTemplateAction(
                            label = self._tList[3][3],
                            text = self._tList[3][4]
                        ),
                        MessageTemplateAction(
                            label = self._tList[3][5],
                            text = self._tList[3][6]
                        ) 
                    ]
                )
            )
        elif self.msg == self._tList[3][4] :
            #冰箱  #室溫
            _isTemp = True;
        elif self.msg == self._tList[3][6]:
            #冰箱  #室溫
            _isTemp = True;
        if _isTemp:
            self._test_getNowAnserList(3);
            pass     
        pass
    
    #查看測試剩下題目數
    def _test_getNowAnserList(self,pNowRow):
        if pNowRow not in [ int(i['q']) for i in self._getNowAnserList()]:
            _tempList.append({'q': str(pNowRow), 'a': self.msg});
        else:
            for i in _tempList:
                if int(i['q']) == pNowRow:
                    i['a'] = self.msg;
        self._test_q_item();#檢查剩下幾題

    #取得目前題數
    def _getNowAnserList(self):
        return _tempList;
    #看雞蛋測驗結果
    def _test_q_result(self):
        if self.msg == self._tList[5][3]:
            #題目選項  
            self.result =  TextSendMessage(text = "尚未連接WS!無法獲得結果") 
        pass
    
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    _reply_token = event.reply_token #event.reply_token
    data = WIKI_EGG(event.message.text, event.source.user_id); #選擇使用者回覆結果
    if not data.isThisNotReturn: #確定回傳內容
        line_bot_api.reply_message(_reply_token,data.result) #回傳內容給使用者
    return 0;   

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

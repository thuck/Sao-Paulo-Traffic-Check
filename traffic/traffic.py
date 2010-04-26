# -*- coding: utf-8 -*-
import urllib2
import re
import time
import threading
import thread
import wx

class Traffic(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.info = '"hora"|"tamanhoTotal"|"lentidao"|"percentualLentidao"|"tendencia"|"CentroLentidao"|"CentroTendencia"|"LesteLentidao"|"LesteTendencia"|"NorteLentidao"|"NorteTendencia"|"OesteLentidao"|"OesteTendencia"|"SulLentidao"|"SulTendencia"'
        self.search = re.compile(self.info).search
        self.stop = False
       
        self.sao_paulo = {'hora':'',
                    'tamanhoTotal':'',
                    'lentidao':'',
                    'percentualLentidao':'',
                    'tendencia':'',
                    'CentroLentidao':'',
                    'CentroTendencia':'',
                    'LesteLentidao':'',
                    'LesteTendencia':'',
                    'NorteLentidao':'',
                    'NorteTendencia':'',
                    'OesteLentidao':'',
                    'OesteTendencia':'',
                    'SulLentidao':'',
                    'SulTendencia':''}

    def retrieve_traffic_info(self):
        try:
            cet = urllib2.urlopen('http://cetsp1.cetsp.com.br/monitransmapa/agora/')
            filtred = filter(self.search, cet)
            cet.close()

            for line in filtred:
                id_ = line.split('"')[1]
                info = line.split('"')[-2:]
                if 'dados' in info[0] or 'lentidao' in info[0] or 'hora' in info[0]:
                    info = info[-1].strip().replace('</b></div>','').replace('><b>','').replace('</div>','').replace('>','')
                else:
                    info = info[-2]
                    
                self.sao_paulo[id_] = info

        except (urllib2.HTTPError, urllib2.URLError):
            pass

    def run(self):
        flag = time.time()
        while self.stop is False:
            tmp_time = time.time()
            if tmp_time - flag > 30:
                flag = tmp_time
                self.retrieve_traffic_info()
                for i,j in self.sao_paulo.items():
                    print i,j
            time.sleep(0.5)

class MainWindow(wx.Frame):
    def __init__(self, parent, title, traffic):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        self.traffic = traffic
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.hour = wx.StaticText(self, label="Hour:%(hour)s" % (self.traffic.hour), pos=(10, 30))
        self.Show(True)
        
    def on_exit(self, e):
        self.traffic.stop = True
        self.Destroy()


if __name__ == '__main__':
    traffic = Traffic()
    traffic.start()
    app = wx.App(False)
    window = MainWindow(None, 'São Paulo', traffic)
    app.MainLoop()

    




import win32com.client as win32

class SendMail:
    """调用Outlook发送邮件"""
    def __init__(self):
        self.outlook = win32.Dispatch("outlook.Application")
        self.mail = self.outlook.CreateItem(0)
    def send_mail(self):
        # addressee = 'fanhai@inovance.com'+';'+'lihaoC@inovance.com'   #发送多个收件人以分号分隔，中间用加号连接；实例：'@'+';'+'@'
        addressee = 'yangqunwu@inovance.com'
        # cc = ''
        self.mail.SentOnBehalfOfName = "yangqunwu@inovance.com"       # 发件人（邮箱或账号）
        self.mail.To = addressee              # 收件人
        # self.mail.CC = cc        # 抄送人
        self.mail.Subject = "测试发送邮件"           # 邮件主题

        self.mail.BodyFormat = 2            # 2表示用Html format，可调整格式
        # HTMLBody插入图片：先把要插入的图片当做一个附件添加，然后在HtmlBody中调用这个图片
        self.mail.Attachments.Add(r"C:\Users\Administrator\Pictures\Camera Roll\共产党宣言.png")    # 添加附件
        self.mail.HtmlBody = """测试添加附件<body>
        <div><img src="共产党宣言.png"></div>
        </body>
        """            # 邮件正文
        # self.mail.HtmlBody = '测试添加附件'
        self.mail.Attachments.Add(r"C:\Users\Administrator\Pictures\Camera Roll\共产党宣言.png")    # 添加正常的附件

        # self.mail.Display()        # 显示发送邮件界面
        self.mail.Send()        # 发送

if __name__ == '__main__':
    SendMail().send_mail()
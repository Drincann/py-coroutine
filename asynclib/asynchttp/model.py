class Response:

    # 接收响应报文
    def __init__(self, res):
        self.res = res
        self.agreement = ""  # 协议
        self.edition = ""  # 版本号
        self.status_code = ""  # 响应状态码
        self.ok = ""  # 响应状态码的描述
        self.headers = dict()  # 消息头
        self.res_text = ""  # 实体内容
        self.division()

    # 分割响应报文
    def division(self):

        num = 0
        lines = self.res.splitlines()
        # 以下为响应行的属性获取：
        # 协议

        line = lines[num].split("/")
        num += 1
        self.agreement = line[0]

        # 版本号

        line = line[1].split(" ")
        self.edition = line[0]

        # 响应状态码

        self.status_code = line[1]

        # 响应状态码的描述

        self.ok = line[2]

        # -------------------------------------------------
        # 以下为消息头的获取：

        for line in lines[num:]:
            num += 1
            if line == "":
                break
            li = line.split(": ")
            self.headers[li[0]] = li[1]

        # -------------------------------------------------------
        # 以下为实体内容的获取：

        for x in lines[num:]:
            self.res_text += x + "\n"
        self.res_text = self.res_text.strip("\n")



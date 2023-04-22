class HttpResponse:
    def __init__(self, rawResponse):
        self.rawResponse = rawResponse
        self.statusCode, self.headers, self.body = self.parseResponse()

    def parseResponse(self):
        lines = self.rawResponse.split('\r\n')

        # parse response line
        responseLine = lines[0].split(' ') if lines else []
        statusCode = int(responseLine[1]) if len(responseLine) > 1 else None

        # parse headers
        headers = {}
        for line in lines[1:]:
            if line == '':
                break
            parts = line.split(': ')
            if len(parts) == 2:
                key, value = parts
                headers[key] = value

        # parse body
        bodyIndex = lines.index('') if '' in lines else len(lines)
        body = '\r\n'.join(lines[bodyIndex+1:])

        return statusCode, headers, body

    def __str__(self):
        contentType = self.headers.get('Content-Type', 'N/A')
        # 删除响应体中的换行符并截取前 20 个字符
        bodyPreview = self.body.replace('\r\n', ' ').replace('\n', ' ')
        bodyPreview = bodyPreview[:20] + \
            '...' if len(bodyPreview) > 20 else bodyPreview
        return f"<HttpResponse, [Status: {self.statusCode}], [Content-Type: {contentType}], [Body Preview: {bodyPreview}]>"

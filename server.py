from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup
import PyPDF2
from summarize import summarize
import requests
import pdfx

app = FlaskAPI(__name__)
CORS(app)


###################### FLASK APIs ###############################################


class InvalidUsage(Exception):
    def __init__(self, message):
        super(InvalidUsage, self).__init__()
        self.message = message



@app.route("/sampleGetRequest", methods=['GET'])
def get_request():

    if request.method == 'GET':
        sample_data = request.args.get('data')
        
        modified_data = sample_data + " modify kar diya."

        resp = {"modified_data": modified_data}

        return resp, status.HTTP_200_OK


@app.route("/loginUser", methods=['POST'])
def loginUser_request():
    if request.method == 'POST':

        usr = request.data.get("username")
        pwd = request.data.get("password")
    if(usr=="admin" and pwd=="12345"):
        some_data = "Success"
        resp = {"response": some_data}
        return resp, status.HTTP_200_OK
    else:
        some_data = "Failed"
        resp = {"response": some_data}
        return resp, status.HTTP_200_OK


@app.route("/processData", methods=['POST'])
def process_request():
    if request.method == 'POST':
        url = request.data.get("url_field")
        #print(url)
        key = request.data.get("keywords")
        key = key[1:-1].split(",")
        keywords=[]
        for k in key:
            keywords.append(k[1:-1])
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        categories = ['new act', 'new rule', 'new regulation', 'notification', 'circular', 'press release',
                      'scheme', 'order', 'ordinance', 'amendment', 'resolution', 'bill', 'report', 'guideline',
                      'direction', 'clarification', 'master direction','revised']
        cat_map = dict()

        for k in keywords:
            india_links = lambda tag: (getattr(tag, 'name', None) == 'a' and
                                       'href' in tag.attrs and
                                       k in tag.get_text().lower())
            results = soup.find_all(india_links)
            extracted = []
            for i in results:
                p = i.get('href')
                i.find('title')
                l=[]
                l.append(i.contents[0])
                l.append(p)
                extracted.append(l)

            for z in extracted:
                flag = 0
                for cat in categories:

                    if cat in z[0].lower():

                        if cat in cat_map:

                            cat_map[cat].append(z)
                            flag = 1
                            break
                        else:
                            cat_map[cat] = [z]
                            flag = 1
                            break
                if flag == 0:
                    if 'others' in cat_map:
                        cat_map['others'].append(z)
                        flag = 1

                    else:
                        cat_map['others'] = [z]
        absUrl = 'http://www.sebi.gov.in/'
        for k, v in cat_map.items():
            for q in range (len(v)):
                url = v[q][1]
                
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")

                for i in soup.find_all('iframe'):
                    innerLinks = i.get('src')
                    pdfLink = absUrl + innerLinks[28:]
                    pdfLink = str(pdfLink)
                    print (pdfLink)
                # url = 'http://www.sebi.gov.in/web/?file=../../../sebi_data/attachdocs/nov-2017/1509707086156.pdf'
                    url = pdfLink
                # writer = PdfFileWriter()
                    pdf = pdfx.PDFx(url)
                # metadata = pdf.get_metadata()

                    references_dict = pdf.get_references_as_dict()
                    metadata = pdf.get_metadata()
                    text = pdf.get_text()
                    z = summarize(text, sentence_count=4, language='english')
                    v[q].append(z)
                    v[q].append(references_dict)
                    v[q].append(metadata)

        return cat_map, status.HTTP_200_OK


# @app.route("/pdfProcess", methods=['POST'])
# def pdf_request():
#     if request.method == 'POST':
#         pdf_url = request.data.get("pdf_url")
#         pdfFileObj = open(pdf_url, 'rb')  # 'rb' for read binary mode
#         pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#         pageObj = pdfReader.getPage(1)
#         text = pageObj.extractText()
#         z = summarize(text, sentence_count=10, language='english')
#         print(z)
#
#         resp = {"response": some_data}
#
#         return resp, status.HTTP_200_OK


@app.route("/samplePostRequest", methods=['POST'])
def post_request():

    if request.method == 'POST':
        #Ye saara data body me send kiya hai.
        some_data = request.data.get("username")
        another_data = request.data.get("password")

        """
        Yahan data ko process karo.
        """
        print(some_data)
        print(another_data)

        resp = {"response": some_data}
        
        return resp, status.HTTP_200_OK



#Error handling
@app.errorhandler(404)
def page_not_found(e):
    return {"message": "Enter the correct url for endpoint."}, 404

@app.errorhandler(405)
def page_not_found(e):
    return {"message": "Type of http request is incorrect."}, 405

@app.errorhandler(500)
def page_not_found(e):
    return {"message": "Internal server error encountered. Pass the parameters in correct format."}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
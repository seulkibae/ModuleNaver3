# <Summary>
# 모듈 프로젝트 3조 - 김민지(98), 김진수, 배슬기, 이동용
# NAVER 검색 API를 이용해 카테고리별 데이터 정제 후 파일 저장
import urllib.request
import datetime
import json
import pandas as pd
import requests

# <Summary>
# NAVER API 호출, 클라이언트 연결
# 크롤링 코드 작성자 - 이동용, 배슬기
# <Remarks>
# 클라이언트 id & secret 입력(검색허용량 25,000회/일)
# </Remakrs>
def GetNaverSearchResult(searchNode, searchText, pageStart, display):
    baseurl = "https://openapi.naver.com/v1/search/"
    nodedata = "%s.json" % searchNode
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(searchText),
                                                        pageStart ,
                                                        display)
    url = baseurl + nodedata + parameters
    
    searchReq = requests.get (url=url, 
                                    headers={"X-Naver-Client-Id" : "i0rOFq7sJon3SVankcLB",
                                            "X-Naver-Client-Secret" :"iNHdUrvzYV"})
    return searchReq.json()

# <Summary>
# 데이터 정제 - 김민지
# 카테고리 별(news) 필드값 명명
def GetNewsDateChange(data, jsonResult):
    resultTitle = data['title'].replace("<b>", "*").replace("</b>", "*").replace("&quot;", "\"")
    resultDesc = data['description'].replace("<b>", "*").replace("</b>", "*").replace("&quot;", "\"")
    resultOrgLink = data['originallink']
    naverLink = data['link']
    changeDate = datetime.datetime.strptime(data['pubDate'], 
                            '%a, %d %b %Y %H:%M:%S +0900')
    changeDateResult = changeDate.strftime('%Y-%m-%d  %H:%M:%S')
    jsonResult.append({ '제목':resultTitle, 
                        '내용': resultDesc,
                        'link': naverLink,
                        'originallink': resultOrgLink,
                        '날짜': changeDateResult})
    return 

def GetBlogDateChange(data, jsonResult):
    resultTitle = data['title'].replace("<b>", "*").replace("</b>", "*").replace("&quot;", "\"")
    resultDesc = data['description'].replace("<b>", "*").replace("</b>", "*").replace("&quot;", "\"")
    resultBlogLink = data['bloggerlink']
    naverLink = data['link']
    resultDate = data['postdate']
    jsonResult.append({ '제목': resultTitle, 
                        '내용': resultDesc,
                        'link': naverLink,
                        'bloggerlink': resultBlogLink,
                        '날짜': resultDate})
    return 

def GetCafeDateChange(data, jsonResult):
    resultTitle = data['title'].replace("<b>", "*").replace("</b>", "*").replace("&quot;", "\"")
    resultDesc = data['description'].replace("<b>", "*").replace("</b>", "*").replace("&quot;", "\"")
    resultCafeurl = data['cafeurl']
    naverLink = data['link']
    jsonResult.append({ '제목': resultTitle, 
                        '내용': resultDesc,
                        'link': naverLink,
                        'cafeurl': resultCafeurl})
    return 

# <Summary>
# 카테고리 별 데이터 정제 후 .json & .xlsx로 저장
# 메인코드 작성자 - 김진수, 이동용
# <Remarks>
# 최대 100개의 데이터만 호출 가능
def main():
    sText = '메타버스'
    dCount = 100
    
    jsonDataResult1 = []
    jsonDataResult2 = []
    jsonDataResult3 = []

    jsonSearchResult1 = {}
    jsonSearchResult2 = {}  
    jsonSearchResult3 = {}

    jsonSearchResult1 = GetNaverSearchResult('news', sText, 1, dCount)
    jsonSearchResult2 = GetNaverSearchResult('blog', sText, 1, dCount)
    jsonSearchResult3 = GetNaverSearchResult('cafearticle', sText, 1, dCount)

    for data in jsonSearchResult1['items']:
             GetNewsDateChange(data, jsonDataResult1)
    for data in jsonSearchResult2['items']:
             GetBlogDateChange(data, jsonDataResult2)
    for data in jsonSearchResult3['items']:
             GetCafeDateChange(data, jsonDataResult3)

    # <Summary>
    # 데이터 정렬 및 파일 저장
    # 코드작성자 - 배슬기
    with open('메타버스.json', 'w', encoding= 'utf-8') as filedata:
       # if 'items' in jsonSearchResult1.keys():
        # tempData = pd.DataFrame(jsonSearchResult['items'][0]['title']['pubDate']['description']['link']['originallink'])
        News = pd.DataFrame(jsonDataResult1, columns= ['제목', '내용','날짜', 'link', 'originallink'])
        Blog = pd.DataFrame(jsonDataResult2, columns= ['제목', '내용','날짜', 'link'])
        Cafe = pd.DataFrame(jsonDataResult3, columns= ['제목', '내용', 'link'])

        temp = News.to_json(force_ascii=False, indent=4) + Blog.to_json(force_ascii=False, indent=4) + Cafe.to_json(force_ascii=False, indent=4) 
        filedata.write(temp)

    # 카테고리별 엑셀 시트별 저장
    # 코드 작성자 - 김민지
    with pd.ExcelWriter('메타버스.xlsx') as writer: 
        News.to_excel(writer, sheet_name = 'News')
        Blog.to_excel(writer, sheet_name = 'Blog')
        Cafe.to_excel(writer, sheet_name = 'Cafe')   

# <Summary>
# Main
if __name__ == '__main__':
    main() 


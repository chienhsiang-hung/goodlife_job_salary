import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd


def goodjob_life(url, pages):
    '''
    Examples:
        goodjob_life('https://www.goodjob.life/companies/%E5%8F%B0%E7%81%A3%E5%BE%AE%E8%BB%9F%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/salary-work-times', 2)
        goodjob_life('https://www.goodjob.life/companies/%E8%B6%A8%E5%8B%A2%E7%A7%91%E6%8A%80%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/salary-work-times', 11)
    '''
    data = []
    for i in range(1, pages+1):
        page = requests.get(url+f'?p={i}')
        soup = BeautifulSoup(page.content, 'html.parser')
        salary_table = soup.find_all('table')[0]
        rows = salary_table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            salary_info = [cell.text for cell in cells]
            data.append(salary_info)
    columns = ['職稱', '職務型態', '表訂 / 實際工時', '一週總工時', '加班頻率', '業界工作經歷', '薪資', '時薪', '參考時間']
    return pd.DataFrame(data, columns=columns)


if __name__ == '__main__':
    url, pages = sys.argv[1], sys.argv[2]
    print(f'URL={url}')
    print(f'Pages={pages}, Type={type(pages)}')

    DF = goodjob_life(url, int(pages))
    cpn = sys.argv[3]
    DF.to_csv(f'salary/{cpn}.csv', index=False, encoding='utf_8_sig')
    print(DF)
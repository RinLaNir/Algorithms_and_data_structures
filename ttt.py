import requests, wget
import pandas as pd
df = pd.read_excel("C:\Program1\Python\Free+English+textbooks.xlsx")
for index, row in df.iterrows():
        file_name = f"{row.loc['Book Title']}_{row.loc['Edition']}".replace('/','-').replace(':','-')
        url = f"{row.loc['OpenURL']}"
        r = requests.get(url)
        download_url = f"{r.url.replace('book','content/pdf')}.pdf"
        wget.download(download_url, f"C:/Program1/Python/download/{file_name}.pdf")
        print(f"downloading {file_name}.pdf Complete ....")

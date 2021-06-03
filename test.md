# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 09:48:40 2021

@author: 210603
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tushare as ts #示範數據

pd.set_option('display.max_columns', 100) # 設置顯示數據的最大列數，防止出現省略號…，導致數據顯示不全
pd.set_option('expand_frame_repr', False) # 當列太多時不自動換行

pro = ts.pro_api() 
df = pro.daily(ts_code='600000.SH', start_date='20190401', end_date='20190430')


## 查看數據
#.head() 查看前n行數據，默認值是5
df.head()
#.tail() 查看後n行數據，默認值是5
df.tail()
#.shape 查看數據維數
df.shape
#.columns 查看所有列名
df.columns
#.info() 查看索引、數據類型和內存信息
df.info()
#.describe() 查看每列數據的基本統計值，包括計數值、均值、標準差、最小最大值、1/4、1/2、3/4分位數。
df.describe()
#.value_counts() 查看Series對象的唯一值和計數值
df['close'].value_counts(dropna=False)


## 用圖看數據
#直方圖
df['close'].plot(kind='hist', rot=0) 
df.hist(column='initial_cost')
plt.show()
#箱型圖
df.boxplot(column='close', by='ts_code', rot=0) plt.show()
#散點圖
df.plot(kind='scatter', x='close', y='pre_close', rot=0) 
plt.show()

##清洗數據
"""
【header】默認header=0，即將文件中的0行作為列名和數據的開頭，但有時候0行的數據是無關的，
我們想跳過0行，讓1行作為數據的開頭，可以通過將header設置為1來實現。

【usecols】根據列的位置或名字，如[0,1,2]或[『a』, 『b』, 『c』]，選出特定的列。

【nrows】要導入的數據行數，在數據量很大、但只想導入其中一部分時使用。

"""
subset_columns = ['Job #', 'Doc #', 'Borough', 'Initial Cost', 'Total Est. Fee'] 
df = pd.read_csv('文件路徑', nrows=100, usecols=subset_columns) 
df.head()
#.drop()刪除某些行和列
to_drop = ['Job #', 'Doc #'] 
df.drop(to_drop, axis=1, inplace=True) 
#.rename()重新命名列
new_names = {'Borough': '區', 'Initial Cost': '初始成本', 'Total Est. Fee': '總附加費用'} 
df.rename(columns=new_names, inplace=True)
#.set_index()重新設置索引
df.set_index('區', inplace=True)



##用字符串操作規範列
"""字符串str操作是非常實用的，因為列中總是會包含不必要的字符，常用的方法如下："""

# str.lower() 是把大寫轉換成小寫
# str.upper() 是把小寫轉換成大寫，將示例中用大寫字母表示的索引轉換成小寫
df.index = df.index.str.lower()
# str.capitalize() 設置首字母大寫
df.index = df.index.str.capitalize()
#str.replace('$', '') 替換特定字符。這裡把列中的美元符號$去掉，替換成空字符。
#str.strip() 去除字符串中的頭尾空格、以及\n \t
"""
df['初始成本'] = ' ' + df['初始成本'] 
df['初始成本'][0] 
Out[28]: ' 2000.00' 
df['初始成本'] = df['初始成本'].str.strip() 
df['初始成本'][0] 
Out[29]: '2000.00'
"""
#str.split('x') 使用字符串中的'x'字符作為分隔符，將字符串分隔成列表。這裡將列中的值以'.'進行分割，
df['總附加費用'] = df['總附加費用'].str.split('.')
#str.get() 選取列表中某個位置的值。
"""
接著上面分割後的結果，我們用str.get(0)取出列表中前一個位置的數值，生成新的一列「總附加費用_整數」，
即取出金額中的整數部分。
df['總附加費用_整數'] = df['總附加費用'].str.get(0) 
df.head() 
Out[31]: 
    初始成本 總附加費用 總附加費用_整數 區 
    Queens 2000.00 [100, 00] 100 
    Queens 15000.00 [151, 50] 151 
    Brooklyn 44726.00 [234, 00] 234 
    Queens 0.00 [243, 00] 243 
    Queens 105000.00 [1275, 60] 1275
"""
#str.contains() 判斷是否存在某個字符，返回的是布爾值。這裡判斷一下"總附加費用_整數"列中是否包含字符'0'。
df['總附加費用_整數'].str.contains('0')
"""
Out[33]: 
    區 
    Queens True 
    Queens False 
    Brooklyn False 
    Queens False 
    Queens False
"""
#str.find()檢測字符串中是否包含子字符串str，如果是，則返回該子字符串開始位置的索引值。
#示例中的'0'字符最開始出現的位置是1。
"""df['總附加費用_整數'][0] 
Out[13]: '100' 
df['總附加費用_整數'][0].find('0')
Out[14]: 1
"""

##組合整理
"""如果condition條件為真，則執行then，否則執行else。
這裡的condition條件可以是一個類數組的對象，也可以是一個布爾表達式，
我們也可以利用np.where函數嵌套多個條件進行矢量化計算和判斷。

下面的這個實例，就是同時嵌套兩個條件解決上面提到的那兩個字符串問題。
思路是，如果字符串裡面包含'London'，就用'London'代替，
這樣可以去除其他冗餘信息，否則，如果字符串裡面包含'Oxford'，則用'Oxford'代替，
同時如果字符串裡面包含符號'-'，則用空格代替。
"""
#np.where(condition, then, else)
pub = df['Place of Publication'] 
london = pub.str.contains('London') 
oxford = pub.str.contains('Oxford') 
df['Place of Publication'] = np.where(london, 'London', np.where(oxford, 'Oxford', pub.str.replace('-', ' ')))


## 用函數規範化
"""
在某些情況下，數據不規範的情況並不局限於某一列，而是更廣泛地分布在整個表格中。
因此，自定義函數並應用於整個表格中的每個元素會更加高效。
用applymap()方法可以實現這個功能，
它類似於內置的map()函數，只不過它是將函數應用於整個表格中的所有元素。
"""
university_towns = [] 
with open('D:/code/tushare interpret and tech team
          /python-data-cleaning-master/Datasets/university_towns.txt')
          as file: 
              for line in file: 
                  if '[edit]' in line: 
              # 該行有[edit] state = line # 將改行信息賦值給「州」，記住這個「州」，
              直到找到下一個為止 
                  else: university_towns.append((state, line)) 
                  # 否則，改行為城市信息，並且它們都屬於上面的「州」 
university_towns[:5]

#pd.DataFrame()方法將這個列錶轉換成一個DataFrame，
#並將列設置為"State"和"RegionName"。
#Pandas將接受列表中的每個元素，並將元組左邊的值傳入"State"列，右邊的值傳入"RegionName"列。
"""
towns_df = pd.DataFrame(university_towns, columns=['State', 'RegionName'])
towns_df.head()
Out[45]: 
 State RegionName
0 Alabama[edit]\n Auburn (Auburn University)[1]\n
1 Alabama[edit]\n Florence (University of North Alabama)\n
2 Alabama[edit]\n Jacksonville (Jacksonville State University)[2]\n
3 Alabama[edit]\n Livingston (University of West Alabama)[2]\n
4 Alabama[edit]\n Montevallo (University of Montevallo)[2]\n


接下來就要對列中的字符串進行整理，"State"列中的有效信息是州名，
"RegionName"列中的有效信息是城市名，其他的字符都可以刪掉。
當然，除了用之前提到的利用循環和.str()方法相結合的方式進行操作，
我們還可以選擇用applymap()方法，它會將傳入的函數作用於整個DataFrame所有行列中的每個元素。

先定義函數get_citystate(item)，功能是只提取元素中的有效信息。

def get_citystate(item):
 if ' (' in item:
 return item[:item.find(' (')]
 elif '[' in item:
 return item[:item.find('[')]
 else:
 return item
然後，我們將這個函數傳入applymap()，並應用於towns_df，結果如下：

towns_df = towns_df.applymap(get_citystate)
towns_df.head()
Out[48]: 
 State RegionName
0 Alabama Auburn
1 Alabama Florence
2 Alabama Jacksonville
3 Alabama Livingston
4 Alabama Montevallo
現在towns_df表格看起來是不是乾淨多了！
"""

## .drop_duplicates()刪除重複數據
tracks_no_duplicates = tracks.drop_duplicates()

原文網址：https://kknews.cc/code/bmkap36.html

## fillna()缺失值
"""以"Ozone"列為例，我們可以調用fillna()函數，用該列的均值.mean()填充NaN值。"""
oz_mean = airquality.Ozone.mean() 
airquality['Ozone'] = airquality['Ozone'].fillna(oz_mean)

原文網址：https://kknews.cc/code/bmkap36.html

https://chriskang028.medium.com/datacamp-cleaning-data-in-python-%E5%A6%82%E4%BD%95%E7%B0%A1%E5%96%AE%E4%B8%8A%E6%89%8B%E8%B3%87%E6%96%99%E6%B8%85%E6%B4%97-866c60a5819f




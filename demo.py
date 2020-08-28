import  pandas as pd
import json
import pymysql
import datetime,time
import os
import xlrd


path = './file/'
all_file = os.listdir(path)

for name in all_file:
    if name.startswith('com.') or name.startswith('surface') or name.startswith('system'):
        #找到符合条件的文件名
        new_name = os.path.splitext(name)[0]
        #文件路径
        new_path = path+new_name+'.xlsx'
        #打开相应的文件
        workbook = xlrd.open_workbook(new_path)
        #文件所包含的所有sheetname
        sheetname = workbook.sheet_names()
        #sheetname的个数
        num = workbook.nsheets
        # 写入数据库
        conn = pymysql.connect(host='10.16.31.77', user='root', password='AutoTest', port=3306)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        for j in range(1, num):
            data = pd.read_excel(new_path,sheet_name=sheetname[j])
            package_id = 5
            crash = int(data['value1'][0])
            dalvik_max = int(data['value2'][0])
            dalvik_min = int(data['value2'][1])
            dalvik_avg = int(data['value2'][2])
            native_max = int(data['value2'][3])
            native_min = int(data['value2'][4])
            native_avg = int(data['value2'][5])
            cpu_max = int(data['value2'][6])
            cpu_min = int(data['value2'][7])
            cpu_avg = int(data['value2'][8])
            tstr = '2020-'+sheetname[j]+' 00:00:00'

            try:
                time.strptime(tstr, "%Y-%m-%d %H:%M:%S")
                create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(tstr, "%Y-%m-%d %H:%M:%S")))
            except Exception:
                # traceback.print_exc()
                continue

            print(create_time)

            sql = "insert into chart_demo.data " \
                  "(package_id,dalvik_max,dalvik_min,dalvik_avg,native_max,native_min,native_avg,cpu_max,cpu_min,cpu_avg,crash,create_time) " \
                  "values('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%s')"\
                  %(package_id,dalvik_max,dalvik_min,dalvik_avg,native_max,native_min,native_avg,cpu_max,cpu_min,cpu_avg,crash,create_time)
            try:
                # values = (dalvik_max,dalvik_min,dalvik_avg,native_max,native_min,native_avg,cpu_max,cpu_min,cpu_avg,crash)
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()

        cursor.close()
        conn.close()

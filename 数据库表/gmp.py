from xlsx2sql import XlsxTool,Xlsx2sql
tool = XlsxTool()
table_header_type = ['varchar(255) not null','varchar(255) ','varchar(255)','varchar(255)','varchar(30)','varchar(30)','data','data','data','data','varchar(100)','varchar(100)']
release = Xlsx2sql(tool)
release.generate(r'./gmp.xlsx',table_header_type,"id",r'./gmp.sql')
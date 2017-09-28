from xlsx2sql import XlsxTool,Xlsx2sql
tool = XlsxTool()
table_header_type = ['varchar(255) not null','varchar(255) ','varchar(255)','varchar(255)','varchar(255)','varchar(255)','varchar(255) ','varchar(255) ','varchar(255)','varchar(255) ','varchar(255) ','varchar(255)','date ','date ','varchar(255) ','varchar(255)','varchar(255) ','varchar(255) ','varchar(255)']
release = Xlsx2sql(tool)
release.generate(r'./medicine_company.xlsx',table_header_type,"id",r'./medicine_company.sql')
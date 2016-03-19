import multiprocessing
import xlrd

class ExcelReader(object):
    def open_excel_file(self,file_path):
        self.data = xlrd.open_workbook(file_path)
        self.table = self.data.sheets()[0]
        
    def getcol(self,index):
        return self.table.col_values(index)
    
    def getrow(self,index):
        return self.table.row_values(index)
    
    def getcol_length(self):
        return self.table.ncols
    
    def getrow_length(self):
        return self.table.nrows;
    
    def getContent_rowbyrow(self):
        for i in xrange(0,a.getrow_length()):
            yield a.getrow(i)

 
if __name__ == "__main__":
    a =  ExcelReader()
    a.open_excel_file("proxy.xlsx")
    for row in a.getContent_rowbyrow():
        for col in row:
            print col
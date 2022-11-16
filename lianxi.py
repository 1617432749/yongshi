student=[]
def mesiage(id, name,age, sex='男', className='03'):
    global student
    student = student + [id,name,age,sex,className]
def shuchu():
    print('id',student[0],'name',student[1],'age',student[2],'className',student[3],sep='|')
mesiage(2556661, '李明', 18)
shuchu()
from pony.orm import *
db = Database()
        #******************  连接mysql，将数据存到mysql表中
db.bind(provider='mysql',host="localhost",user="root",passwd="123456",db="vdtextdb")
#音频文字表
class VdText(db.Entity):
    num = PrimaryKey(int,auto=True)
    textstr = Required(str)
    lentext = Required(str)
# db.generate_mapping(create_tables=True)
#用户信息表
class UserBase(db.Entity):
    user_name = Required(str)
    pass_word = Required(str)
    notes = Required(str)

db.generate_mapping(create_tables=True)



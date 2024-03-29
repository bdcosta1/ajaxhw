#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
from datetime import datetime

db.define_table('boards',
                Field('name', 'text'),
                Field('fromDB', 'text', default=True),
                Field('board_creator', 'text'),
                Field('draft_id', 'text')
            )
db.define_table('post',
             Field('name', 'text'),
             Field('fromDB', 'text', default=True),
             Field('post_creator', 'text'), # To uniquely identify drafts and messages.
             Field('draft_id', 'text'),
             Field('board_table_id', 'reference boards'),
             Field('description', 'text'),
             Field('created_on', default=datetime.utcnow())
            )
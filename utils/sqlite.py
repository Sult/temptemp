import sqlite3
from collections import namedtuple


def connect():
    con = sqlite3.connect('data/dump')
    con.row_factory = sqlite3.Row
    return con
    

#only works with table IDs!
def get_sql(the_dict):
    keys = the_dict.keys()
    #get row by table field pk
    if keys == ["table", "pk", "field"]:
        return "SELECT * FROM %s WHERE %s=%d" % (the_dict["table"], the_dict["field"], the_dict["pk"])
    else:
        raise Exception("not implemented yet")


#get row object
def get_single_row(**kwargs):
    con = connect()
    with con:
        cur = con.cursor()
        try:
            cur.execute(get_sql(kwargs["kwargs"]))
            row = cur.fetchone()
        except:
            return None
        if row == None:
            return None
        else:
            return namedtuple('Temp', row.keys())(**row)
    



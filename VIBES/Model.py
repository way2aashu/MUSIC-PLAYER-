import cx_Oracle
import traceback
class Model:
    def __init__(self):
        self.song_dict={}
        self.db_status = True
        self.conn=None
        self.cur=None

        try:
           self.conn=cx_Oracle.connect("mouzikka/music@localhost")
           print("Connected successfully to DB.. ")
           print(self.conn)
           self.cur=self.conn.cursor()
           print(self.cur)
        except cx_Oracle.DatabaseError:
            print("DB Error",traceback.format_exc())


    def get_song_count(self):
        total_song=len(self.song_dict)
        return total_song


    def get_db_status(self):
        return self.db_status


    def close_db_connection(self):
        try:
           if(self.cur is not None):
               self.cur.close()
               print("Cursor Close")

           if(self.conn is not None):
               self.conn.close()
               print("Connection Close")
        except cx_Oracle.DatabaseError:
            print("DB Error", traceback.format_exc())

    def add_song(self, song_name, song_path):
        self.song_dict[song_name]=song_path
        print("song added",self.song_dict[song_name])


    def get_song_path(self,song_name):
        return self.song_dict[song_name]


    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print(self.song_dict)


    def search_song_in_favourites(self,song_name):
        self.cur.execute("Select song_name from myfavourites where song_name=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True

    def add_song_to_favourites(self, song_name,song_path):
        print("song name is", song_name)
        print("song path is", song_path)
        is_song_present=self.search_song_in_favourites(song_name)
        if(is_song_present==True):
            return "Song already present in your favourites"
        else:
            self.cur.execute("Select max(song_id) from myfavourites")
            last_song_id = self.cur.fetchone()[0]
            next_song_id = 1
            if last_song_id is not None:
                next_song_id = last_song_id + 1
            print("last song id:", last_song_id, "next song id:", next_song_id)
            self.cur.execute("insert into myfavourites values(:1,:2,:3)", (next_song_id, song_name,song_path))
            self.conn.commit()
            return "Song added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfavourites")
        songs_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            songs_present = True
        if songs_present == True:
    #        return True
            return "List populated from favourites"
        else:
            return "No songs present in your favourites"
    #        return False

    def remove_song_from_favourites(self, song_name):
        song_present=self.search_song_in_favourites(song_name)
        if(song_present):
           self.cur.execute("Delete from myfavourites where song_name=:1",(song_name,))
           self.conn.commit()
           self.song_dict.pop(song_name)
           return "song deleted from your favourite"
        else:
            return "song isnt present"
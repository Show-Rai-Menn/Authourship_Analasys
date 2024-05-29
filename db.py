import os
import sqlite3

conn = sqlite3.connect('memory.db', check_same_thread=False)  # Connect to 'memory.db' database
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                   original_name TEXT PRIMARY KEY,
                   Q_or_K TEXT, 
                   file_path TEXT
                )''')
conn.commit()

def upload(filename, kind, root_dir):

    file_path=os.path.join(root_dir, 'templates', filename)
    

    cursor.execute("INSERT OR IGNORE INTO files VALUES (?, ?)", (filename, file_path))
    conn.commit()  # Commit changes to the database

    print(f"File uploaded successfully! New name: {filename}")

def search(query):
    cursor.execute("SELECT original_name FROM files WHERE original_name LIKE ?", ('%' + query + '%',))
    file_data=cursor.fetchall()
    print(file_data)
    return file_data

def delete_file(filename):

    
    cursor.execute("DELETE FROM files WHERE original_name = ?", (filename,))
    conn.commit()  # Commit changes to the database

    print(f"File '{filename}' deleted.")


def search_all():  #すべてのファイルを取り出す関数
    cursor.execute("SELECT original_name FROM files")
    filename=cursor.fetchall()
    print(type(filename))
    return [name[0] for name in filename]
    
    



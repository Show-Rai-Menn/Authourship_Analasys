import os
import sqlite3

conn = sqlite3.connect('memory.db', check_same_thread=False)  # Connect to 'memory.db' database
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Q_files (
                   original_name TEXT PRIMARY KEY,
                   file_path TEXT
                )''')#Qのテーブル

cursor.execute('''CREATE TABLE IF NOT EXISTS K_files (
                   original_name TEXT PRIMARY KEY,
                   file_path TEXT
                )''')#Kのテーブル

conn.commit()

def upload(filename, kind, root_dir):
    try:
        file_path = os.path.join(root_dir, 'templates', filename)

        if kind == 'Q':
            cursor.execute("INSERT OR IGNORE INTO Q_files (original_name, file_path) VALUES (?, ?)", (filename, file_path))
        elif kind == 'K':
            cursor.execute("INSERT OR IGNORE INTO K_files (original_name, file_path) VALUES (?, ?)", (filename, file_path))
        else:
            print(f"Unknown kind: {kind}")
            return

        conn.commit()  # Commit changes to the database
        print(f"File uploaded successfully! New name: {filename}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def search(query):
    cursor.execute("SELECT original_name FROM files WHERE original_name LIKE ?", ('%' + query + '%',))
    file_data=cursor.fetchall()
    print(file_data)
    return file_data

def delete_file(filename):

    
    cursor.execute("DELETE FROM files WHERE original_name = ?", (filename,))
    conn.commit()  # Commit changes to the database

    print(f"File '{filename}' deleted.")


def search_allQ():  #すべてのQファイルを取り出す関数
    cursor.execute("SELECT original_name FROM Q_files")
    filenameQ=cursor.fetchall()
    new_fileQ = [(file[0], 'Q') for file in filenameQ]
    


    print(type(new_fileQ))
    return new_fileQ

def search_allK():
    cursor.execute("SELECT original_name FROM K_files")
    filenameK = cursor.fetchall()
    new_filesK = []
    print(filenameK)

    # ファイル名にK1, K2, ...と名付ける
    for index, (original_name,) in enumerate(filenameK, start=1):  # タプルのアンパック
        newname = f"K{index}"
        new_filesK.append((original_name, newname))

    print(type(new_filesK))  # デバッグ用
    return new_filesK
    
    



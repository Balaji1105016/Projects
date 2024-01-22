# pip install mysql-connector-python
# pip install google-api-python-client

# chan_ids = ['UCYejIJpDILRa1n8ooXgvhPA'] #-->UCYhtvdk5phE11JqJXdwYpSA-->DB Record
#             # 'UCY1kMZp36IQSyNx_9h4mpCg',
#             # 'UCIq3h8ijNSBId8rLgwcR53A', 'UCYejIJpDILRa1n8ooXgvhPA',
#             # 'UC9h2hiIb600WWP4IEfLADkA', 'UCYhtvdk5phE11JqJXdwYpSA',
#             # 'UC6_clxPYNS_BstewLKjyA9g', 'UCCP3zcy7l8KyBen7gAHsD6Q',
#             # 'UC9pqvfDuuTqOA2AVD10O-9A', 'UCebNNPdj1ND6ExPFIp9Qh1g'

import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus as pl
import pymysql

api_key = 'AIzaSyAYfwOFHkD04T-r7ZsH7RN_UnZCFjaa3zs'
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)


st.title("ALPHA-THE B😃T")
st.write("Note: ALPHA-THE B😃T Is A User-Friendly Web Application That Allows Users To Perform Data Scrapping By Using YouTube API And Data Migration And Will Provide Some Meaningful Insights About YouTube Data To Users Who Are Accessing This Application.")
# Login and Logout Section:
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
    
username = st.text_input("User Name")
password = st.text_input("Password",type = 'password')
if st.button("Login"):
    if username == "Balaji" and password == "Balaji@123":
        st.session_state.login_status = True
        st.success("Login Successful!")
    
    else:
        st.session_state.login_status = False
        st.error("Invalid Credentials. Please try again.")

if st.session_state.login_status:      
    logout = st.sidebar.button("Logout")
    if logout:
        if 'login_status' in st.session_state:
            st.session_state.login_status = False
            st.experimental_rerun()
                
    st.sidebar.header("Featues:")
    st.sidebar.subheader("""
                    
                    Easy To Interact\n 
                    Users Can Scrap Multiple Channels At A Time\n
                    Data Migration\n
                    Can Able To Get Some Meningfull Insights
                    
                    """)
    st.sidebar.header("Application Process Overview")
    st.sidebar.subheader("""
                         1. Setting Up A Streamlit App\n
                         2. Connecting To The YouTube API\n
                         3. Storing The Scrapped Data In Mongo DB\n
                         4. Migrating The Data To The SQL DB\n
                         5. Quering The SQL Data\n
                         6. Displaying The Data In The Streamlit APP\n
                         """)
    st.sidebar.header("Usefull Links")
    st.sidebar.subheader("Streamlit")
    st.sidebar.markdown("https://www.youtube.com/@streamlitofficial")
    st.sidebar.subheader("YouTube Data Importance")
    st.sidebar.markdown("https://www.youtube.com/watch?v=vJWaYMzpGjc")
    st.sidebar.subheader("How To Copy The Channel ID's From YouTube")
    # st.sidebar.markdown("https://www.youtube.com/watch?v=Pez9_tnkKVk")
    st.sidebar.markdown("https://www.youtube.com/watch?v=D12v4rTtiYM")
    st.sidebar.header("How To Get The API Key And How To Enable YouTube Data API V3 Service")
    st.sidebar.markdown("https://www.youtube.com/watch?v=pP4zvduVAqo")
    st.subheader(".........You Tube Data Harvesting & Data WareHousing........")
    st.subheader("Data Scrapping")
    
    # Data Scrapping Section
    chan_ids = st.text_input("Enter the channel ID:")
    unique_chan_ids = set(chan_ids.split(","))
    scraping_button = st.button("Scrape Data")

    if scraping_button:
        chan_result = []

        def get_c_data(unique_chan_ids):
            for chan_id in unique_chan_ids:
                req = youtube.channels().list(part="snippet, statistics, contentDetails", id=chan_id.strip())
                resp = req.execute()
                
                for i in range(len(resp['items'])):
                    c_data = {'Chan_id': resp['items'][i]['id'],
                        'Chan_name': resp['items'][i]['snippet']['title'],
                        'chan_published_At': resp['items'][i]['snippet']['publishedAt'],
                        'Chan_playlist_id': resp['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                        'Chan_des': resp['items'][i]['snippet']['description'],
                        'Sub_count': resp['items'][i]['statistics']['subscriberCount'],
                        'Chan_view_count': resp['items'][i]['statistics']['viewCount'],
                        'Total_video_count': resp['items'][i]['statistics']['videoCount']}
                    chan_result.append(c_data)  

            return chan_result
        
        
        channel_data = get_c_data(unique_chan_ids)
        st.subheader("Channel Information")
        st.dataframe(pd.DataFrame(channel_data))
        chan_df = pd.DataFrame(channel_data)
        playlist_ids = [chan['Chan_playlist_id'] for chan in channel_data]
        
        # Playlist Details
        vid = []
        for playlist_id in playlist_ids:
            pagetoken = None
            while True:
                req = youtube.playlistItems().list(part='id,status,snippet,contentDetails', playlistId=playlist_id, maxResults=10, pageToken=pagetoken)
                res = req.execute()

                for item in res.get('items', []):
                    playlist_info = {
                        'Chan_playlist_id': item['snippet']['playlistId'],
                        'video_id': item['snippet']['resourceId']['videoId']}
                    vid.append(playlist_info)

                pagetoken = res.get('nextPageToken')

                if not pagetoken:
                    break

        st.subheader("Playlist Details")
        st.dataframe(pd.DataFrame(vid))
        
        #Video Details:
        vid_data = []
        page_token = None
        while True:
            for playlist_info in vid:
                video_id = playlist_info['video_id']
                request = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id, maxResults=50, pageToken=page_token)
                response = request.execute()
                
                for j in response.get('items', []):
                    snip = j['snippet']
                    stat = j['statistics']
                    cont = j['contentDetails']

                    video_info = {
                        'video_id': j['id'],
                        'title': snip['title'],
                        'des': snip.get('description', 'Not_Available'),
                        'published_at': snip['publishedAt'],
                        'viewCount': stat.get('viewCount', 0),
                        'like_count': stat.get('likeCount', 0),
                        'dislike_count': stat.get('dislikeCount', 0),
                        'fav_count': stat.get('favoriteCount', 0),
                        'duration': cont.get('duration', 0),
                        'thum_url': snip['thumbnails']['default']['url'],
                        'caption_status': cont.get('caption', 'Not_Available')
                    }
                    vid_data.append(video_info)
            page_token = response.get('nextPageToken')

            if not page_token:
                break

        st.subheader("Video Details")
        st.dataframe(pd.DataFrame(vid_data))
        
        # Comment_Details:
        com_data = []
        p_tokken = None
        com_limit = 2
        
        while True:
            
            for one_vid_id in vid_data:
                
                comment_request = youtube.commentThreads().list(part="snippet,replies", videoId=one_vid_id['video_id'], maxResults=50,pageToken=p_tokken)
                comment_response = comment_request.execute()

                for k in comment_response.get('items',[])[:com_limit]:
                    out_snippet = k['snippet']['topLevelComment']
                    in_snippet = k['snippet']['topLevelComment']['snippet']
                    comment_info = {
                        'comment_id': out_snippet['id'],
                        'video_id': k['snippet']['videoId'],
                        'comment_text': in_snippet['textDisplay'],
                        'Author': in_snippet['authorDisplayName'],
                        'Published_date': in_snippet['publishedAt']}
                    com_data.append(comment_info)

                p_tokken = comment_response.get('nextPageToken')
                # ['snippet']['topLevelComment']['id']-->comment_id
                # ['snippet']['topLevelComment']['snippet']['textDisplay']-->comment_text,
                # ['snippet']['topLevelComment']['snippet']['authorDisplayName']comment_author,
                # ['snippet']['topLevelComment']['snippet']['publishedAt']comment_published_date
            if not p_tokken:
                break

        com_df = pd.DataFrame(com_data)
        st.subheader("Comment Details")
        st.dataframe(com_df)


    # MongoDB - Data Migration Section:
    st.subheader("Data Migration")
    c_ids = st.text_input("Enter the channel_ID Which You Want To Migrate:")
    migration_button = st.button("Migrate Data")

    if migration_button:
        if len(c_ids) == 24 and c_ids.isalnum():  
            def get_ch_data(c_ids):
                req = youtube.channels().list(part="snippet, statistics, contentDetails", id=c_ids.strip())
                resp = req.execute()
                chan_result = []
                c_data = {
                    'Chan_id': resp['items'][0]['id'],
                    'Chan_name': resp['items'][0]['snippet']['title'],
                    'chan_published_At': resp['items'][0]['snippet']['publishedAt'],
                    'Chan_playlist_id': resp['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
                    'Chan_des': resp['items'][0]['snippet']['description'],
                    'Sub_count': resp['items'][0]['statistics']['subscriberCount'],
                    'Chan_view_count': resp['items'][0]['statistics']['viewCount'],
                    'Total_video_count': resp['items'][0]['statistics']['videoCount']
                }
                chan_result.append(c_data)
                return chan_result

            c_d = get_ch_data(c_ids)
            playlist_ids = [chan['Chan_playlist_id'] for chan in c_d]
            st.subheader("Channel Details")
            st.dataframe(pd.DataFrame(c_d))


    # Playlist Details:
            pl_d = []
            pagetoken = None
            for playlist_id in playlist_ids:
                while True:
                    req = youtube.playlistItems().list(part='id,status,snippet,contentDetails', playlistId=playlist_id, maxResults=10, pageToken=pagetoken)
                    res = req.execute()

                    for item in res.get('items', []):
                        playlist_info = {
                            'Chan_playlist_id': item['snippet']['playlistId'],
                            'video_id': item['snippet']['resourceId']['videoId']}
                        pl_d.append(playlist_info)
                    pagetoken = res.get('nextPageToken')

                    if not pagetoken:
                        break
            st.subheader("Playlist Details")
            st.dataframe(pd.DataFrame(pl_d))

    # Video Details:
            vid_data = []
            page_token = None
            while True:
                for playlist_info in pl_d:
                    video_id = playlist_info['video_id']
                    request = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id, maxResults=50, pageToken=page_token)
                    response = request.execute()
                    
                    for j in response.get('items', []):
                        snip = j['snippet']
                        stat = j['statistics']
                        cont = j['contentDetails']

                        video_info = {
                            'video_id': j['id'],
                            'title': snip['title'],
                            'des': snip.get('description', 'Not_Available'),
                            'published_at': snip['publishedAt'],
                            'viewCount': stat.get('viewCount', 0),
                            'like_count': stat.get('likeCount', 0),
                            'dislike_count': stat.get('dislikeCount', 0),
                            'fav_count': stat.get('favoriteCount', 0),
                            'duration': cont.get('duration', 0),
                            'thum_url': snip['thumbnails']['default']['url'],
                            'caption_status': cont.get('caption', 'Not_Available')
                        }
                        vid_data.append(video_info)
                page_token = response.get('nextPageToken')

                if not page_token:
                    break

            st.subheader("Video Details")
            st.dataframe(pd.DataFrame(vid_data))

    # Comment_Details:
            com_data = []
            p_tokken = None
            com_limit = 2

            while True:
                
                for one_vid_id in vid_data:
                    
                    comment_request = youtube.commentThreads().list(part="snippet,replies", maxResults=50,videoId=one_vid_id['video_id'], pageToken=p_tokken)
                    comment_response = comment_request.execute()

                    for k in comment_response.get('items',[])[:com_limit]:
                        out_snippet = k['snippet']['topLevelComment']
                        in_snippet = k['snippet']['topLevelComment']['snippet']
                        comment_info = {
                            'comment_id': out_snippet['id'],
                            'video_id': k['snippet']['videoId'],
                            'comment_text': in_snippet['textDisplay'],
                            'Author': in_snippet['authorDisplayName'],
                            'Published_date': in_snippet['publishedAt']}
                        com_data.append(comment_info)

                    p_tokken = comment_response.get('nextPageToken')
                if not p_tokken:
                    break

            st.subheader("Comment Details")
            st.dataframe(pd.DataFrame(com_data))
        

            cn = c_d 
            plyl = pl_d 
            vi_d = vid_data
            Com_m = com_data 
            coll_data = [{'Channel_Details': cn, 'Playlist_Details': plyl, 'Video_Details': vi_d, 'Comment_Details': Com_m}]
            
            # MongoDB Integration:
            passcode = pl("Balaji@123")
            uri = f"mongodb+srv://balaji:{passcode}@cluster0.9baxl7q.mongodb.net/?retryWrites=true&w=majority"

            # Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))

            # Send a ping to confirm a successful connection
            try:
                client.admin.command('ping')
                print("!!!!!!!!!!!!!!!..........Hi Balaji,Now your python code is connected with MongoDB.......!!!!!!!!!!!!!")
            except Exception as e:
                print(e)
                    
            db = client["Youtube_DB"]#-->The Db will be created
            mycol = db['Youtube_Table1']
                
            # Record Insertion and Duplicate Check:
            for entry in coll_data:
                # Check if entry is a dictionary
                if isinstance(entry, dict):
                    # Check if 'Channel_Details' key is present and is a list
                    if 'Channel_Details' in entry and isinstance(entry['Channel_Details'], list):
                        # Iterate over the list of channel details dictionaries
                        for channel_details_dict in entry['Channel_Details']:
                            # Check if 'Chan_id' key is present in the channel details dictionary
                            if 'Chan_id' in channel_details_dict:
                                c_i = channel_details_dict['Chan_id']
                                existing_record = mycol.find_one({'Channel_Details.Chan_id': c_i})

                                if existing_record is None:
                                    # Record does not exist, insert it
                                    mycol.insert_one(entry)
                                    st.write(f"Record For Channel {c_i} Migrated Successfully.")
                                else:
                                    st.write(f"Record For Channel {c_i} Already Exists, Skipping Migration.")
                            else:
                                st.write("Missing 'Chan_id' Key In 'Channel_Details'.")
                    else:
                        st.write("Invalid Data Structure For 'Channel_Details'.")
                        st.write(f"Problematic Entry: {entry}")
                else:
                    st.write("Invalid Data Structure For Entry.")
                    st.write(f"Problematic Entry: {entry}")
    
    #Record Fetch From MongoDB:
        
    # st.subheader("Data Migration - SQL DB")
    # fetch_button = st.button("My-SQL Work Bench Data Migration")

    # if fetch_button:
    #     # Fetch all records from the MongoDB collection
            passcode = pl("Balaji@123")
            uri = f"mongodb+srv://balaji:{passcode}@cluster0.9baxl7q.mongodb.net/?retryWrites=true&w=majority"

            # Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))
            db = client["Youtube_DB"]#-->The Db will be created
            mycol = db['Youtube_Table1']
            all_records = mycol.find()

            M_C_df_list = []
            M_P_df_list = []
            M_V_df_list = []
            M_CM_df_list = []
            # Process each record
            for record in all_records:
                M_C_df_list.append(pd.DataFrame(list(record.get('Channel_Details', []))))
                M_P_df_list.append(pd.DataFrame(list(record.get('Playlist_Details', []))))
                M_V_df_list.append(pd.DataFrame(list(record.get('Video_Details', []))))
                M_CM_df_list.append(pd.DataFrame(list(record.get('Comment_Details', []))))

            # Concatenate DataFrames
            M_C_df = pd.concat(M_C_df_list, ignore_index=True)
            M_P_df = pd.concat(M_P_df_list, ignore_index=True)
            M_V_df = pd.concat(M_V_df_list, ignore_index=True)
            M_CM_df = pd.concat(M_CM_df_list, ignore_index=True)

            # Display DataFrames
            st.header("Fetched Records From Mongo DB")
            st.subheader("Channel Details")
            st.dataframe(M_C_df)
            st.subheader("Playlist Details")
            st.dataframe(M_P_df)
            st.subheader("Video Details")
            st.dataframe(M_V_df)
            st.subheader("Comment Details")
            st.dataframe(M_CM_df)

            # SQL Integration:
            myconnection_1 = pymysql.connect(host='127.0.0.1', user='root', password='test', database='Youtubedb_ST_FINAL_1')
            cur_1 = myconnection_1.cursor()

            # Record Insertion:
            cur_1.execute('CREATE TABLE IF NOT EXISTS Channel ('
                    'Chan_id VARCHAR(30) PRIMARY KEY,'
                    'Chan_name VARCHAR(30),'
                    'chan_published_At VARCHAR(30),'
                    'Chan_playlist_id  VARCHAR(30) UNIQUE NOT NULL,'
                    'Chan_des MEDIUMTEXT,'
                    'Sub_count INT,'
                    'Chan_view_count INT,'
                    'Total_video_count INT)')

            c_sql = 'Insert into Channel(Chan_id,Chan_name,chan_published_At,Chan_playlist_id,Chan_des,Sub_count,Chan_view_count,Total_video_count)values(%s,%s,%s,%s,%s,%s,%s,%s)'
            for z in range(0,len(M_C_df)):
                cur_1.execute(c_sql,tuple(M_C_df.iloc[z]))#-->z
                myconnection_1.commit()
                
            cur_1.execute('CREATE TABLE IF NOT EXISTS Playlist ('
                    'Chan_playlist_id VARCHAR(30) REFERENCES Channel(Chan_playlist_id),'
                    'video_id VARCHAR(30) UNIQUE NOT NULL)')

            pl_sql = 'Insert into Playlist(Chan_playlist_id,video_id)values(%s,%s)'
            for u in range(0,len(M_P_df)):
                cur_1.execute(pl_sql,tuple(M_P_df.iloc[u]))#-->u
                myconnection_1.commit()
                
            cur_1.execute('CREATE TABLE IF NOT EXISTS Videos_info ('
                    'video_id VARCHAR(30) REFERENCES Playlist(video_id),'
                    'title MEDIUMTEXT,'
                    'des MEDIUMTEXT,'
                    'published_at Varchar(30),'
                    'viewCount MEDIUMINT,'
                    'like_count INT,'
                    'dislike_count INT,'
                    'fav_count INT,'
                    'duration VARCHAR(20),'
                    'thum_url MEDIUMTEXT,'
                    'caption_status VARCHAR(6))')

            v_sql = 'INSERT INTO Videos_info (video_id, title, des, published_at, viewCount, like_count, dislike_count, fav_count, duration, thum_url, caption_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            for n in range(0, len(M_V_df)):
                cur_1.execute(v_sql, tuple(M_V_df.iloc[n]))
                myconnection_1.commit()

            cur_1.execute('CREATE TABLE IF NOT EXISTS COMMENT ('
                        'comment_id varchar(26) PRIMARY KEY,'
                        'video_id VARCHAR(30) REFERENCES Videos_info(video_id),'
                        'comment_text MEDIUMTEXT,'
                        'Authour MEDIUMTEXT,'
                        'Published_date VARCHAR(30))')
                
            cm_sql = 'INSERT INTO COMMENT (comment_id,video_id,comment_text,Authour,Published_date) VALUES (%s, %s, %s, %s, %s)'
            for h in range(0, len(M_CM_df)):
                cur_1.execute(cm_sql, tuple(M_CM_df.iloc[h]))
                myconnection_1.commit()
                
            #Closing Connections:
            cur_1.close()
            myconnection_1.close()

            st.success("The Records Fetched From Mongo DB Were Inserted In To My-SQL WorkBench")
        else:
            st.warning("""
                        
                        !!!!!!!!!.......Sorry........!!!!!!!!!,
                        
                        You Are Trying To Migrate More Than One Channel_ID At A Time,
                        
                        Provide your Channel ID's One By One For Data Migration
                        
                        !!!!!!!!........Please Check Your Provided Inputs......!!!!!!!!! 
                        
                        """)
        
    # Questions Section:
    st.subheader("Questions")
    conn = pymysql.connect(host='127.0.0.1', user='root', password='test', database='Youtubedb_ST_FINAL_1')
    option = st.selectbox('Meaningfull Insights',('Question_1', 'Question_2', 'Question_3','Question_4','Question_5','Question_6','Question_7','Question_8','Question_9','Question_10'))
    button = st.button("Click Me")
    if button:
        with conn.cursor() as cursor: 
            
            if option == 'Question_1':
                st.subheader('# Question 1: What Are The Names Of All The Videos And The Channels')
                cursor.execute("select A.Chan_name,C.title as Video_Name from Youtubedb_ST_FINAL_1.channel  A INNER JOIN Youtubedb_ST_FINAL_1.playlist B on (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C on (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D on (C.video_id = D.video_id)")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                                
                                Column 0 --> Channel Names\n
                                Column 1 ---> Video Names
                        
                        """)
                
            
            elif option == 'Question_2':
                st.subheader('# Question 2: Which Channel Has The Most Number Of Videos And How Many Videos Do They Have')
                cursor.execute("select A.Chan_name,count(C.video_id) as Count_of_video_id from Youtubedb_ST_FINAL_1.channel  A INNER JOIN Youtubedb_ST_FINAL_1.playlist B on (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C on (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D on (C.video_id = D.video_id) group by A.chan_name")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                                
                                Column 0 --> Channel Names\n
                                Column 1 --> Video Count
                        
                        """)
            
            elif option == 'Question_3':
                st.subheader('# Question 3: What Are The Top 10 Most Viewed Videos And Their Respective Channels')
                cursor.execute("select A.Chan_name,C.Video_id,C.title,C.viewCount as Video_View_count  from Youtubedb_ST_FINAL_1.channel  A INNER JOIN Youtubedb_ST_FINAL_1.playlist B on (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C on (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D on (C.video_id = D.video_id) order by C.viewCount desc limit 10")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                                
                                Column 0 --> Channel Names\n
                                Column 1 --> Video ID's\n
                                Column 2 --> Video Names\n
                                Column 3 --> Video View Count
                        
                        """)
            
            elif option == 'Question_4':
                st.subheader('# Question 4: How Many Comments Were Made On Each Video And What Are The Corresponding Video Names')
                cursor.execute("select distinct(C.video_id),C.title,count(D.comment_id)over(partition by C.video_id) as comment_count_per_video from Youtubedb_ST_FINAL_1.channel  A INNER JOIN Youtubedb_ST_FINAL_1.playlist B on (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C on (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D on (C.video_id = D.video_id) Order by comment_count_per_video desc")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                                
                                Column 0 --> Video ID's\n
                                Column 1 --> Video Name\n
                                Column 2 --> Comment Counts Per Video\n
                                
                        
                        """)
                
            elif option == 'Question_5':
                st.subheader('# Question 5: Which Videos Have The Highiest Number Of Likes And What Are All The Corresponding Channel Names')
                cursor.execute("select A.Chan_name,C.Video_id,C.title,C.like_count as Video_like_count from Youtubedb_ST_FINAL_1.channel  A INNER JOIN Youtubedb_ST_FINAL_1.playlist B on (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C on (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D on (C.video_id = D.video_id)  order by C.viewCount desc")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                                
                                Column 0 --> Channel Names\n
                                Column 1 --> Video ID's\n
                                Column 2 --> Video Names\n
                                Column 3 --> Video Like Count
                                
                        
                        """)
                
            elif option == 'Question_6':
                st.subheader('# Question 6: What Are The Total Number Of Likes and Dislikes For Each Video And What Are The Corresponding Video Names')
                cursor.execute("SELECT DISTINCT C.video_id, C.title, SUM(C.like_count) OVER (PARTITION BY C.video_id) AS Like_Count_Per_Video, SUM(C.dislike_count) OVER (PARTITION BY C.video_id) AS Dislike_Count_Per_Video FROM Youtubedb_ST_FINAL_1.channel A INNER JOIN Youtubedb_ST_FINAL_1.playlist B ON (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C ON (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D ON (C.video_id = D.video_id) ORDER BY Like_Count_Per_Video DESC, Dislike_Count_Per_Video DESC")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                                
                                Column 0 --> Video ID's\n
                                Column 1 --> Video Names\n
                                Column 2 --> Like Count Per Video\n
                                Column 3 --> Dislike Count Per Video
                                
                        
                        """)

                
            elif option == 'Question_7':
                st.subheader('# Question 7: What Are The Total Number Of Views For Each Channel And What Are Their Corresponding Channel Names')
                cursor.execute("select chan_name,chan_view_count from Youtubedb_ST_FINAL_1.channel")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                    
                    Column 0 --> Channel Name\n
                    Column 1 --> Channel View Count\n
                
                """)
                
                
            elif option == 'Question_8':
                st.subheader('# Question 8: What Are The Names Of All The Channels That Have Published Videos In The Year 2022')
                cursor.execute("select A.chan_name, C.published_at AS Video_Published_At FROM Youtubedb_ST_FINAL_1.channel A INNER JOIN Youtubedb_ST_FINAL_1.playlist B ON A.Chan_playlist_id = B.Chan_playlist_id INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C ON B.video_id = C.video_id INNER JOIN Youtubedb_ST_FINAL_1.comment D ON C.video_id = D.video_id where C.published_at LIKE '2022%'")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                    
                    Column 0 --> Channel Name\n
                    Column 1 --> Video Published At
                
                """)
                
            elif option == 'Question_9':
                st.subheader('# Question 9: What Is The Average Duration Of All The Videos In Each Channel And What Are Their Corresponding Channel Names')
                cursor.execute("SELECT A.chan_name, AVG(TIME_TO_SEC(SUBSTRING_INDEX(SUBSTRING_INDEX(C.duration, 'PT', -1), 'S', 1))) AS Average_Video_Duration FROM Youtubedb_ST_FINAL_1.channel A INNER JOIN Youtubedb_ST_FINAL_1.playlist B ON (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C ON (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D ON (C.video_id = D.video_id) GROUP BY A.chan_name")
                result = cursor.fetchall()
                st.dataframe(result)
                st.text("Average Duration Results in Seconds")
                st.success("""
                    
                    Column 0 --> Channel Name\n
                    Column 1 --> Average Video Duration
                
                """)
            
            elif option == 'Question_10':
                st.subheader('# Question 10: Which Video Has The Highiest Number Of Comments And What Are The Their Channel Name')
                cursor.execute("select distinct(C.video_id),count(D.comment_id) over (partition by C.video_id) as count_of_comment_per_video,A.Chan_name from Youtubedb_ST_FINAL_1.channel  A INNER JOIN Youtubedb_ST_FINAL_1.playlist B on (A.Chan_playlist_id = B.Chan_playlist_id) INNER JOIN Youtubedb_ST_FINAL_1.Videos_info C on (B.video_id = C.video_id) INNER JOIN Youtubedb_ST_FINAL_1.comment D on (C.video_id = D.video_id) order by count_of_comment_per_video desc limit 1")
                result = cursor.fetchall()
                st.dataframe(result)
                st.success("""
                    
                    Column 0 --> Video ID's\n
                    Column 1 --> Count Of Comment Per Video\n
                    Column 2 --> Channel Name
                
                """)
            
        conn.close()
    

    





    
    
    
    
    

    

    
    
    
    

        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    # # Fetching data from MongoDB based on the list of channel IDs
    # chan_ids_list = mycol.distinct('Channel_Details.Chan_id')

    # # Check if any channel IDs were obtained
    # if chan_ids_list:
    #     # Fetch all documents with matching channel IDs
    #     query = {'Channel_Details.Chan_id': {'$in': chan_ids_list}}
    #     cursor = mycol.find(query)
        
    #     # Convert the cursor to a list of dictionaries
    #     data_list = list(cursor)

    #     # Check if any documents were found
    #     if data_list:
    #         # Create separate dataframes for each type of data
    #         M_C_df = pd.DataFrame([item['Channel_Details'] for item in data_list])
    #         M_P_df = pd.DataFrame([item['Playlist_Details'] for item in data_list])
    #         M_V_df = pd.DataFrame([item['Video_Details'] for item in data_list])
    #         M_CM_df = pd.DataFrame([item['Comment_Details'] for item in data_list])

    #         # Proceed with using the dataframes
    #         st.success("Data fetched from MongoDB successfully.")
    #     else:
    #         st.warning("No data found for the specified channel IDs.")
    # else:
    #     st.warning("No channel IDs found in MongoDB.")


 
    
    
    
    # Channel_ID Check:
# def is_channel_data_in_mongo(channel_id, mycol):
#     existing_data = mycol.find_one({"Channel_Details.Chan_id": channel_id})
#     if existing_data:
#         st.warning(f"The Channel_ID {channel_id} is already existed in MongoDB. No need for Data Scraping")
#     else:
#         st.success(f"The Channel_ID {channel_id} is not existed in MongoDB. You can go ahead for Data Scraping.")

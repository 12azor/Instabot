import requests
import urllib
import json

my_token="1606815543.feefa28.c2601ebc8ed5493481c5e0b5f72ec84e"
base_url="https://api.instagram.com/v1/"

#--------------------Function to get Self Information--------------------#
def self_info():
    url=base_url+"users/self/?access_token=%s"%(my_token)
    result= requests.get(url).json()
    print(json.dumps(result, indent=3))
    
    
#--------------------Function to get information of user from provided username--------------------#
def get_user_info(user_id):
    url=base_url + ("users/%s/?access_token=%s") % (user_id, my_token)
    result=requests.get(url).json()
    print(json.dumps(result, indent=3))
    

#--------------------Function to get recent media liked by self--------------------#
def recent_media_liked():
    url=base_url+("users/self/media/liked?access_token=%s") % (my_token)
    result=requests.get(url).json()    
    print "The recent media liked by the user is : "
    print (json.dumps(result["data"][0],indent= 3))
    

#--------------------Function to return USER ID--------------------#
def get_user_id(user_name):
    url = (base_url + "users/search?q=%s&access_token=%s") % (user_name, my_token)
    result=requests.get(url).json()
    if result["meta"]["code"]==200:
        return result["data"][0]["id"]
    else:
        return 0

        
#--------------------Function to fetch info of self recent post--------------------#
def get_own_post():
    url=base_url+"users/self/media/recent/?access_token=%s" %(my_token)
    result= requests.get(url).json()
    if result["meta"]["code"]==200: #checks if the request was sucessfull
        if len(result["data"]):     #check if data is present
            my_posts_info=result["data"][0]
            print(json.dumps(my_posts_info, indent= 3))
            return result["data"][0]["id"]
        else:
            print "You have no post."
    else:
        return 0


#--------------------Function to Check if user exixts and has some Information--------------------#
def search_user(user_name):
    url = (base_url + "users/search?q=%s&access_token=%s") % (user_name, my_token)
    result=requests.get(url).json()
    if result["meta"]["code"]==200 and len(result["data"])>=1:
        print "A User With Such Username Exists."
        return(1)
    else:
        print "Either the Username does not exist in sandbox OR does not contain any information to retrive."
        return(0)
    


#--------------------Function to get User's post--------------------#
def get_user_post(username):
    user_id = get_user_id(username)
    if user_id == None:
        print "User doesmnt exist"
    else:
        url= base_url + 'users/%s/media/recent/?access_token=%s'% (user_id, my_token)
        user_media = requests.get(url).json()
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                option=int(raw_input("You want to choose the post on the basis of:\n1. Most Recent\n2. Max Likes\n3. Max Comments\nOption: "))
                                     
                if option==1:
                    return user_media['data'][0]['id']
                                     
                elif option==2:
                    counter=1
                    media_id=user_media["data"][0]["id"]
                    max_like=user_media["data"][0]
                    while len(user_media["data"])>counter:
                        if max_like["likes"]["count"]<user_media["data"][counter]["likes"]["count"]:
                            max_like=user_media["data"][counter]
                            media_id=max_like["id"]
                        counter=counter+1
                    return media_id
                              
                elif option==3:
                    counter=1
                    media_id=user_media["data"][0]["id"]
                    max_like=user_media["data"][0]
                    while len(user_media["data"])>counter:
                        if max_like["comments"]["count"]<user_media["data"][counter]["comments"]["count"]:
                            max_like=user_media["data"][counter]
                            media_id=max_like["id"]
                        counter=counter+1
                    return media_id
                              
            else:
                print "There is no post!"
        else:
            print "Status code other than 200 received!"


#--------------------Function to download self recent post--------------------#
def self_download_post():
    url=base_url+"users/self/media/recent/?access_token=%s" %(my_token)
    result= requests.get(url).json()
    image_name=raw_input("Enter the image name you want to save it with (append '.jpeg' at the end): ")     
    image_url = result['data'][0]['images']['standard_resolution']['url']
    urllib.urlretrieve(image_url, image_name )
    print "Your image has been downloaded!"


#--------------------Function to download USER's recent post--------------------#
def user_download_post(user_name,media_id):
    user_id = get_user_id(user_name)
    if user_id != None:
        image_url=""
        url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, my_token)
        user_media = requests.get(url).json()
        image_name = raw_input("\nEnter the image name you want to save it with (append '.jpeg' at the end): ")
        for i in range(0,len(user_media["data"])):
            if user_media["data"][i]["id"]==media_id:
                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                break
        if len(image_url)!=0:
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
    else:
        print "User Doesnot Exist"


while True:
    user_option=int(raw_input("Enter the number corresponding to the options you want to perform the actions on:\n1. Self\n2. Other Users\n3. Exit.\nOption: "))
    
    if user_option==1:
        choice_option=int(raw_input("Do you want to:\n1. Fetch and display your all user details.\n2. Fetch and display your recent post's details.\n3.Recent media liked.\nOption: "))
        
        if choice_option==1:
            self_info()
            
        elif choice_option==2:
            my_post_id=get_own_post()
            if my_post_id==0:
                print "Some other code other than 200 recieved."
            elif my_post_id != None:
                print "My recent post's ID is: "+str(my_post_id)
                print "The recent Image will now be downloaded...."
                self_download_post()
        elif choice_option==3:
            recent_media_liked()
        else:
            print "You have entered a wrong option. Try again./n"
            
        continue
    
    elif user_option==2:
        username=raw_input("Enter the username: ")
        validate_username=search_user(username)
        
        if validate_username:
            username_choice=int(raw_input("Would you like to:\n1. Get %s 's user ID.\n2. Fetch %s 's POST.\n3. Print general Info of %s.\n4. Get comments on a post of %s.\n5. Make acomment on %s 's post.\n6. Like %s 's post.\nOption: " %(username,username,username,username,username,username)))

            if username_choice==1:
                user_id=get_user_id(username)
                if user_id==0:
                    print "Some Other code than 200 recieved."
                else:
                    print "User ID is: "+str(user_id)
                    
            elif username_choice==2:
                media_id=get_user_post(username)
                if media_id!= None:
                    print "The ID of recent media is: "+str(media_id)
                    print "The Image with above ID will now be downloaded....."
                    user_download_post(username,media_id)

            elif username_choice==3:
                user_id=get_user_id(username)
                get_user_info(user_id)
                
                
                
        

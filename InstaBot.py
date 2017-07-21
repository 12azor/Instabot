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
    
    
#--------------------Function to get information of user from provided username--------------------
def get_user_info(user_id):
    url=base_url + ("users/%s/?access_token=%s") % (user_id, my_token)
    result=requests.get(url).json()
    print result


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
        print "Some other code recieved."


#--------------------Function to Check if user exixts and has some Information--------------------#
def search_user(user_name):
    url = (base_url + "users/search?q=%s&access_token=%s") % (user_name, my_token)
    result=requests.get(url).json()
    if result["meta"]["code"]==200 and len(result["data"])>=1:
        print "A User With Such Username Exists."
        return(1)
    else:
        print "The Username does not exists OR does not contain any information to retrive."
        return(0)
    


#--------------------Function to get User's recent post--------------------#
def get_user_post(username):
    user_id = get_user_id(username)
    if user_id == None:
        print "User does'nt exist"
    else:
        url= base_url + 'users/%s/media/recent/?access_token=%s'% (user_id, my_token)
        user_media = requests.get(url).json()
        print user_media["data"]
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                print "Info of the Recent Media is: "+str(json.dumps(user_media['data'][0],indent=3))
                return user_media['data'][0]['id']
            else:
                print "There is no recent post!"
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
    


while True:
    user_option=int(raw_input("Enter the number corresponding to the options you want to perform the actions on:\n1. Self\n2. Other Users\n3. Exit.\nOption: "))
    
    if user_option==1:
        choice_option=int(raw_input("Do you want to:\n1. Fetch and display your all user details.\n2. Fetch and display your recent post's details.\nOption: "))
        
        if choice_option==1:
            self_info()
            
        elif choice_option==2:
            my_post_id=get_own_post()
            print "My recent post's ID is: "+str(my_post_id)
            print "The recent Image will now be downloaded...."
            self_download_post()
            
        else:
            print "You have entered a wrong option. Try again./n"
            
        continue
    
    elif user_option==2:
        username=raw_input("Enter the username: ")
        validate_username=search_user(username)
        
        if validate_username:
            username_choice=int(raw_input("Would you like to:\n1. Get %s 's ID.\n2. Fetch %s 's recent POST.\n3. Get recent media liked by %s.\n4. Get comments on a post of %s.\n5. Make acomment on %s 's post.\n6. Like %s 's post.\nOption: " %(username,username,username,username,username,username)))

            if username_choice==1:
                user_id=get_user_id(username)
                if user_id==0:
                    print "Some Other code than 200 recieved."
                else:
                    print "User ID is: "+str(user_id)
                    
            elif username_choice==2:
                media_id=get_user_post(username)
                print "The ID of recent media is: "+str(media_id)
        

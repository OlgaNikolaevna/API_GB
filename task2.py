import vk

session = vk.AuthSession(app_id=input("APP_ID: "),
                         user_login=input("user_login: "),
                         user_password=input("user_password: "))
vkapi = vk.API(session)



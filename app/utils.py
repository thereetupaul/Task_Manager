from passlib.context import CryptContext 


#bcrypt 5.0.0 is NOT compatible with passlib (as of now) 
#Officially recommended versions (WORKING combo) ->  passlib==1.7.4  bcrypt==4.0.1
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def Hash(password: str):
    return pwd_context.hash(password)


def Verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
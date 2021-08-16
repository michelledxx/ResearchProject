myhost="heroku.cocoldeaofkv.us-east-2.rds.amazonaws.com"
mypasswd="dublinbus"
myuser="admin"
mydatabase="dubbusdb"
mycharset="utf8mb4"

engine = f"mysql+mysqlconnector://{myuser}:{mypasswd}@{myhost}:3306/{mydatabase}"
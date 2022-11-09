from pymongo import MongoClient

cluster=MongoClient("mongodb+srv://shadank:shadankalam@cluster0.ef68wuq.mongodb.net/?retryWrites=true&w=majority")
db=cluster["Cluster0"]
collections=db["test"]
class data():
    def userdata(item:dict):
        collections.insert_one(item)
    
    def userquery(username:str):
        results=collections.find({"_id":username})
        if results:
            for result in results:
                return result["password"]
                break
        else:
            return "wrong username/password"
    def updatephone(username:str, phone:int):
        collections.update_one({"_id":username}, {"$set":{"phone":phone}})

    def nameupdate(username:str, newname:str):
        collections.update_one({"_id":username}, {"$set":{"name":newname}})

    def getUserDetails(username:str):
        user=collections.find({"_id":username})
        return user


        



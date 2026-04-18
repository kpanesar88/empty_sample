import json

filename = "dataset/dataset.json"

def add_email(data, filename):
    with open(filename, "w", encoding="utf-8") as database:
        json.dump(data, database, indent = 4)

with open(filename, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    
    new_email = {
    "id": 61,
    "company": "TEST",
    "job_title": "Engineering Intern",
    "sender": "recruitment@peakroute.com",
    "subject": "TEST",
    "body": "We are pleased to let you know that you have been moved forward to the next stage.",
    "status": "next_step"
     }
    
    data["emails"].append(new_email)
    


add_email(data,filename)
    

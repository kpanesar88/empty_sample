import json

filename = "dataset/dataset.json"
next_id = ""


rv_company = ""
rv_job_title=""
rv_sender=""
rv_subject=""
rv_body=""
rv_status=""
rv_id = next_id



def add_email(data, filename):
    with open(filename, "w", encoding="utf-8") as database:
        json.dump(data, database, indent = 4)
        
        if len(data["emails"] == 0):
            next_id = 1
        else: 
            next_id = data["emails"][-1]["id"] + 1


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
    

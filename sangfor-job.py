import requests
import json

# 岗位列表链接：https://app.mokahr.com/campus_apply/sangfor/6146#/jobs
jobs_url = "https://app.mokahr.com/api/outer/ats-jc-apply/website/jobs"
data = {"limit": 15, "offset": 0, "siteId": 6146, "orgId": "sangfor", "site": "campus", "needStat": "true"}
headers = {
    'Content-Type': 'application/json'
}
# response1 = requests.post(url=jobs_url, json=data)
response = requests.post(url=jobs_url, headers=headers, data=json.dumps(data))
total_job = response.json()["data"]["jobStats"]["total"]
jobs = response.json()["data"]["jobs"]
print(total_job)
for job in jobs:
    title = job["title"]
    education = job["education"]
    print(title, education)
    for location in job["locations"]:
        city_id = location["cityId"]
        address = location["address"].strip()
        print(city_id, address)
    # https://app.mokahr.com/campus_apply/sangfor/6146#/job/9a955d38-b4fb-41b9-baaa-ae4fb4217313
    desc_url = "https://app.mokahr.com/campus_apply/sangfor/6146#/job/" + job["id"]
    print(desc_url)
    print()
    # print(job)
# print(response.json()["data"])

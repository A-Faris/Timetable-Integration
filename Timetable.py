import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Timetable code in website file is opened and read
with open('website.html', 'rb') as f:
  soup = BeautifulSoup(f.read(), 'html.parser')

# Enable access to Notion Timetable database
token = "secret_lDaX0i5lT0SwzPnnAUyUBhAmcG8ARyGujSk57kSYrp5" # from Notion integration
databaseId = "367ae1009e4c4cadba7eafbbacc39c39" # from Notion database page
# https://notiom.notion.site/367ae1009e4c4cadba7eafbbacc39c39?v=c910ad29ed224715b05a9f35ef349a07&pvs=4

headers = {
  "Authorization": "Bearer " + token,
  "Content-Type": "application/json",
  "Notion-Version": "2022-02-22"
}

def createPage(databaseId, headers, title = "", week = "", start = "", end = "", location = "", date = ""):
  # Correcting data
  if "CAPE5010M" in title:
    title = "Research Project (MEng)"
    module = "CAPE5010M Research Project (MEng)"
    staff = ["Dr Simon Antony"]
  elif "CAPE5300M" in title:
    title = "Chemical Products Design and Development"
    module = "CAPE5300M Chemical Products Design and Development"
    staff = ["Dr David Harbottle", "Dr Tim Hunter", "Prof. Andrew Bayly"]
  elif "CAPE5320M" in title:
    title = "Multi-Scale Modelling and Simulation"
    module = "CAPE5320M Multi-Scale Modelling and Simulation"
    staff = ["Dr Ali Hassanpour", "Dr Antonia Borissova", "Dr Robert Hammond", "Prof. Andrew Bayly"]
  elif "CAPE5330M" in title:
    title = "Advanced Reaction Engineering"
    module = "CAPE5330M Advanced Reaction Engineering"
    staff = ["Prof. Frans Muller"]
  elif "CAPE5340M" in title:
    title = "Advances in Chemical Engineering"
    module = "CAPE5340M Advances in Chemical Engineering"
    staff = ["Dr Nicholas Warren", "Prof Richard Bourne"]
  elif "CAPE Personal Tutorials" in title:
    title = "CAPE Personal Tutorials"
    module = " "
    staff = []
  else:
    title = "Employability"
    module = " "
    staff = []
  
  # Create a new page in Notion Timetable database
  newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "Dates": {
                "date": {
                    "start": datetime.strptime(date + " " + start, '%A %d %B %Y %H:%M').isoformat(),
                    "end": datetime.strptime(date + " " + end, '%A %d %B %Y %H:%M').isoformat(),
                    "time_zone": "Europe/London"
                }
            },
            "Topic":        {"select":        {"name": module}},
            "Staff Member": {"multi_select": [{"name": i} for i in staff]},
            "Week":         {"multi_select": [{"name": "Week " + week}]},
            "Module":       {"select":        {"name": module}},
            "Location":     {"rich_text":    [{"text": {"content": location}}]},
            "Name":         {"title":        [{"text": {"content": title}}]}
        }
    }
  res = requests.request("POST", 'https://api.notion.com/v1/pages', headers=headers, data=json.dumps(newPageData))
  print(res.status_code)
  print(res.text)

# Input the data into Notion Timetable database
for day in soup.findAll(class_="day"):
  for i in range(len(day.select(".start"))):
    createPage(
      databaseId,
      headers,
      [j.get_text().strip() for j in day.select(".description")][i],  # title
      [j.get_text().strip() for j in day.select(".week")][0],         # week number
      [j.get_text().strip() for j in day.select(".start")][i],        # start
      [j.get_text().strip() for j in day.select(".end")][i],          # end
      [j.get_text().strip() for j in day.select(".location")][i],     # location
      [j.get_text().strip() for j in day.select(".date")][0]          # date
    )
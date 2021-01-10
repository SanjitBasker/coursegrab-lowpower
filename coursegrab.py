from bs4 import BeautifulSoup
import json
import requests


def jprint(obj, sort_keys=True, indent=4):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=sort_keys, indent=indent)
    print(text)


def harvestSections(roster, subject, number, *args):
    ans = {}
    response = requests.get("https://classes.cornell.edu/browse/roster/{}/class/{}/{}".format(roster, subject, number))
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    # print(soup.body.prettify())
    enrollBox = soup.body.find_all(id="wrap", role="main")[0].find_all(id="content-wrap")[0].find_all(id="content")[0] \
        .find_all(id="main")[0].find_all(id="main-body")[0].find_all(id="search-refresh")[0].find_all(
        attrs={"class": "class-listing"})[0].find_all(attrs={"data-subject": subject, "data-catalog-nbr": number})[0] \
        .find_all(attrs={"class": "sections"})[0].find_all(attrs={"class": "group heavy-left"})[0]
    for i in enrollBox.children:
        if "section" in i['class']:
            classNum = 0
            sectionName = ""
            available = None
            for j in i.children:
                if j['class'] == ['class-numbers']:
                    guessNum = int(j.find('p').find('strong').contents[0])
                    if len(args) == 0 or guessNum in args[0]:
                        classNum = guessNum
                        sectionName = j.find('em').contents[0] + " " + str(j.find('p').contents[-2]).strip()
                elif j['class'] == ['open-status']:
                    if 'open-status-closed' in j.span.span['class']:
                        available = False
                    if 'open-status-open' in j.span.span['class']:
                        available = True
            if classNum != 0:
                ans[sectionName] = [classNum, available]
    return ans


def test():
    ans = {}
    courses = [("CS", 4410), ("CS", 4700), ("MATH", 1920)]
    roster = "SP21"
    for subject, number in courses:
        ans[subject + ' ' + str(number)] = harvestSections(roster, subject, number)

    specCourses = [("ECON", 1120, [4840, 4842, 5041, 4843, 4845, 4848, 17802, 17805])]
    for subject, number, restriction in specCourses:
        ans[subject + ' ' + str(number)] = harvestSections(roster, subject, number, restriction)
    for key in ans:
        val = ans[key]
        for key2 in list(val.keys()):
            if val[key2][-1] == False:
                del val[key2]
    jprint(ans)


if __name__ == "__main__":
    ans = {}
    courses = [("CS", 4380), ("CS", 4700), ("MATH", 4500)]
    roster = "SP21"
    for subject, number in courses:
        ans[subject + ' ' + str(number)] = harvestSections(roster, subject, number)

    specCourses = [("ECON", 1120, [4840, 4842, 5041, 4843, 4845, 4848, 17802, 17805])]
    for subject, number, restriction in specCourses:
        ans[subject + ' ' + str(number)] = harvestSections(roster, subject, number, restriction)
    for key in ans:
        val = ans[key]
        for key2 in list(val.keys()):
            if val[key2][-1] == False:
                del val[key2]

    pass

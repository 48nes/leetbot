from requests import Session
from config import us
import json


class leetmodel:
    def __init__(self, un, pw, resolve=us):

        self.session = Session()
        self.api = resolve
        resp = self.session.get(self.api["login"], headers={
            "X-Requested-With": 'XMLHttpRequest',
            "X-CSRFToken": ""
        })

        self.uname = un

        self.tokens = {"csrf": resp.cookies.get_dict()['csrftoken']}
        self.tokens["LEETCODE_SESSION"] = "abcd"

        hd = self.get_headers(self.api["login"])
        payload = {"csrfmiddlewaretoken": self.tokens["csrf"], "login": un, "password": pw}

        resp2 = self.session.post(self.api["login"], headers=hd, data=payload)
        self.tokens["session"] = resp2.cookies.get_dict()["LEETCODE_SESSION"]

    def get_headers(self, referer=None):
        if referer == None:
            referer = self.api["base"]

        hd = {'User-Agent': 'Mozilla/5.0',
              "X-Requested-With": 'XMLHttpRequest', 'Referer': referer,
              "Cookie": "LEETCODE_SESSION=${Helper.credit.session};csrftoken=${Helper.credit.csrfToken}"}

        if "csrf" in self.tokens:
            hd["X-CSRFToken"] = self.tokens["csrf"]

        if "session" in self.tokens:
            hd["Cookie"] = "LEETCODE_SESSION=%s;csrftoken=%s;" % (self.tokens["session"], self.tokens["csrf"])

        return hd

    def getRecentSubs(self, user):
        op = {"operationName": "getRecentSubmissionList",
              "variables": json.dumps({"username": user}),
              "query": "query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n"}

        hd = self.get_headers(self.api["profile"](user))

        s = self.session.post(self.api["graphql"], headers=hd, data=op)

        return json.loads(s.content)["data"]["recentSubmissionList"]

    def getUserData(self, user):
        op = {"operationName": "getUserProfile", "variables": json.dumps({"username": user}),
              "query": "query getUserProfile($username: String!) {\n  allQuestionsCount {\n    difficulty\n    count\n    __typename\n  }\n  matchedUser(username: $username) {\n    username\n    socialAccounts\n    githubUrl\n    contributions {\n      points\n      questionCount\n      testcaseCount\n      __typename\n    }\n    profile {\n      realName\n      websites\n      countryName\n      skillTags\n      company\n      school\n      starRating\n      aboutMe\n      userAvatar\n      reputation\n      ranking\n      __typename\n    }\n    submissionCalendar\n    submitStats: submitStatsGlobal {\n      acSubmissionNum {\n        difficulty\n        count\n        submissions\n        __typename\n      }\n      totalSubmissionNum {\n        difficulty\n        count\n        submissions\n        __typename\n      }\n      __typename\n    }\n    badges {\n      id\n      displayName\n      icon\n      creationDate\n      __typename\n    }\n    upcomingBadges {\n      name\n      icon\n      __typename\n    }\n    activeBadge {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n"}

        hd = self.get_headers(self.api["profile"](user))

        s = self.session.post(self.api["graphql"], headers=hd, data=op)

        return json.loads(s.content)["data"]["matchedUser"]
import requests, time, os, re
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from dotenv import load_dotenv


def message_webhook(post):
    try:
        Message = {
            "username": post["username"],
            "avatar_url": post["avatar"],
            "content": "{0}\n---\n{1}".format(post["link"], post["post"]),
        }
        requests.post(os.getenv('webhook_url'), data=Message)
    except Exception as e:
        print(e)


def get_last_post(threadid):
    payload = {"threadid": threadid, "goto": "lastpost"}
    r = requests.get("https://forums.somethingawful.com/showthread.php", params=payload)
    pageid = parse_qs(r.url)["pagenumber"][0].replace("#lastpost", "")
    soup = BeautifulSoup(r.text, "html.parser")
    last_post = soup.find_all("a", {"title": "Link to this post"}, href=True)[-1][
        "href"
    ].replace("#post", "")
    return last_post, pageid


def generate_link(threadid, pageid, postid):
    return "https://forums.somethingawful.com/showthread.php?threadid={0}&pagenumber={1}#post{2}".format(
        threadid, pageid, postid
    )


def get_post_content(threadid, pageid, postid):
    payload = {"threadid": threadid, "pagenumber": pageid}
    r = requests.get("https://forums.somethingawful.com/showthread.php", params=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find("table", {"id": "post{0}".format(postid)})
    post_text = content.find("td", {"class": "postbody"}).get_text().strip()
    if "posted:\n" in post_text:
        try:
            result = re.match(r"(.*:\n)(.*)(\n\n)", post_text)
            post_text = "```{0}```{1}".format(post_text[result.regs[0][0]:result.regs[0][1]], post_text[result.regs[0][1]:])
        except Exception as e:
            print(e)
    try:
        avatar_url = content.find("dd", {"class": "title"}).find("img")["src"]
    except:
        avatar_url = ""
    post = {
        "username": content.find("dt", {"class": "author"}).get_text(),
        "link": r.url + "#post{0}".format(postid),
        "avatar": avatar_url,
        "post": post_text,
    }
    return post


while True:
    load_dotenv()

    last_post, pageid = get_last_post(os.getenv('threadid'))
    post = get_post_content(os.getenv('threadid'), pageid, last_post)
    time.sleep(5)

    try:
        if last_post > old_post:
            print(
                "Got new post by {0}: {1}".format(
                    post["username"], generate_link(os.getenv('threadid'), pageid, last_post)
                )
            )
            message_webhook(post)
            old_post = last_post
        else:
            print(
                "No new posts, current last post by {0}: {1}".format(
                    post["username"], generate_link(os.getenv('threadid'), pageid, last_post)
                )
            )
    except NameError:
        print(
            "First run, current last post by {0}: {1}".format(
                post["username"], generate_link(os.getenv('threadid'), pageid, last_post)
            )
        )
        old_post = last_post

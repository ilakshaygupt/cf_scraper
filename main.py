from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def extract_contest_and_problem_code(link):
    parts = link.split("/")
    return parts[4], parts[6]


def scrape_codeforces_submissions(username, total_pages=1):
    contests_by_length = {1: [], 2: [], 3: [], 4: []}
    url = f"https://codeforces.com/submissions/{username}/page/1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    max_page_index = max(int(span['pageindex'])
                         for span in soup.find_all("span", class_="page-index"))

    total_pages = max_page_index
    for page in range(1, total_pages + 1):
        url = f"https://codeforces.com/submissions/{username}/page/{page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            problem_cells = soup.find_all(
                "td", class_="status-small", attrs={"data-problemid": True})

            for cell in problem_cells:
                if cell.find("a"):
                    link = "https://codeforces.com" + cell.find("a")["href"]
                    contest_id, problem_code = extract_contest_and_problem_code(
                        link)
                    contests_by_length[len(contest_id)].append({"link": link, "text": f"{contest_id} - {cell.find('a').get_text(strip=True)} "})

            print(f"Page {page} processed for {username}.")
        else:
            print(f"Failed to retrieve the page {page} for {username}. Status code: {response.status_code}")
        unique_dicts = {x['link']: x for x in contests_by_length[1]}.values()
        unique_list_1 = list(unique_dicts)
        contests_by_length[1] = unique_list_1
        unique_dicts = {x['link']: x for x in contests_by_length[2]}.values()
        unique_list_2 = list(unique_dicts)
        contests_by_length[2] = unique_list_2
        unique_dicts = {x['link']: x for x in contests_by_length[3]}.values()
        unique_list_3 = list(unique_dicts)
        contests_by_length[3] = unique_list_3
        unique_dicts = {x['link']: x for x in contests_by_length[4]}.values()
        unique_list_4 = list(unique_dicts)
        contests_by_length[4] = unique_list_4
        contests_by_length[1].sort(key=lambda x: x["link"])
        contests_by_length[2].sort(key=lambda x: x["link"])
        contests_by_length[3].sort(key=lambda x: x["link"])
        contests_by_length[4].sort(key=lambda x: x["link"])

    all_problem_info = contests_by_length[1] + contests_by_length[2] + \
        contests_by_length[3] + contests_by_length[4]

    return all_problem_info


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user1 = request.form.get('user1')
        user2 = request.form.get('user2')

        user1_submissions = scrape_codeforces_submissions(user1)
        user2_submissions = scrape_codeforces_submissions(user2)
        unique_items = [
            item for item in user1_submissions if item not in user2_submissions]
        unique_items_2 = [
            item for item in user2_submissions if item not in user1_submissions]
        return render_template('index.html', user1=user1, user2=user2, user1_submissions=user1_submissions, user2_submissions=user2_submissions, unique_items=unique_items, unique_items_2=unique_items_2)

    return render_template('index.html', user1=None, user2=None, user1_submissions=None, user2_submissions=None, unique_items=None, unique_items_2=None)


if __name__ == '__main__':
    app.run(debug=True)

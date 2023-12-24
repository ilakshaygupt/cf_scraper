from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_contest_and_problem_code(link):
    parts = link.split("/")
    return parts[4], parts[6]

def scrape_codeforces_submissions(username, total_pages):
    contests_by_length = {1: [], 2: [], 3: [], 4: []}

    for page in range(1, total_pages + 1):
        url = f"https://codeforces.com/submissions/{username}/page/{page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            problem_cells = soup.find_all("td", class_="status-small", attrs={"data-problemid": True})

            for cell in problem_cells:
                if cell.find("a"):
                    link = "https://codeforces.com" + cell.find("a")["href"]
                    contest_id, problem_code = extract_contest_and_problem_code(link)
                    contests_by_length[len(contest_id)].append({"link": link, "text": f"{contest_id} - {cell.find('a').get_text(strip=True)} "})

            print(f"Page {page} processed for {username}.")
        else:
            print(f"Failed to retrieve the page {page} for {username}. Status code: {response.status_code}")
        contests_by_length[1].sort(key=lambda x: x["link"])
        contests_by_length[2].sort(key=lambda x: x["link"])
        contests_by_length[3].sort(key=lambda x: x["link"])
        contests_by_length[4].sort(key=lambda x: x["link"])
    
    all_problem_info = contests_by_length[1] + contests_by_length[2] + contests_by_length[3] + contests_by_length[4]

    return all_problem_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user1 = request.form.get('user1')
        user2 = request.form.get('user2')
        total_pages = int(request.form.get('total_pages')) 
        user1_submissions = scrape_codeforces_submissions(user1, total_pages)
        user2_submissions = scrape_codeforces_submissions(user2, total_pages)

        return render_template('index.html', user1=user1, user2=user2, user1_submissions=user1_submissions, user2_submissions=user2_submissions)
    
    return render_template('index.html', user1=None, user2=None, user1_submissions=None, user2_submissions=None)

if __name__ == '__main__':
    app.run(debug=True)
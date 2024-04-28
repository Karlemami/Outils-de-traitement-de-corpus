import requests
from pathlib import Path
from dataclasses import dataclass

@dataclass
class File:
    size: int
    sha: str
    language: str
    file_path_in_repo: str
    repo_url: str
    repo_licences: list[str]
    stars_count: int
    issues_count: int
    forks_count: int
    content: str
    # avg_line_length: float
    # max_line_length: int

def scrapper(language, nb_of_repos, headers):
    """Fetch the n most starred repositories containing a given language on Github"""
    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={nb_of_repos}"
    response = requests.get(url, headers=headers)
    repos = response.json()["items"]
    return repos


def download_files_recursively(folder, extension, headers):
    """
    Download all files in a folder and its subfolders with a given extension
    Files are downloaded dynamically to avoid saving no files after waiting for a long time in case of an error
    """
    files = requests.get(folder, headers=headers).json()
    print(folder)
    files_content = []
    for item in files:
        if item["type"] == "file":
            file_path = Path(item["name"])
            if file_path.suffix == extension:
                files_content.append(download_file(item, headers))
        elif item["type"] == "dir":
            files_content.extend(download_files_recursively(
                folder=item["url"],
                extension=extension,
                headers=headers,
            ))
    return files_content


def download_file(file,headers):
    """Download files to a given directory"""
    file_response = requests.get(file["download_url"], headers=headers)
    if file_response.status_code == 200:
        return [file_response.text, file["size"], file["sha"], file["path"]]


def main():
    import argparse
    import json

    extensions = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "c++": ".cpp",
        "c": ".c",
        "rust": ".rs",
    }

    parser = argparse.ArgumentParser(
        description="Scrap the most starred repositories containing a given language on Github"
    )
    parser.add_argument(
        "language",
        type=str,
        choices=list(extensions.keys()),
        help="The language to scrap",
    )
    parser.add_argument(
        "nb_of_repos", type=int, help="The number of repositories to scrap"
    )
    parser.add_argument(
        "-j","--json", type=str, help="The csv file to save the data"
    )
    parser.add_argument(
        "-pat",
        "--personal-access-token",
        type=str,
        help="you github personal access token, in case you reached the guest api limit",
    )
    args = parser.parse_args()

    if args.personal_access_token:
        headers = {"Authorization": f"token {args.personal_access_token}"}
    else:
        headers = None

    repos = scrapper(args.language, args.nb_of_repos, headers)
    files = []
    for repo_index in range(len(repos) - 1):
        print("Crawling through repo number", repo_index + 1)
        repo_info = requests.get(f"https://api.github.com/repos/{repos[repo_index]['full_name']}",headers=headers).json()
        repo_api_link = f"https://api.github.com/repos/{repos[repo_index]['full_name']}/contents/"

        repo_files = download_files_recursively(
            folder=repo_api_link,
            extension=extensions[args.language],
            headers=headers,
        )
        for file in repo_files:
        
            file_obj = File(
            content=file[0],
            size=file[1],
            sha=file[2],
            language=args.language,
            file_path_in_repo=file[3],
            repo_url=repo_info["html_url"],
            repo_licences=repo_info.get("license", {}).get("spdx_id", []),
            stars_count=repo_info["stargazers_count"],
            issues_count=repo_info["open_issues_count"],
            forks_count=repo_info["forks_count"],
            # avg_line_length=calculate_avg_line_length(file_response.text),
            # max_line_length=calculate_max_line_length(file_response.text)
        )
            with open(args.json, 'a') as f:
                f.write(json.dumps(file_obj.__dict__))
                f.write('\n')


if __name__ == "__main__":
    main()

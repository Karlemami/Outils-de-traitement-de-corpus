import requests
from pathlib import Path


def scrapper(language, nb_of_repos, headers):
    """Fetch the n most starred repositories containing a given language on Github"""
    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={nb_of_repos}"
    response = requests.get(url, headers=headers)
    repos = response.json()["items"]
    return repos


def download_files_recursively(folder, extension, headers, save_directory):
    """
    Download all files in a folder and its subfolders with a given extension
    Files are downloaded dynamically to avoid saving no files after waiting for a long time in case of an error
    """
    folder = requests.get(folder, headers=headers).json()
    for item in folder:
        if item["type"] == "file":
            file_path = Path(item["name"])
            if file_path.suffix == extension:
                download_file(item, save_directory, headers)
        elif item["type"] == "dir":
            download_files_recursively(
                folder=item["url"],
                extension=extension,
                headers=headers,
                save_directory=save_directory,
            )


def download_file(file, directory, headers):
    """Download files to a given directory"""
    file_response = requests.get(file["download_url"], headers=headers)
    if file_response.status_code == 200:
        with open(f'{directory}/{file["sha"]}_{file["name"]}', "w") as f:
            f.write(file_response.text)


def main():
    import argparse

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
        "download_directory",
        type=str,
        help="path to the directory where the files are to be downloaded. The folder must already exist",
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
    for repo_index in range(len(repos) - 1):
        print("Crawling through repo number", repo_index + 1)
        repo_api_link = f"https://api.github.com/repos/{repos[repo_index]['full_name']}/contents/"

        download_files_recursively(
            folder=repo_api_link,
            extension=extensions[args.language],
            headers=headers,
            save_directory=args.download_directory,
        )


if __name__ == "__main__":
    main()

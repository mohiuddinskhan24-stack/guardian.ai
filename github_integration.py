from github import Github

g = Github("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")

def get_repo_files(repo_name):
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")
    
    files = []
    
    for content in contents:
        if content.type == "file":
            files.append((content.name, content.decoded_content.decode()))
    
    return files
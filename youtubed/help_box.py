def help_box():
    box_width = 70
    lines = [
        "YouTubed - A simple youtube downloader",
        "-" * (box_width - 2),
        "",
        "To run this script, you need to install:",
        "",
        "Git: https://git-scm.com/downloads",
        "Python: https://www.python.org/downloads",
        "Poetry: https://python-poetry.org/docs/#installation",
        "",
        "After installing all the dependencies, run:",
        "",
        "git clone https://github.com/mauriciobellon/youtubed.git",
        "cd youtubed",
        "poetry install",
        "poetry run youtubed **url**",
        "",
        "-" * (box_width - 2),
        "Made by Mauricio Bellon",
    ]
    print("")
    print("  +" + "-" * (box_width - 2) + "+")
    for line in lines:
        print("  |" + line.center(box_width - 2) + "|")
    print("  +" + "-" * (box_width - 2) + "+")
    print("")
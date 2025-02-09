import sys
from pathlib import Path

from score import Score, ScoreArchive

if __name__ == "__main__":
    scores = [Score(s) for s in Path(sys.argv[1]).iterdir()]
    scorearchive = ScoreArchive.from_scores(scores).sort() 
    html_page = scorearchive.to_html()
    with open("partituras.html", "w") as f:
        f.write(html_page)


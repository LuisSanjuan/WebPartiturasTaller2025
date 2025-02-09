import sys
from pathlib import Path

from score import Score, ScoreRecord

if __name__ == "__main__":
    score = Score(Path(sys.argv[1]))
    scorerecord = ScoreRecord.from_score(score)
    html_page = scorerecord.to_html()
    with open("partituras.html", "w") as f:
        f.write(html_page)


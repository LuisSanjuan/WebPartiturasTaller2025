from collections import UserList
from dataclasses import dataclass, field, KW_ONLY
from itertools import zip_longest
from pathlib import Path
from typing_extensions import ClassVar, Self # in >3.10: from typing ...

from lark import Lark, Token, Transformer
from jinja2 import Template
from pymupdf import Document as PdfDocument

COVERS_DIR = Path("img")
COVER_FORMAT = ".png"

# Grammar for score filenames
GRAMMAR = """
    score: composer "_" work ("_" editor)?
    
    composer: words
    work: words
    editor: words
    
    words: word ("-" word)*
    word: SUBWORD ("+" SUBWORD)*
    
    SUBWORD: /[^-+_]+/
    
    %import common.WS
    %ignore WS
    """

# HTML templates
SCORE_HTML_TEMPLATE = """
    <article class="score-record">
      <div class="score-link">
        <a download href="{{scorerecord.score.path}}"></a>
      </div>
      <div class="score-info">
        <p class="composer">{{scorerecord.composer}}</p>
        <p class="work">{{scorerecord.work}}</p>
        <p class="editor">{{scorerecord.editor}}</p>
      </div>
    </article>
    """

ARCHIVE_HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <title>Web Partituras</title>
      <meta charset="utf-8">
      <link href="css/score.css" rel="stylesheet">
    </head>
    <body>
      <h1>Web Partituras</h1>
      <section class="score-archive">
      {% for scorerecord in scorearchive %}
        <article class="score-record">
          <div class="score-link"
               style="background-image: url({{scorerecord.score.cover}})">
            <a download href="{{scorerecord.score.path}}"></a>
          </div>
          <div class="score-info">
            <p class="composer">{{scorerecord.composer}}</p>
            <p class="work">{{scorerecord.work}}</p>
            <p class="editor">{{scorerecord.editor}}</p>
          </div>
        </article>
      {% endfor %}
      </section>
    </body>
    </html>
    """

@dataclass
class Score:
    path: Path
    name: str = field(init=False)
    cover: Path = field(init=False)
    _: KW_ONLY
    with_cover: bool = True

    def __post_init__(self):
        self.name = self.path.stem
        self.cover = Path(COVERS_DIR, self.name).with_suffix(COVER_FORMAT)
        if self.with_cover:
            CoverGenerator(self.path, self.cover).make_cover() 

    def to_dict(self) -> dict:
        """Convert the Score name into a dictionary."""
        parser = Lark(GRAMMAR, start="score")
        tree = parser.parse(self.name)
        scoreinfo = ScoreNameTransformer().transform(tree)
        return scoreinfo | {"score": self}

@dataclass
class ScoreRecord:
    composer: str
    work: str
    editor: str
    score: Score 

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        """Construct a ScoreRecord from the given dictionary."""
        return cls(**d) 
 
    @classmethod
    def from_score(cls, s: Score) -> Self:
        """Construct a ScoreRecord from the given score."""
        return cls.from_dict(s.to_dict())
    
    def to_html(self) -> str:
        """Convert the ScoreRecord into an HTML element."""
        return Template(SCORE_HTML_TEMPLATE).render(scorerecord=self)

class ScoreNameTransformer(Transformer):
    FIELDS: ClassVar[list[str]] = ["composer", "work", "editor"]

    def score(self, items: list[str]) -> dict:
        return dict(zip_longest(self.FIELDS, items, fillvalue=""))

    def words(self, items: list[str]) -> str:
        return " ".join(items)

    def word(self, items: list[Token]) -> str:
        return "-".join(items)

    composer = words
    work = words
    editor = words

class ScoreArchive(UserList):
    @classmethod
    def from_scores(cls, scores: list[Score]) -> Self:
        """Construct the ScoreArchive from the given scores."""
        return cls([ScoreRecord.from_score(s) for s in scores])

    def sort(self) -> Self:
        """Sort the ScoreRecord by composer and work."""
        def composer_and_work(sr: ScoreRecord) -> tuple:
            composer_names = sr.composer.split(" ")
            composer_last_name = composer_names[-1]
            composer_first_name = composer_names[:-1]
            return (composer_last_name, composer_first_name, sr.work)
        return ScoreArchive(sorted(self, key=composer_and_work))

    def to_html(self) -> str:
        """Convert the ScoreArchive into an HTML element."""
        return Template(ARCHIVE_HTML_TEMPLATE).render(scorearchive=self)

@dataclass
class CoverGenerator:
    pdf: Path
    cover: Path

    def make_cover(self) -> None:
        """Creates a cover from pdf if it does not exist and
        save it to cover."""
        if not self.cover.exists():
            print(f"Creating cover for {self.pdf} ...")
            cover_image = PdfDocument(self.pdf).get_page_pixmap(0)
            cover_image.save(self.cover)


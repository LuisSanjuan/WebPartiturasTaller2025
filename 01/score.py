from dataclasses import dataclass, field
from itertools import zip_longest
from pathlib import Path
from typing_extensions import ClassVar, Self # in >3.10: from typing ...

from lark import Lark, Token, Transformer
from jinja2 import Template

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

# Score HTML template
HTML_TEMPLATE = """
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

@dataclass
class Score:
    path: Path
    name: str = field(init=False)

    def __post_init__(self):
        self.name = self.path.stem

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
        return Template(HTML_TEMPLATE).render(scorerecord=self)

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


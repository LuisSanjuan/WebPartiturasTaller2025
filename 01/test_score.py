import pytest
from pathlib import Path
from score import Score, ScoreRecord

# Examples --------------------------------------------------------------
## Score
@pytest.fixture
def score1():
    return Score(Path("Heitor-Villa+Lobos_Preludio-1_Max-Eschig.pdf"))

@pytest.fixture
def score2():
    return Score(Path("Heitor-Villa+Lobos_Preludio-1.pdf"))

## score dict
@pytest.fixture
def scoredict1(score1):
    return {
        "composer": "Heitor Villa-Lobos",
        "work": "Preludio 1",
        "editor": "Max Eschig",
        "score": score1
    }

@pytest.fixture
def scoredict2(score2):
    return {
        "composer": "Heitor Villa-Lobos",
        "work": "Preludio 1",
        "editor": "",
        "score": score2
    }

## ScoreRecord
@pytest.fixture
def scorerecord1(score1):
    return ScoreRecord(
        composer="Heitor Villa-Lobos",
        work="Preludio 1",
        editor="Max Eschig",
        score=score1
    )

## HTML
@pytest.fixture
def scorehtml1():
    return """
        <article class="score-record">
          <div class="score-link">
            <a download href="Heitor-Villa+Lobos_Preludio-1_Max-Eschig.pdf">
            </a>
          </div>
          <div class="score-info">
            <p class="composer">Heitor Villa-Lobos</p>
            <p class="work">Preludio 1</p>
            <p class="editor">Max Eschig</p>
          </div>
        </article>
        """

# Utils -----------------------------------------------------------------
def normalize_html(element):
    """Format HTML element to a single line."""
    return "".join([s.strip() for s in element.split("\n")])

# Tests -----------------------------------------------------------------
## Score methods
def test_score_to_dict(score1, scoredict1, score2, scoredict2):
    assert score1.to_dict() == scoredict1
    assert score2.to_dict() == scoredict2

## ScoreRecord methods
def test_scorerecord_from_dict(scoredict1, scorerecord1):
    assert ScoreRecord.from_dict(scoredict1) == scorerecord1

def test_scorerecord_from_score(score1, scorerecord1):
    assert ScoreRecord.from_score(score1) == scorerecord1

def test_scorerecord_to_html(scorerecord1, scorehtml1):
    assert (
        normalize_html(scorerecord1.to_html()) 
        == normalize_html(scorehtml1)
    )


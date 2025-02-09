import pytest
from pathlib import Path
from score import Score, ScoreRecord, ScoreArchive

# Examples --------------------------------------------------------------
## Score
@pytest.fixture
def score1():
    return Score(Path("Heitor-Villa+Lobos_Preludio-1_Max-Eschig.pdf"))

@pytest.fixture
def score2():
    return Score(Path("Heitor-Villa+Lobos_Preludio-1.pdf"))

@pytest.fixture
def score3():
    return Score(Path("Francisco-Tárrega_Adelita.pdf"))

@pytest.fixture
def score4():
    return Score(Path("Francesco-da-Milano_Fantasía_Ruggero-Chiesa.pdf"))

@pytest.fixture
def score5():
    return Score(Path("Anónimo_Greensleeves.pdf"))

@pytest.fixture
def score6():
    return Score(Path("Johann-Sebastian-Bach_Sarabande-BWV-995.pdf"))

@pytest.fixture
def score7():
    return Score(Path("Johann-Sebastian-Bach_Preludio-BWV-999.pdf"))

@pytest.fixture
def score8():
    return Score(Path("Carl-Philipp-Emanuel-Bach_Sonata.pdf"))

## list of Score
@pytest.fixture
def scores1(score3, score4, score5):
    return [score3, score4, score5]

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

@pytest.fixture
def scorerecord3(score3):
    return ScoreRecord.from_score(score3)

@pytest.fixture
def scorerecord4(score4):
    return ScoreRecord.from_score(score4)

@pytest.fixture
def scorerecord5(score5):
    return ScoreRecord.from_score(score5)

@pytest.fixture
def scorerecord6(score6):
    return ScoreRecord.from_score(score6)

@pytest.fixture
def scorerecord7(score7):
    return ScoreRecord.from_score(score7)

@pytest.fixture
def scorerecord8(score8):
    return ScoreRecord.from_score(score8)

## ScoreArchive
@pytest.fixture
def scorearchive1(scorerecord3, scorerecord4, scorerecord5):
    return ScoreArchive([scorerecord3, scorerecord4, scorerecord5])

@pytest.fixture
def scorearchive2(scorerecord3, scorerecord5, scorerecord6, 
                  scorerecord7, scorerecord8):
    return ScoreArchive([scorerecord6, scorerecord5, scorerecord3,
                         scorerecord7, scorerecord8])

@pytest.fixture
def scorearchive3(scorerecord3, scorerecord5, scorerecord6, 
                  scorerecord7, scorerecord8):
    return ScoreArchive([scorerecord5, scorerecord8, scorerecord7,
                         scorerecord6, scorerecord3])

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

@pytest.fixture
def scorearchivehtml1():
    return """
        <section class="score-archive">
          <article class="score-record">
              <div class="score-link">
                <a download href="Francisco-Tárrega_Adelita.pdf">
                </a>
              </div>
              <div class="score-info">
                <p class="composer">Francisco Tárrega</p>
                <p class="work">Adelita</p>
                <p class="editor"></p>
              </div>
          </article>
          <article class="score-record">
              <div class="score-link">
                <a download href="Francesco-da-Milano_Fantasía_Ruggero-Chiesa.pdf">
                </a>
              </div>
              <div class="score-info">
                <p class="composer">Francesco da Milano</p>
                <p class="work">Fantasía</p>
                <p class="editor">Ruggero Chiesa</p>
              </div>
          </article>
          <article class="score-record">
              <div class="score-link">
                <a download href="Anónimo_Greensleeves.pdf">
                </a>
              </div>
              <div class="score-info">
                <p class="composer">Anónimo</p>
                <p class="work">Greensleeves</p>
                <p class="editor"></p>
              </div>
          </article>
        </section>
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

## ScoreArchive methods
def test_scorearchive_from_scores(scores1, scorearchive1):
    assert ScoreArchive.from_scores(scores1) == scorearchive1
        
def test_scorearchive_sort(scorearchive2, scorearchive3):
    assert scorearchive2.sort() == scorearchive3

def test_scorearchive_to_html(scorearchive1, scorearchivehtml1):
    assert (
        normalize_html(scorearchive1.to_html()) 
        == normalize_html(scorearchivehtml1)
    )


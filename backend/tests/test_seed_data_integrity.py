from __future__ import annotations

from collections import Counter

from app.seeds.data.artifacts import ARTIFACTS
from app.seeds.data.discoveries import DISCOVERIES
from app.seeds.data.galaxies import GALAXIES
from app.seeds.data.planets import PLANETS
from app.seeds.data.practices import PRACTICES
from app.seeds.data.quizzes import QUIZ_QUESTIONS


def test_python_galaxy_seed_counts_are_complete() -> None:
    assert len(GALAXIES) == 1
    assert len(PLANETS) == 6
    assert len(DISCOVERIES) == 30
    assert len(PRACTICES) == 30
    assert len(QUIZ_QUESTIONS) == 60
    assert len(ARTIFACTS) == 6


def test_seed_keys_are_unique_within_each_dataset() -> None:
    datasets = [GALAXIES, PLANETS, DISCOVERIES, PRACTICES, QUIZ_QUESTIONS, ARTIFACTS]
    for dataset in datasets:
        keys = [item["key"] for item in dataset]
        assert len(keys) == len(set(keys))


def test_each_python_planet_has_expected_content_counts() -> None:
    planet_keys = [planet["key"] for planet in PLANETS]

    discovery_counts = Counter(discovery["planet_key"] for discovery in DISCOVERIES)
    practice_counts = Counter(practice["planet_key"] for practice in PRACTICES)
    quiz_counts = Counter(question["planet_key"] for question in QUIZ_QUESTIONS)

    assert set(planet_keys) == set(discovery_counts) == set(practice_counts) == set(quiz_counts)
    assert all(count == 5 for count in discovery_counts.values())
    assert all(count == 5 for count in practice_counts.values())
    assert all(count == 10 for count in quiz_counts.values())


def test_planet_artifact_links_are_complete() -> None:
    artifact_keys = {artifact["key"] for artifact in ARTIFACTS}
    planet_artifact_keys = {planet["artifact_key"] for planet in PLANETS}

    assert None not in planet_artifact_keys
    assert planet_artifact_keys.issubset(artifact_keys)

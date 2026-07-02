from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz_question import QuizQuestion
from app.seeds.data.quizzes import QUIZ_QUESTIONS, QuizQuestionSeedData
from app.seeds.utils import (
    SeedContext,
    SeedStats,
    add_all_and_flush,
    fetch_existing_by_composite,
    require_mapping_value,
)


class QuizSeeder:
    """Seeds quiz question records into the database."""

    label = "Quiz Questions"

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    async def seed(self, session: AsyncSession, context: SeedContext) -> SeedStats:
        """Seeds quiz questions using resolved planet references."""

        stats = SeedStats(label=self.label)
        quiz_records: tuple[QuizQuestionSeedData, ...] = QUIZ_QUESTIONS
        if not quiz_records:
            return stats

        resolved_records: list[tuple[QuizQuestionSeedData, UUID]] = []
        composite_keys: list[tuple[UUID, int]] = []
        for record in quiz_records:
            planet_id = require_mapping_value(context.planet_ids, record["planet_key"], entity_label="planet")
            resolved_records.append((record, planet_id))
            composite_keys.append((planet_id, record["order_number"]))

        existing_by_key = await fetch_existing_by_composite(
            session=session,
            model=QuizQuestion,
            columns=(QuizQuestion.planet_id, QuizQuestion.order_number),
            keys=composite_keys,
        )

        new_models: list[QuizQuestion] = []
        pending_keys: list[str] = []
        for record, planet_id in resolved_records:
            composite_key = (planet_id, record["order_number"])
            existing = existing_by_key.get(composite_key)
            if existing is not None:
                context.quiz_question_ids[record["key"]] = existing.id
                stats.skipped += 1
                continue

            question = QuizQuestion(
                planet_id=planet_id,
                question_text=record["question_text"],
                question_type=record["question_type"],
                options=record["options"],
                correct_answer=record["correct_answer"],
                explanation=record["explanation"],
                difficulty=record["difficulty"],
                xp_reward=record["xp_reward"],
                order_number=record["order_number"],
            )
            new_models.append(question)
            pending_keys.append(record["key"])

        await add_all_and_flush(session, new_models)
        for record_key, question in zip(pending_keys, new_models, strict=True):
            context.quiz_question_ids[record_key] = question.id
        stats.inserted = len(new_models)
        return stats

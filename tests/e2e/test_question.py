from app.core.database import get_session
from asgi import app
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_question_creation_deletion(async_db_session):
    async with AsyncClient(app=api, base_url="http://localhost:8080") as ac:

        # Create a topic
        response = await ac.post("/quiz/api/v1/topics", json={"title": "Test Topic", "description": "Test Description"})
        topic_id = response.json()['id']

       # Create a question
        response = await ac.post("/quiz/api/v1/questions", json={
            "difficulty": "easy",
            "is_verified": True,
            "points": 1,
            "question_text": "What is a common cause of syntax errors in TypeScript?",
            "question_type": "single_select_mcq",
            "topic_id": topic_id
        })
        assert response.status_code == 200
        assert response.json()[
            "question_text"] == "What is a common cause of syntax errors in TypeScript?"

        await ac.delete(f"/quiz/api/v1/questions/{response.json()['id']}")
        await ac.delete(f"/quiz/api/v1/topics/{topic_id}")

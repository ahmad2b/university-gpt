from fastapi import APIRouter, Query, HTTPException, status

from app.api.deps import AsyncSessionDep
from app.crud.topic_crud import content_crud, topic_crud

from app.models.topic_models import (
    TopicCreate,
    TopicResponse,
    TopicUpdate,
    TopicResponseWithContent,
    ContentCreate,
    ContentResponse,
    ContentUpdate,
)
from app.core.config import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("", response_model=TopicResponseWithContent)
async def create_new_topic(topic: TopicCreate, db: AsyncSessionDep):
    """
    Create a new recursive topic.

    Args:
        topic (TopicCreate): The topic data to create.

    Returns:
        TopicResponse: The created topic.

    Raises:
        HTTPException: If an error occurs while creating the topic.
    """
    logger.info("%s.create_a_topic: %s", __name__, topic)
    try:
        created_topic = await topic_crud.create_topic(topic=topic, db=db)
        return created_topic
    except (
        ValueError
    ) as e:  # Catching the custom ValueError raised from CRUD operations
        logger.error(f"Error creating topic: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as httperr:
        logger.error(f"Error creating topic: {httperr}")
        raise httperr
    except Exception as e:  # Catching any unexpected errors
        logger.error(f"Unexpected error creating topic: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Get all Topics


@router.get("", response_model=list[TopicResponse])
async def get_all_topics(
    db: AsyncSessionDep,
    offset: int = Query(default=0, lte=10),
    limit: int = Query(default=10, lte=100),
):
    """
    Get all topics.

    Args:
        offset (int, optional): The offset for pagination. Defaults to 0.
        limit (int, optional): The limit for pagination. Defaults to 100.

    Returns:
        list[TopicResponse]: The list of topics.

    Raises:
        HTTPException: If an error occurs while retrieving topics.
    """
    logger.info("%s.get_topics: triggered", __name__)
    try:
        topics = await topic_crud.read_topics(offset=offset, limit=limit, db=db)
        return topics
    except HTTPException as http_err:
        logger.error(f"Error retrieving topics: {http_err}")
        raise http_err  # Re-raise the HTTPException with the original status code and detail
    except Exception as e:
        logger.error(f"Unexpected error retrieving topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics.")


# Get a Topic by ID
@router.get("/{topic_id}", response_model=TopicResponseWithContent)
async def get_topic_and_its_content_by_id(topic_id: int, db: AsyncSessionDep):
    """
    Get a Topic and its Content by ID.

    Args:
        topic_id (int): The ID of the topic.

    Returns:
        TopicResponse: The topic with the specified ID.
    """
    logger.info("%s.get_topic_by_id: %s", __name__, topic_id)
    try:
        return await topic_crud.read_topic_by_id(id=topic_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error retrieving topic: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topic.")


# Get all topics and subtopics


@router.get("/{topic_id}/subtopics")
async def get_topic_and_subtopics(topic_id: int, db: AsyncSessionDep):
    logger.info("%s.get_topic_and_subtopics: %s", __name__, topic_id)
    try:
        return await topic_crud.read_topic_and_subtopics(id=topic_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error retrieving topics: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topics.")


# Update a Topic by ID
@router.patch("/{topic_id}", response_model=TopicResponse)
async def update_topic_by_id(topic_id: int, topic: TopicUpdate, db: AsyncSessionDep):
    """
    Update a topic by ID.

    Args:
        topic_id (int): The ID of the topic to update.
        topic (TopicUpdate): The updated topic data.

    Returns:
        TopicResponse: The updated topic.
    """
    logger.info("%s.update_topic_by_id: %s", __name__, topic_id)
    try:
        return await topic_crud.update_topic(id=topic_id, topic=topic, db=db)
    except ValueError as e:
        logger.error(f"Error updating topic: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to update topic.")


# Delete a Topic by ID


@router.delete("/{topic_id}")
async def delete_topic_by_id(topic_id: int, db: AsyncSessionDep):
    """
    Delete a topic by ID.

    Args:
        topic_id (int): The ID of the topic to delete.
    """
    logger.info("%s.delete_topic_by_id: %s", __name__, topic_id)
    try:
        return await topic_crud.delete_topic(id=topic_id, db=db)
    except HTTPException as http_err:
        logger.error(f"Error deleting topic: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error deleting topic: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete topic.")


# Create new Content for a Topic
@router.post("/content", response_model=ContentResponse)
async def create_content_for_topic(content: ContentCreate, db: AsyncSessionDep):
    """
    Create a new content for a topic.

    Args:
        content (ContentCreate): The content data to create that is topic_id and content_text.

    Returns:
        ContentResponse: The created content.
    """
    logger.info("%s.create_content_for_topic: %s", __name__, content)
    try:
        return await content_crud.create_new_content(content=content, db=db)
    except HTTPException as http_ex:
        # Reraise the HTTPException to be handled by FastAPI
        raise http_ex
    except Exception as ex:
        logger.error(f"Unexpected error occurred while creating content: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


# Get all Content for a Topic


@router.get("/{topic_id}/content", response_model=list[ContentResponse])
async def get_content_for_topic(topic_id: int, db: AsyncSessionDep):
    """
    Get all content for a topic.

    Args:
        topic_id (int): The ID of the topic.

    Returns:
        list[ContentResponse]: The list of content for the topic.
    """
    logger.info("%s.get_content_for_topic: %s", __name__, topic_id)
    try:
        all_contents = await content_crud.read_content_for_topic(
            topic_id=topic_id, db=db
        )
        print(all_contents)
        return all_contents

    except HTTPException as http_err:
        logger.error(f"Error retrieving content: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving content: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content.")


# Get a Content by ID


@router.get("/{topic_id}/content/{content_id}", response_model=ContentResponse)
async def call_get_content_by_id(topic_id: int, content_id: int, db: AsyncSessionDep):
    """
    Get a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content.
       db (optional) : Database Dependency Injection.

    Returns:
        ContentResponse: The content with the specified ID.
    """
    logger.info("%s.get_content_by_id: %s", __name__, content_id)
    try:
        return await content_crud.get_content_by_id(
            topic_id=topic_id, content_id=content_id, db=db
        )
    except HTTPException as http_err:
        logger.error(f"Error retrieving content: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error retrieving content: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve content.")


# Update a Content by ID


@router.patch("/content/{content_id}", response_model=ContentResponse)
async def update_content_by_id(
    content_id: int, content: ContentUpdate, db: AsyncSessionDep
):
    """
    Update a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content to update.
        content (ContentUpdate): The updated content data.
       db (optional) : Database Dependency Injection.

    Returns:
        ContentResponse: The updated content.
    """
    logger.info("%s.update_content_by_id: %s", __name__, content_id)
    try:
        return await content_crud.update_content(id=content_id, content=content, db=db)
    except HTTPException as http_err:
        logger.error(f"Error updating content: {http_err}")
        raise http_err
    except Exception as e:
        logger.error(f"Unexpected error updating content: {e}")
        raise HTTPException(status_code=500, detail="Failed to update content.")


# Delete a Content by ID


@router.delete("/content/{content_id}")
async def delete_content_by_id(content_id: int, db: AsyncSessionDep):
    """
    Delete a content by ID.

    Args:
        topic_id (int): The ID of the topic.
        content_id (int): The ID of the content to delete.
       db (optional) : Database Dependency Injection.
    """
    logger.info("%s.delete_content_by_id: %s", __name__, content_id)
    return await content_crud.delete_content(id=content_id, db=db)

from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# @router.get("/posts/latest")
# async def get_latest_post():
#    post = posts[len(posts)-1]
#    return { "data": post }


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    # post = cursor.fetchone()
    # db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post).get(id)
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message": "Post does not found" }
    
    return post


# @router.post("/posts")
# async def create_post(body: dict = Body(...)):
#    print(body)
#    return { "data": f"title {body['title']} content {body['content']}" }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(1, 1000000)
    # print(post.dict())
    # posts.append(post_dict)
    # cursor.execute(""" 
    #    INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #    (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found" )

    # posts.pop(index)
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    #cursor.execute(""" 
    #    UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
    #    (post.title, post.content, post.published, str(id)))
    #post = cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()

    if old_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found" )

    # post_dict = post.dict()
    # post_dict['id'] = id
    # posts[index] = post_dict
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
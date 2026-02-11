from fastapi import APIRouter, HTTPException
from ..examples import get_example_list, get_example_by_id

router = APIRouter(prefix="/api/examples", tags=["examples"])


@router.get("")
async def list_examples():
    return get_example_list()


@router.get("/{example_id}")
async def get_example(example_id: str):
    example = get_example_by_id(example_id)
    if example is None:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

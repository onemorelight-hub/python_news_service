from fastapi import APIRouter, HTTPException, Body, Query

from services.auto_correct_service import get_candidates, autocomplete, correct, auto_suggest

router = APIRouter()


@router.get("/autocorrect/v1")
def autocorrect_endpoint(word: str = Query(..., description="Misspelled word")):
    return {
        "input": word,
        "suggestions": get_candidates(word)
    }


@router.get("/autocorrect/v1/correct")
def autocorrect_endpoint(word: str = Query(..., description="Misspelled word")):
    return {
        "input": word,
        "suggestions": correct(word)
    }


@router.get("/autocomplete/v1")
def autocomplete_endpoint(prefix: str = Query(..., description="Prefix for autocomplete")):
    return {
        "prefix": prefix,
        "completions": autocomplete(prefix)
    }


@router.get("/autocorrect/v1/suggest")
def autocorrect_endpoint(word: str = Query(..., description="Misspelled word")):
    return {
        "input": word,
        "suggestions": auto_suggest(word)
    }

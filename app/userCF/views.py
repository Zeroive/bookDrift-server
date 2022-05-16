from flask import Blueprint
from app.userCF.models import RECOMMENDER


userCF = Blueprint('userCF', __name__, url_prefix="/userCF")
UserRecommendService =
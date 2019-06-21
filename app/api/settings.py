from flask import (
   Blueprint, g, request, abort, jsonify)
from app import mongo
from flask_jwt_extended import (
    jwt_required, create_access_token, get_current_user
)
from app import token
from bson import ObjectId
from app.util import serialize_doc


bp = Blueprint('system', __name__, url_prefix='/system')


@bp.route('/settings', methods=['POST'])
@jwt_required
def settings():
 user = get_current_user()
 if user["role"] == "Admin":   
    if not request.json:
        abort(500)
    integrate_with_hr = request.json.get('integrate_with_hr', False)
    if integrate_with_hr is True:
        hr = mongo.db.hr.insert_one({
            "integrate_with_hr": integrate_with_hr
        }).inserted_id
        return jsonify(str(hr))
    else:
        hr = mongo.db.hr.update({
            "integrate_with_hr": True
        }, {
                "$unset": {
                     "integrate_with_hr": integrate_with_hr
                 }
             })
        return ("settings off")

   
#Api for slack token settings   
@bp.route('/slack_settings', methods=["PUT","GET"])
@jwt_required
@token.admin_required
def slack_setings():
    if request.method == "GET":
        users = mongo.db.slack_tokens.find({})
        users = [serialize_doc(doc) for doc in users]
        default = [{
        "slack_token":"xoxp-124720392913-124692552128-671654051172-e445a95943aec1a243e3f496d51ff454",
        "webhook_url":"https://hooks.slack.com/services/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",
        "secret_key":"3dd7fe8a6ea2ea9afb9a7366980253b7"
        }]
        return jsonify(default if not users else users)

    if request.method == "PUT":
        webhook_url = request.json.get("webhook_url")
        slack_token = request.json.get("slack_token")
        secret_key =request.json.get("secret_key")
        ret = mongo.db.slack_tokens.update({
        }, {
            "$set": {
                "webhook_url": webhook_url,
                "slack_token": slack_token,
                "secret_key":secret_key
            }
        },upsert=True)
        return jsonify(str(ret))

#Api for schdulers on off settings
@bp.route('/schdulers_settings', methods=["GET","PUT"])
@jwt_required
@token.admin_required
def schdulers_setings():
    if request.method == "GET":
        ret = mongo.db.schdulers_setting.find({
        })
        ret = [serialize_doc(doc) for doc in ret]
        default=[{
            "monthly_remainder":"Please create your monthly report",
            "weekly_remainder1":"you need to create your weekly",
            "weekly_remainder2":"You are past due your date for weekly report, you need to do your weekly report before Thursday. Failing to do so will automatically set your weekly review to 0 which will effect your overall score.",
            "review_activity":"you have weekly report's pending to be reviewed",
            "monthly_manager_reminder":"you have to be reviewed",
            "missed_checkin":"you have missed"
            }]
        return jsonify(default if not ret else ret)

    if request.method == "PUT":
        monthly_remainder = request.json.get("monthly_remainder")
        weekly_remainder = request.json.get("weekly_remainder")
        recent_activity = request.json.get("recent_activity")
        review_activity = request.json.get("review_activity")
        monthly_manager_reminder = request.json.get("monthly_manager_reminder")
        ret = mongo.db.schdulers_setting.update({
            },{
                "$set":{
                "monthly_remainder": monthly_remainder,
                "weekly_remainder": weekly_remainder,
                "recent_activity": recent_activity,
                "review_activity": review_activity,
                "monthly_manager_reminder": monthly_manager_reminder
            }}, upsert=True)
        return jsonify(str(ret))


#Api for schdulers mesg settings
@bp.route('/schduler_mesg', methods=["GET","PUT"])
@jwt_required
@token.admin_required
def slack_schduler():
    if request.method == "GET":
        ret = mongo.db.schdulers_msg.find({
        })
        ret = [serialize_doc(doc) for doc in ret]
        default=[{
            "monthly_remainder":"Please create your monthly report",
            "weekly_remainder1":"you need to create your weekly",
            "weekly_remainder2":"You are past due your date for weekly report, you need to do your weekly report before Thursday. Failing to do so will automatically set your weekly review to 0 which will effect your overall score.",
            "review_activity":"you have weekly report's pending to be reviewed",
            "monthly_manager_reminder":"you have to be reviewed",
            "missed_checkin":"you have missed"
            }]
        return jsonify(default if not ret else ret)
    if request.method == "PUT":
        monthly_remainder = request.json.get("monthly_remainder")
        weekly_remainder1 = request.json.get("weekly_remainder1")
        weekly_remainder2 = request.json.get("weekly_remainder2")
        review_activity = request.json.get("review_activity")
        monthly_manager_reminder = request.json.get("monthly_manager_reminder")
        missed_checkin = request.json.get("missed_checkin")
        ret = mongo.db.schdulers_msg.update({
        }, {
            "$set": {
                "monthly_remainder": monthly_remainder,
                "weekly_remainder1": weekly_remainder1,
                "weekly_remainder2":weekly_remainder2,
                "review_activity":review_activity,
                "monthly_manager_reminder":monthly_manager_reminder,
                "missed_checkin":missed_checkin
            }
        })
        return jsonify(str(ret))

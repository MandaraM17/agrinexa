from flask import Blueprint, request


voice_bp = Blueprint("voice", __name__)


@voice_bp.route("/", methods=["GET"])
def voice_home():

    return {
        "message": "Voice Input API is working!"
    }


@voice_bp.route("/process", methods=["POST"])
def process_voice():

    data = request.get_json()

    text = data.get("text")

    if not text:
        return {
            "error": "Voice text is required"
        }, 400

    text_lower = text.lower()

    if "price" in text_lower:

        response = "Please check the market price section for crop prices."

    elif "crop" in text_lower:

        response = "You can view your crops in the farmer dashboard."

    elif "worker" in text_lower:

        response = "You can find agricultural workers in the worker section."

    elif "disease" in text_lower:

        response = "Please provide the crop disease details for further assistance."

    else:

        response = "I understood your request, but I need more information."

    return {
        "input": text,
        "response": response
    }
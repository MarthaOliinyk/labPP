from src.app import app
from src.models import Tag
from src.utils.exception_wrapper import handle_server_exception


@app.route('/tag', methods=['GET'])
@handle_server_exception
def get_tags():
    return {'items': [Tag.to_json(tag) for tag in Tag.get_all()]}

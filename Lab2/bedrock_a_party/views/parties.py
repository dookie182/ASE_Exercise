from flakon import JsonBlueprint
from flask import abort, jsonify, request

from bedrock_a_party.classes.party import CannotPartyAloneError, ItemAlreadyInsertedByUser, NotExistingFoodError, NotInvitedGuestError, Party

parties = JsonBlueprint('parties', __name__)

_LOADED_PARTIES = {}  # dict of available parties
_PARTY_NUMBER = 0  # index of the last created party


@parties.route("/parties", methods=['POST','GET'])
def all_parties():
    result = None
    if request.method == 'POST':
        try:
            #Create a party 
            result = create_party(request)
        except CannotPartyAloneError:
            #Exception for handling empty party case
            abort(400)

    elif request.method == 'GET':
        #Returns all parties created
        result = get_all_parties()

    return result


@parties.route("/parties/loaded", methods=['GET'])
def loaded_parties():
    #Returns the number of parties currently loaded in the system
    return jsonify({'loaded_parties': len(_LOADED_PARTIES)})


@parties.route("/party/<id>", methods=['GET', 'DELETE'])
def single_party(id):
    global _LOADED_PARTIES
    result = ""

    #Check if the party is an existing one
    exists_party(id)

    if 'GET' == request.method:
        #Retrieve a party
        result = jsonify(_LOADED_PARTIES[id].serialize())

    elif 'DELETE' == request.method:
        #Delete a party
        del _LOADED_PARTIES[id]
        result = jsonify("Party Deleted!")


    return result


@parties.route("/party/<id>/foodlist", methods=['GET'])
def get_foodlist(id):
    global _LOADED_PARTIES
    result = ""

    #Check if the party is an existing one
    exists_party(id)

    if 'GET' == request.method:
        #Retrieve food list of the party
        result = jsonify({'foodlist':_LOADED_PARTIES[id].get_food_list().serialize()})

    return result


@parties.route("/party/<id>/foodlist/<user>/<item>", methods=['POST', 'DELETE'])
def edit_foodlist(id, user, item):
    global _LOADED_PARTIES

    #Check if the party is an existing one
    exists_party(id)
    #Retrieve the party
    tmpParty = _LOADED_PARTIES[id]
    result = ""

    if 'POST' == request.method:
        try:
           result = jsonify(tmpParty.add_to_food_list(item,user).serialize())
        except(NotInvitedGuestError):
            #Exception for handling add item to food list case from not invited guest
            abort(401)
        except(ItemAlreadyInsertedByUser):
            #Exception for handling the case when a guest tries to insert an item already inserted in the food list
            abort(400)
            
    if 'DELETE' == request.method:
        try:
            #Remove food from food list of a party
            tmpParty.remove_from_food_list(item,user)
            result = jsonify({'msg':"Food deleted!"})
        except(NotExistingFoodError):
            #Exception for handling the delete of a food not inserted in the food list
            abort(400)

    return result

#
# These are utility functions. Use them, DON'T CHANGE THEM!!
#

def create_party(req):
    global _LOADED_PARTIES, _PARTY_NUMBER

    # get data from request
    json_data = req.get_json()

    # list of guests
    try:
        guests = json_data['guests']
    except:
        raise CannotPartyAloneError("you cannot party alone!")

    # add party to the loaded parties lists
    _LOADED_PARTIES[str(_PARTY_NUMBER)] = Party(_PARTY_NUMBER, guests)
    _PARTY_NUMBER += 1

    return jsonify({'party_number': _PARTY_NUMBER - 1})


def get_all_parties():
    global _LOADED_PARTIES

    return jsonify(loaded_parties=[party.serialize() for party in _LOADED_PARTIES.values()])


def exists_party(_id):
    global _PARTY_NUMBER
    global _LOADED_PARTIES

    if int(_id) > _PARTY_NUMBER:
        abort(404)  # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(_id in _LOADED_PARTIES):
        abort(410)  # error 410: Gone, i.e. it existed but it's not there anymore

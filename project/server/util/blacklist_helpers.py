from datetime import datetime, timezone

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token
from project.database import db_scoped_session as db
from project.database.models import Blocklist

from .exceptions import TokenNotFound


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    # user_identity = decoded_token[identity_claim] # this is the original line ??
    user_identity = decoded_token['sub']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = Blocklist(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.add(db_token)
    db.commit()


def is_token_revoked(jwt_payload):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = jwt_payload["jti"]
    try:
        token = Blocklist.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    return Blocklist.query.filter_by(Blocklist.user_identity == user_identity).all()


def revoke_token(token_id, user):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = Blocklist.query.filter_by(
            id=token_id, user_identity=user).one()
        token.revoked = True
        db.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def unrevoke_token(token_id, user):
    """
    Unrevokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = Blocklist.query.filter_by(
            id=token_id, user_identity=user).one()
        token.revoked = False
        db.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def prune_database():
    """
    Delete tokens that have expired from the database.
    How (and if) you call this is entirely up you. You could expose it to an
    endpoint that only administrators could call, you could run it as a cron,
    set it up with flask cli, etc.
    """
    now = datetime.now()
    expired = Blocklist.query.filter(Blocklist.expires < now).all()
    for token in expired:
        db.delete(token)
    db.commit()
    print(len(expired), ' entries deleted')

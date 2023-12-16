"""Interface for the ida.models module."""
from .agent import Agent, Organization, Person
from .concept import Concept
from .content import ContentAttributes, ContentTypeExtended
from .entity_phrase import EntityPhrase
from .group import GroupProperties
from .headword import Headword
from .location import Location
from .object import Object, ObjectAttribute
from .options_list import OptionsList
from .page import Page
from .permission import Permission
from .place import Place
from .public_register import PublicRegister
from .publication import Publication
from .reference import (
    AttributeReference,
    CountryReference,
    LanguageReference,
    LocaleReference,
)
from .relationship import Relationship
from .rights_policy import RightsPolicy
from .scope import Scope, ScopeType
from .tenant import Domain, Tenant
from .ticket import Ticket
from .token import Token
from .transcription import Transcription
from .user import User
from .wordform import Wordform

__all__ = [
    'Agent',
    'AttributeReference',
    'Concept',
    'ContentAttributes',
    'ContentTypeExtended',
    'CountryReference',
    'Domain',
    'EntityPhrase',
    'GroupProperties',
    'Headword',
    'LanguageReference',
    'LocaleReference',
    'Location',
    'Object',
    'ObjectAttribute',
    'OptionsList',
    'Organization',
    'Page',
    'Permission',
    'Person',
    'Place',
    'PublicRegister',
    'Publication',
    'Relationship',
    'RightsPolicy',
    'Scope',
    'ScopeType',
    'Tenant',
    'Ticket',
    'Token',
    'Transcription',
    'User',
    'Wordform',
]

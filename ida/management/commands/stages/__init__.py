"""Interface for the migrate_data management command."""

from .attribute_options import Stage as AttributeOptionsStage
from .attribute_types import Stage as AttributeTypesStage
from .attributes import Stage as AttributesStage
from .auth import Stage as AuthStage
from .bootstrap_pharmacopeias import Stage as PharmaStage
from .collections import Stage as CollectionsStage
from .content_fixes import Stage as ContentFixes
from .finalize import Stage as FinalizeStage
from .named_agents import Stage as NamedAgentsStage
from .public import Stage as PublicStage
from .rank_0 import Stage as RankZeroStage
from .rank_1 import Stage as RankOneStage
from .rank_2 import Stage as RankTwoStage
from .records import Stage as RecordsStage

__all__ = [
    'AttributeOptionsStage',
    'AttributeTypesStage',
    'AttributesStage',
    'AuthStage',
    'CollectionsStage',
    'FinalizeStage',
    'ContentFixes',
    'PublicStage',
    'RankOneStage',
    'RankTwoStage',
    'RankZeroStage',
    'RecordsStage',
    'PharmaStage',
    'NamedAgentsStage',
]

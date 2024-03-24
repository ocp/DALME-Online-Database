"""Interface for the migrate_data management command."""

from .attribute_types import Stage as AttributeTypesStage
from .attributes import Stage as AttributesStage
from .auth import Stage as AuthStage
from .collections import Stage as CollectionsStage
from .finalize import Stage as FinalizeStage
from .post_fixes import Stage as PostFixes
from .public import Stage as PublicStage
from .rank_0 import Stage as RankZeroStage
from .rank_1 import Stage as RankOneStage
from .rank_2 import Stage as RankTwoStage
from .records import Stage as RecordsStage

__all__ = [
    'AttributeTypesStage',
    'AttributesStage',
    'AuthStage',
    'CollectionsStage',
    'FinalizeStage',
    'PostFixes',
    'PublicStage',
    'RankOneStage',
    'RankTwoStage',
    'RankZeroStage',
    'RecordsStage',
]

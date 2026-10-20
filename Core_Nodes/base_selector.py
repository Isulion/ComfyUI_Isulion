"""Shared seeded-selection core for the simple 'pick from a pool' nodes.

Subclasses declare their option pool as a class attribute (POOL or POOLS)
and call _make_rng() instead of touching the process-global random module,
so every node's output is reproducible from its own inputs alone.
"""

import random
from typing import ClassVar, Dict, List, Optional, Sequence, Tuple


class SimpleSelectorNode:
    """Base for single-choice selector nodes (no ComfyUI imports here)."""

    POOL: ClassVar[Optional[Sequence[str]]] = None
    POOLS: ClassVar[Optional[Dict[str, Sequence[str]]]] = None
    MAX_SEED: int = 0xFFFFFFFFFFFFFFFF

    @classmethod
    def _pool_for(cls, category: str = "any") -> List[str]:
        """Resolve the candidate list, optionally filtered by POOLS key."""
        if cls.POOLS is not None:
            if category and category != "any":
                return list(cls.POOLS.get(category, []))
            return [item for sub in cls.POOLS.values() for item in sub]
        return list(cls.POOL or [])

    def _make_rng(self, randomize: str, seed: int) -> Tuple[random.Random, int]:
        """Instance-local RNG honoring the legacy seed contract.

        enable + seed>0 -> deterministic stream seeded by `seed`.
        enable + seed==0 -> fresh entropy, reported via returned seed.
        disable -> rng is unused; caller keeps the dropdown value.
        """
        if randomize == "enable":
            if seed is not None and seed > 0:
                return random.Random(seed), seed
            new_seed = random.Random().randint(0, self.MAX_SEED)
            return random.Random(new_seed), new_seed
        return random.Random(seed), seed

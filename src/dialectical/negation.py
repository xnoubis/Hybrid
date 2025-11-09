"""
Negation Zone Mapping
Identify and analyze zones of productive impossibility
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .engine import Perspective, NegationZone


@dataclass
class TensionPoint:
    """A point of tension between perspectives"""
    dimension: str
    perspective_A_position: str
    perspective_B_position: str
    tension_strength: float
    productive: bool


class NegationMapper:
    """Map negation zones between perspectives"""

    def __init__(self):
        self.tension_dimensions = [
            'epistemology',  # How we know
            'ontology',      # What exists
            'values',        # What matters
            'methods',       # How we act
            'goals',         # What we seek
        ]

    def map_zone(
        self,
        perspective_A: Perspective,
        perspective_B: Perspective
    ) -> NegationZone:
        """
        Map the negation zone between two perspectives

        Args:
            perspective_A: First perspective
            perspective_B: Second perspective

        Returns:
            NegationZone object
        """
        # Find tension points
        tensions = self._identify_tensions(perspective_A, perspective_B)

        # Analyze what's true in both
        both_true = self._find_mutual_truths(
            perspective_A,
            perspective_B,
            tensions
        )

        # Why neither is sufficient
        neither_sufficient = self._find_insufficiencies(
            perspective_A,
            perspective_B,
            tensions
        )

        # Core impossibility
        impossibility_core = self._extract_impossibility_core(
            perspective_A,
            perspective_B,
            tensions
        )

        # Creative tension
        creative_tension = self._identify_creative_tension(tensions)

        return NegationZone(
            contradiction=f"{perspective_A.claim} vs {perspective_B.claim}",
            both_true=both_true,
            neither_sufficient=neither_sufficient,
            impossibility_core=impossibility_core,
            creative_tension=creative_tension
        )

    def analyze_tensions(
        self,
        perspective_A: Perspective,
        perspective_B: Perspective
    ) -> List[TensionPoint]:
        """
        Detailed analysis of tension points

        Returns:
            List of TensionPoint objects
        """
        return self._identify_tensions(perspective_A, perspective_B)

    def _identify_tensions(
        self,
        perspective_A: Perspective,
        perspective_B: Perspective
    ) -> List[TensionPoint]:
        """Identify all tension points"""
        tensions = []

        # Goal tension
        if perspective_A.victory_condition != perspective_B.victory_condition:
            tensions.append(TensionPoint(
                dimension='goals',
                perspective_A_position=perspective_A.victory_condition,
                perspective_B_position=perspective_B.victory_condition,
                tension_strength=self._calculate_tension_strength(
                    perspective_A.victory_condition,
                    perspective_B.victory_condition
                ),
                productive=True
            ))

        # Claim tension
        tensions.append(TensionPoint(
            dimension='claims',
            perspective_A_position=perspective_A.claim,
            perspective_B_position=perspective_B.claim,
            tension_strength=self._calculate_tension_strength(
                perspective_A.claim,
                perspective_B.claim
            ),
            productive=True
        ))

        # Assumption tensions
        for assumption_A in perspective_A.assumptions:
            for assumption_B in perspective_B.assumptions:
                if self._are_contradictory(assumption_A, assumption_B):
                    tensions.append(TensionPoint(
                        dimension='assumptions',
                        perspective_A_position=assumption_A,
                        perspective_B_position=assumption_B,
                        tension_strength=0.8,
                        productive=True
                    ))

        return tensions

    def _find_mutual_truths(
        self,
        perspective_A: Perspective,
        perspective_B: Perspective,
        tensions: List[TensionPoint]
    ) -> List[str]:
        """Find what's true in both perspectives"""
        truths = []

        # Both care about solving the problem
        truths.append(f"{perspective_A.name} seeks {perspective_A.victory_condition}")
        truths.append(f"{perspective_B.name} seeks {perspective_B.victory_condition}")

        # Both have valid claims
        truths.append(f"{perspective_A.claim} has merit")
        truths.append(f"{perspective_B.claim} has merit")

        # Both have non-negotiables
        if perspective_A.non_negotiables:
            truths.append(
                f"{perspective_A.name} cannot compromise on: "
                f"{', '.join(perspective_A.non_negotiables)}"
            )

        if perspective_B.non_negotiables:
            truths.append(
                f"{perspective_B.name} cannot compromise on: "
                f"{', '.join(perspective_B.non_negotiables)}"
            )

        return truths

    def _find_insufficiencies(
        self,
        perspective_A: Perspective,
        perspective_B: Perspective,
        tensions: List[TensionPoint]
    ) -> List[str]:
        """Find why neither perspective is sufficient alone"""
        insufficiencies = []

        # A alone ignores B's victory condition
        insufficiencies.append(
            f"{perspective_A.name} alone fails to achieve {perspective_B.victory_condition}"
        )

        # B alone ignores A's victory condition
        insufficiencies.append(
            f"{perspective_B.name} alone fails to achieve {perspective_A.victory_condition}"
        )

        # A alone violates B's non-negotiables
        if perspective_B.non_negotiables:
            insufficiencies.append(
                f"{perspective_A.name} alone violates: "
                f"{', '.join(perspective_B.non_negotiables)}"
            )

        # B alone violates A's non-negotiables
        if perspective_A.non_negotiables:
            insufficiencies.append(
                f"{perspective_B.name} alone violates: "
                f"{', '.join(perspective_A.non_negotiables)}"
            )

        return insufficiencies

    def _extract_impossibility_core(
        self,
        perspective_A: Perspective,
        perspective_B: Perspective,
        tensions: List[TensionPoint]
    ) -> str:
        """Extract the core impossibility"""
        # Find strongest tension
        if tensions:
            strongest = max(tensions, key=lambda t: t.tension_strength)
            return (
                f"Seems impossible to achieve both "
                f"{perspective_A.victory_condition} and "
                f"{perspective_B.victory_condition} because "
                f"{strongest.perspective_A_position} contradicts "
                f"{strongest.perspective_B_position}"
            )

        return (
            f"Seems impossible to satisfy both "
            f"{perspective_A.name} and {perspective_B.name}"
        )

    def _identify_creative_tension(
        self,
        tensions: List[TensionPoint]
    ) -> str:
        """Identify the creative/productive aspect of tension"""
        productive_tensions = [t for t in tensions if t.productive]

        if not productive_tensions:
            return "The tension between perspectives"

        # Focus on strongest productive tension
        strongest = max(productive_tensions, key=lambda t: t.tension_strength)

        return (
            f"The tension in {strongest.dimension} between "
            f"'{strongest.perspective_A_position}' and "
            f"'{strongest.perspective_B_position}' "
            f"creates a generative space for new solutions"
        )

    def _calculate_tension_strength(self, pos_A: str, pos_B: str) -> float:
        """
        Calculate tension strength between positions

        Simple heuristic based on text similarity (lower = stronger tension)
        """
        # Convert to sets of words
        words_A = set(pos_A.lower().split())
        words_B = set(pos_B.lower().split())

        # Calculate Jaccard distance (1 - similarity)
        intersection = words_A & words_B
        union = words_A | words_B

        if not union:
            return 0.5

        similarity = len(intersection) / len(union)
        tension = 1 - similarity

        return max(0.0, min(1.0, tension))

    def _are_contradictory(self, claim_A: str, claim_B: str) -> bool:
        """Check if two claims are contradictory"""
        # Simple heuristic: look for negation words
        negation_words = {'not', 'never', 'no', 'cannot', 'impossible'}

        words_A = set(claim_A.lower().split())
        words_B = set(claim_B.lower().split())

        # If one has negation and they share content words
        has_negation_A = bool(words_A & negation_words)
        has_negation_B = bool(words_B & negation_words)

        content_overlap = (words_A - negation_words) & (words_B - negation_words)

        # Contradictory if different negation status but shared content
        return (has_negation_A != has_negation_B) and len(content_overlap) > 2


def main():
    """CLI for negation zone mapping"""
    import argparse
    from .engine import Perspective

    parser = argparse.ArgumentParser(description='Map Negation Zones')
    parser.add_argument('--perspective-a', required=True, help='First perspective')
    parser.add_argument('--perspective-b', required=True, help='Second perspective')

    args = parser.parse_args()

    # Create perspectives from simple input
    perspective_A = Perspective(
        name='A',
        claim=args.perspective_a,
        victory_condition=f"Achieve {args.perspective_a}",
        assumptions=[],
        non_negotiables=[args.perspective_a]
    )

    perspective_B = Perspective(
        name='B',
        claim=args.perspective_b,
        victory_condition=f"Achieve {args.perspective_b}",
        assumptions=[],
        non_negotiables=[args.perspective_b]
    )

    # Map negation zone
    mapper = NegationMapper()
    zone = mapper.map_zone(perspective_A, perspective_B)

    print("Negation Zone Analysis")
    print("=" * 60)
    print(f"\nContradiction: {zone.contradiction}")
    print(f"\nImpossibility Core:\n  {zone.impossibility_core}")
    print(f"\nCreative Tension:\n  {zone.creative_tension}")

    print("\nBoth True:")
    for truth in zone.both_true:
        print(f"  - {truth}")

    print("\nNeither Sufficient:")
    for insufficiency in zone.neither_sufficient:
        print(f"  - {insufficiency}")

    # Analyze tensions
    tensions = mapper.analyze_tensions(perspective_A, perspective_B)
    print(f"\nTension Points: {len(tensions)}")
    for tension in tensions:
        print(f"  - {tension.dimension}: strength={tension.tension_strength:.2f}")


if __name__ == '__main__':
    main()

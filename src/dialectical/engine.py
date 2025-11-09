"""
Dialectical Solution Engine
Find solutions through impossibility crystallization
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from enum import Enum
import json


class SolutionType(Enum):
    """Types of dialectical solutions"""
    SYNTHESIS = "synthesis"  # Transcends both poles
    SUBLATION = "sublation"  # Preserves and elevates
    REFRAME = "reframe"  # Changes the frame
    EMBRACE = "embrace"  # Lives in the contradiction
    EMERGENCE = "emergence"  # New possibility emerges


@dataclass
class Problem:
    """Problem crystallization"""
    surface_tension: str
    impossibility: str
    why_impossible: List[str]
    metadata: Dict[str, Any]


@dataclass
class Perspective:
    """A perspective on the problem"""
    name: str
    claim: str
    victory_condition: str
    assumptions: List[str]
    non_negotiables: List[str]


@dataclass
class NegationZone:
    """The zone of impossibility between perspectives"""
    contradiction: str
    both_true: List[str]
    neither_sufficient: List[str]
    impossibility_core: str
    creative_tension: str


@dataclass
class Solution:
    """Dialectical solution"""
    solution_type: SolutionType
    description: str
    how_it_works: str
    preserves_A: List[str]
    preserves_B: List[str]
    transcends: str
    implementation_sketch: str
    new_questions: List[str]
    validation_criteria: List[str]


class SolutionEngine:
    """
    5-Phase Dialectical Solution Protocol

    1. Crystallize Problem
    2. Map Perspectives
    3. Identify Negation
    4. Crystallize Solution
    5. Validate Solution
    """

    def __init__(self):
        self.phase = 0
        self.problem: Optional[Problem] = None
        self.perspectives: Dict[str, Perspective] = {}
        self.negation: Optional[NegationZone] = None
        self.solution: Optional[Solution] = None

    def crystallize_problem(
        self,
        surface: str,
        impossibility: str,
        reasons: Optional[List[str]] = None
    ) -> Problem:
        """
        Phase 1: Crystallize the problem

        Args:
            surface: Surface-level tension
            impossibility: Core impossibility
            reasons: Why it seems impossible

        Returns:
            Problem object
        """
        if reasons is None:
            reasons = []

        self.problem = Problem(
            surface_tension=surface,
            impossibility=impossibility,
            why_impossible=reasons,
            metadata={}
        )

        self.phase = 1
        return self.problem

    def map_perspectives(
        self,
        perspectives: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Perspective]:
        """
        Phase 2: Map extreme perspectives

        Args:
            perspectives: Dict of perspective definitions
                Each should have: claim, victory, assumptions, non_negotiables

        Returns:
            Dict of Perspective objects
        """
        if not self.problem:
            raise ValueError("Must crystallize problem first")

        for name, data in perspectives.items():
            self.perspectives[name] = Perspective(
                name=name,
                claim=data.get('claim', ''),
                victory_condition=data.get('victory', ''),
                assumptions=data.get('assumptions', []),
                non_negotiables=data.get('non_negotiables', [])
            )

        self.phase = 2
        return self.perspectives

    def identify_negation(
        self,
        perspectives: Optional[Dict[str, Perspective]] = None
    ) -> NegationZone:
        """
        Phase 3: Identify the negation zone

        The negation zone is where both perspectives are true
        but neither is sufficient - the impossibility lives here

        Returns:
            NegationZone object
        """
        if perspectives is None:
            perspectives = self.perspectives

        if not perspectives or len(perspectives) < 2:
            raise ValueError("Need at least 2 perspectives")

        # Extract perspective pairs (usually A and B)
        persp_list = list(perspectives.values())
        A, B = persp_list[0], persp_list[1]

        # Find what's true in both
        both_true = [
            f"{A.name} is right that we need {A.claim}",
            f"{B.name} is right that we need {B.claim}"
        ]

        # Find why neither is sufficient alone
        neither_sufficient = [
            f"{A.name} alone ignores {B.victory_condition}",
            f"{B.name} alone ignores {A.victory_condition}"
        ]

        # The core impossibility
        impossibility_core = (
            f"We need both {A.claim} AND {B.claim}, "
            f"but they seem mutually exclusive"
        )

        # The creative tension
        creative_tension = (
            f"The tension between {A.name} and {B.name} "
            f"points to something beyond both"
        )

        self.negation = NegationZone(
            contradiction=f"{A.claim} vs {B.claim}",
            both_true=both_true,
            neither_sufficient=neither_sufficient,
            impossibility_core=impossibility_core,
            creative_tension=creative_tension
        )

        self.phase = 3
        return self.negation

    def crystallize_solution(
        self,
        negation: Optional[NegationZone] = None,
        solution_type: Optional[SolutionType] = None
    ) -> Solution:
        """
        Phase 4: Crystallize solution from negation zone

        Args:
            negation: NegationZone to work with
            solution_type: Type of solution to seek

        Returns:
            Solution object
        """
        if negation is None:
            negation = self.negation

        if not negation:
            raise ValueError("Must identify negation first")

        # Auto-detect solution type if not specified
        if solution_type is None:
            solution_type = self._detect_solution_type(negation)

        # Generate solution based on type
        if solution_type == SolutionType.SYNTHESIS:
            solution = self._generate_synthesis(negation)
        elif solution_type == SolutionType.SUBLATION:
            solution = self._generate_sublation(negation)
        elif solution_type == SolutionType.REFRAME:
            solution = self._generate_reframe(negation)
        elif solution_type == SolutionType.EMBRACE:
            solution = self._generate_embrace(negation)
        else:  # EMERGENCE
            solution = self._generate_emergence(negation)

        self.solution = solution
        self.phase = 4
        return solution

    def validate_solution(
        self,
        solution: Optional[Solution] = None,
        criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Phase 5: Validate solution

        Validation criteria:
        - Both extreme perspectives preserved (not compromised)
        - Impossibility embraced (not solved away)
        - Implementation plan concrete and testable
        - Generates new questions (not terminal answer)
        - Reproducible by independent application

        Returns:
            Dict with validation results
        """
        if solution is None:
            solution = self.solution

        if not solution:
            raise ValueError("Must crystallize solution first")

        if criteria is None:
            criteria = [
                'preserves_both_extremes',
                'embraces_impossibility',
                'implementable',
                'generative',
                'reproducible'
            ]

        results = {}

        for criterion in criteria:
            if criterion == 'preserves_both_extremes':
                passed = (
                    len(solution.preserves_A) > 0 and
                    len(solution.preserves_B) > 0
                )
                results[criterion] = {
                    'passed': passed,
                    'message': 'Both perspectives preserved' if passed
                               else 'Missing perspective preservation'
                }

            elif criterion == 'embraces_impossibility':
                passed = 'impossib' in solution.transcends.lower()
                results[criterion] = {
                    'passed': passed,
                    'message': 'Impossibility embraced' if passed
                               else 'Impossibility avoided'
                }

            elif criterion == 'implementable':
                passed = len(solution.implementation_sketch) > 50
                results[criterion] = {
                    'passed': passed,
                    'message': 'Implementation sketch provided' if passed
                               else 'Implementation unclear'
                }

            elif criterion == 'generative':
                passed = len(solution.new_questions) > 0
                results[criterion] = {
                    'passed': passed,
                    'message': 'Generates new questions' if passed
                               else 'Terminal solution (not dialectical)'
                }

            elif criterion == 'reproducible':
                passed = len(solution.validation_criteria) > 0
                results[criterion] = {
                    'passed': passed,
                    'message': 'Validation criteria provided' if passed
                               else 'No validation method'
                }

        # Overall validation
        results['overall'] = {
            'passed': all(r['passed'] for r in results.values() if r != 'overall'),
            'criteria_met': sum(1 for r in results.values()
                              if r != 'overall' and r['passed']),
            'total_criteria': len(criteria)
        }

        self.phase = 5
        return results

    def _detect_solution_type(self, negation: NegationZone) -> SolutionType:
        """Auto-detect most appropriate solution type"""
        # Simple heuristic for now
        # Could be enhanced with ML/pattern matching
        return SolutionType.SYNTHESIS

    def _generate_synthesis(self, negation: NegationZone) -> Solution:
        """Generate synthesis-type solution"""
        return Solution(
            solution_type=SolutionType.SYNTHESIS,
            description="Transcend both poles through higher-order integration",
            how_it_works=f"By recognizing that {negation.creative_tension}",
            preserves_A=["Core claim from perspective A"],
            preserves_B=["Core claim from perspective B"],
            transcends=negation.impossibility_core,
            implementation_sketch="1. Identify integration point\n2. Build bridge\n3. Test",
            new_questions=[
                "What other contradictions does this pattern apply to?",
                "What emerges at the integration point?"
            ],
            validation_criteria=[
                "Both perspectives feel heard",
                "New capability emerged",
                "Contradiction productive not dissolved"
            ]
        )

    def _generate_sublation(self, negation: NegationZone) -> Solution:
        """Generate sublation-type solution (Hegelian aufheben)"""
        return Solution(
            solution_type=SolutionType.SUBLATION,
            description="Preserve and elevate both poles",
            how_it_works=f"Lift both perspectives to meta-level: {negation.creative_tension}",
            preserves_A=["Essential truth from A"],
            preserves_B=["Essential truth from B"],
            transcends=negation.impossibility_core,
            implementation_sketch="1. Preserve both\n2. Elevate to meta\n3. Integrate",
            new_questions=["What meta-pattern contains both?"],
            validation_criteria=["Both preserved at higher level"]
        )

    def _generate_reframe(self, negation: NegationZone) -> Solution:
        """Generate reframe-type solution"""
        return Solution(
            solution_type=SolutionType.REFRAME,
            description="Change the frame that creates the contradiction",
            how_it_works=f"The contradiction exists in a frame: {negation.contradiction}",
            preserves_A=["What A really cares about"],
            preserves_B=["What B really cares about"],
            transcends="The frame itself",
            implementation_sketch="1. Identify frame\n2. Question assumptions\n3. Reframe",
            new_questions=["What frame creates this?", "What frame dissolves it?"],
            validation_criteria=["Frame shift observable", "Contradiction dissolves"]
        )

    def _generate_embrace(self, negation: NegationZone) -> Solution:
        """Generate embrace-type solution"""
        return Solution(
            solution_type=SolutionType.EMBRACE,
            description="Live productively in the contradiction",
            how_it_works=f"Make the tension productive: {negation.creative_tension}",
            preserves_A=["A's core value"],
            preserves_B=["B's core value"],
            transcends="The need to resolve it",
            implementation_sketch="1. Accept tension\n2. Make it generative\n3. Iterate",
            new_questions=["How is this tension useful?"],
            validation_criteria=["Tension remains", "Productivity increases"]
        )

    def _generate_emergence(self, negation: NegationZone) -> Solution:
        """Generate emergence-type solution"""
        return Solution(
            solution_type=SolutionType.EMERGENCE,
            description="Let new possibility emerge from the gap",
            how_it_works=f"The impossibility gap is creative: {negation.creative_tension}",
            preserves_A=["A's intent"],
            preserves_B=["B's intent"],
            transcends="Both current forms",
            implementation_sketch="1. Create space\n2. Notice emergence\n3. Nurture",
            new_questions=["What wants to emerge?"],
            validation_criteria=["Something new appeared", "Neither A nor B"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Export full engine state"""
        return {
            'phase': self.phase,
            'problem': asdict(self.problem) if self.problem else None,
            'perspectives': {
                name: asdict(p) for name, p in self.perspectives.items()
            },
            'negation': asdict(self.negation) if self.negation else None,
            'solution': asdict(self.solution) if self.solution else None
        }

    def to_json(self) -> str:
        """Export as JSON"""
        return json.dumps(self.to_dict(), indent=2)


def main():
    """CLI demo of dialectical engine"""
    print("Dialectical Solution Engine - Interactive Demo")
    print("=" * 60)

    # Example: AI Safety vs Capability
    engine = SolutionEngine()

    # Phase 1: Crystallize Problem
    print("\nPhase 1: Crystallize Problem")
    problem = engine.crystallize_problem(
        surface="AI safety vs capability",
        impossibility="Need powerful AI that's constrained",
        reasons=[
            "More capability means harder to control",
            "More safety means less useful",
            "Seems like zero-sum tradeoff"
        ]
    )
    print(f"Problem: {problem.impossibility}")

    # Phase 2: Map Perspectives
    print("\nPhase 2: Map Perspectives")
    perspectives = engine.map_perspectives({
        'Capability': {
            'claim': 'AI must reach full potential',
            'victory': 'AGI achieved',
            'assumptions': ['Progress is paramount'],
            'non_negotiables': ['Cannot cripple AI']
        },
        'Safety': {
            'claim': 'AI must be controllable',
            'victory': 'No catastrophic risk',
            'assumptions': ['Safety first'],
            'non_negotiables': ['Cannot risk extinction']
        }
    })
    print(f"Mapped {len(perspectives)} perspectives")

    # Phase 3: Identify Negation
    print("\nPhase 3: Identify Negation Zone")
    negation = engine.identify_negation()
    print(f"Impossibility: {negation.impossibility_core}")
    print(f"Creative tension: {negation.creative_tension}")

    # Phase 4: Crystallize Solution
    print("\nPhase 4: Crystallize Solution")
    solution = engine.crystallize_solution()
    print(f"Solution type: {solution.solution_type.value}")
    print(f"Description: {solution.description}")

    # Phase 5: Validate
    print("\nPhase 5: Validate Solution")
    validation = engine.validate_solution()
    print(f"Overall: {'PASSED' if validation['overall']['passed'] else 'FAILED'}")
    print(f"Criteria met: {validation['overall']['criteria_met']}/{validation['overall']['total_criteria']}")

    # Export
    print("\n" + "=" * 60)
    print("Full session exported to JSON")
    print(engine.to_json())


if __name__ == '__main__':
    main()

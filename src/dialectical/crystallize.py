"""
Solution Crystallization
Detect and refine solution types
"""

from typing import Dict, Any, List, Optional
from .engine import SolutionType, Solution, NegationZone


class SolutionCrystallizer:
    """Detect and crystallize solutions from negation zones"""

    def __init__(self):
        self.type_signatures = {
            SolutionType.SYNTHESIS: {
                'keywords': ['integrate', 'combine', 'unify', 'transcend'],
                'pattern': 'both-and',
                'marker': 'higher order'
            },
            SolutionType.SUBLATION: {
                'keywords': ['preserve', 'elevate', 'aufheben', 'meta'],
                'pattern': 'preserve-elevate',
                'marker': 'meta-level'
            },
            SolutionType.REFRAME: {
                'keywords': ['reframe', 'recontextualize', 'shift perspective'],
                'pattern': 'question-frame',
                'marker': 'different frame'
            },
            SolutionType.EMBRACE: {
                'keywords': ['live with', 'productive tension', 'dynamic'],
                'pattern': 'maintain-tension',
                'marker': 'generative conflict'
            },
            SolutionType.EMERGENCE: {
                'keywords': ['emerge', 'novel', 'create', 'new'],
                'pattern': 'gap-creation',
                'marker': 'something new'
            }
        }

    def detect_type(
        self,
        negation: NegationZone,
        context: Optional[str] = None
    ) -> SolutionType:
        """
        Detect most appropriate solution type

        Args:
            negation: The negation zone
            context: Additional context

        Returns:
            Detected SolutionType
        """
        # Analyze negation zone
        text = ' '.join([
            negation.contradiction,
            negation.impossibility_core,
            negation.creative_tension
        ])

        if context:
            text += ' ' + context

        text_lower = text.lower()

        # Score each type
        scores: Dict[SolutionType, float] = {}

        for solution_type, signature in self.type_signatures.items():
            score = 0.0

            # Check keywords
            for keyword in signature['keywords']:
                if keyword in text_lower:
                    score += 1.0

            # Check pattern markers
            if signature['pattern'] in text_lower:
                score += 2.0

            if signature['marker'] in text_lower:
                score += 1.5

            scores[solution_type] = score

        # Return highest scoring type
        if max(scores.values()) == 0:
            # Default to synthesis if no clear signal
            return SolutionType.SYNTHESIS

        return max(scores.items(), key=lambda x: x[1])[0]

    def refine_solution(
        self,
        solution: Solution,
        feedback: Dict[str, Any]
    ) -> Solution:
        """
        Refine solution based on feedback

        Args:
            solution: Initial solution
            feedback: Feedback dict with refinements

        Returns:
            Refined Solution
        """
        # Update fields based on feedback
        if 'description' in feedback:
            solution.description = feedback['description']

        if 'implementation_sketch' in feedback:
            solution.implementation_sketch = feedback['implementation_sketch']

        if 'new_questions' in feedback:
            solution.new_questions.extend(feedback['new_questions'])

        if 'validation_criteria' in feedback:
            solution.validation_criteria.extend(feedback['validation_criteria'])

        if 'preserves_A' in feedback:
            solution.preserves_A.extend(feedback['preserves_A'])

        if 'preserves_B' in feedback:
            solution.preserves_B.extend(feedback['preserves_B'])

        return solution

    def generate_alternatives(
        self,
        negation: NegationZone,
        primary_type: SolutionType
    ) -> List[Solution]:
        """
        Generate alternative solutions of different types

        Args:
            negation: The negation zone
            primary_type: Primary solution type to exclude

        Returns:
            List of alternative solutions
        """
        from .engine import SolutionEngine

        alternatives = []
        engine = SolutionEngine()

        # Generate solutions for each type except primary
        for solution_type in SolutionType:
            if solution_type != primary_type:
                try:
                    solution = engine._generate_solution_of_type(
                        negation,
                        solution_type
                    )
                    alternatives.append(solution)
                except Exception:
                    continue

        return alternatives


def main():
    """CLI for solution crystallization"""
    import argparse
    from .engine import SolutionEngine

    parser = argparse.ArgumentParser(description='Crystallize Solutions')
    parser.add_argument('--problem', required=True, help='Problem description')

    args = parser.parse_args()

    # Create simple problem
    engine = SolutionEngine()
    problem = engine.crystallize_problem(
        surface=args.problem,
        impossibility=f"How to solve: {args.problem}"
    )

    # Create basic perspectives
    perspectives = engine.map_perspectives({
        'A': {
            'claim': 'First approach',
            'victory': 'A succeeds',
            'assumptions': [],
            'non_negotiables': []
        },
        'B': {
            'claim': 'Second approach',
            'victory': 'B succeeds',
            'assumptions': [],
            'non_negotiables': []
        }
    })

    # Get negation
    negation = engine.identify_negation()

    # Detect solution type
    crystallizer = SolutionCrystallizer()
    detected_type = crystallizer.detect_type(negation, args.problem)

    print(f"Detected solution type: {detected_type.value}")

    # Generate alternatives
    alternatives = crystallizer.generate_alternatives(negation, detected_type)
    print(f"\nGenerated {len(alternatives)} alternative solutions")

    for alt in alternatives:
        print(f"  - {alt.solution_type.value}: {alt.description}")


if __name__ == '__main__':
    main()

"""
Tests for Dialectical Solution Engine
"""

import pytest
from src.dialectical.engine import (
    SolutionEngine, SolutionType, Problem, Perspective, NegationZone, Solution
)
from src.dialectical.crystallize import SolutionCrystallizer
from src.dialectical.negation import NegationMapper, TensionPoint


class TestSolutionEngine:
    """Test dialectical solution engine"""

    def test_five_phase_protocol(self):
        """Test complete 5-phase protocol"""
        engine = SolutionEngine()

        # Phase 1: Crystallize Problem
        problem = engine.crystallize_problem(
            surface="AI safety vs capability",
            impossibility="Need powerful AI that's constrained"
        )
        assert engine.phase == 1
        assert problem.impossibility == "Need powerful AI that's constrained"

        # Phase 2: Map Perspectives
        perspectives = engine.map_perspectives({
            'Safety': {
                'claim': 'Must be controllable',
                'victory': 'No catastrophe',
                'assumptions': ['Safety first'],
                'non_negotiables': ['No extinction risk']
            },
            'Capability': {
                'claim': 'Must reach potential',
                'victory': 'AGI achieved',
                'assumptions': ['Progress paramount'],
                'non_negotiables': ['No crippling']
            }
        })
        assert engine.phase == 2
        assert len(perspectives) == 2

        # Phase 3: Identify Negation
        negation = engine.identify_negation()
        assert engine.phase == 3
        assert negation is not None
        assert len(negation.both_true) > 0

        # Phase 4: Crystallize Solution
        solution = engine.crystallize_solution()
        assert engine.phase == 4
        assert solution is not None
        assert isinstance(solution.solution_type, SolutionType)

        # Phase 5: Validate
        validation = engine.validate_solution()
        assert engine.phase == 5
        assert 'overall' in validation

    def test_solution_types(self):
        """Test different solution types"""
        engine = SolutionEngine()

        # Set up simple problem
        engine.crystallize_problem("Test", "Test impossibility")
        engine.map_perspectives({
            'A': {'claim': 'A', 'victory': 'A wins', 'assumptions': [], 'non_negotiables': []},
            'B': {'claim': 'B', 'victory': 'B wins', 'assumptions': [], 'non_negotiables': []}
        })
        negation = engine.identify_negation()

        # Test each solution type
        for solution_type in SolutionType:
            solution = engine.crystallize_solution(solution_type=solution_type)
            assert solution.solution_type == solution_type

    def test_validation_criteria(self):
        """Test validation criteria"""
        engine = SolutionEngine()

        # Create complete solution
        engine.crystallize_problem("Test", "Test impossibility")
        engine.map_perspectives({
            'A': {'claim': 'A', 'victory': 'A wins', 'assumptions': [], 'non_negotiables': []},
            'B': {'claim': 'B', 'victory': 'B wins', 'assumptions': [], 'non_negotiables': []}
        })
        engine.identify_negation()
        solution = engine.crystallize_solution()

        # Validate
        validation = engine.validate_solution()

        assert 'preserves_both_extremes' in validation
        assert 'embraces_impossibility' in validation
        assert 'implementable' in validation
        assert 'generative' in validation
        assert 'reproducible' in validation

    def test_export_json(self):
        """Test JSON export"""
        engine = SolutionEngine()

        engine.crystallize_problem("Test", "Test impossibility")
        engine.map_perspectives({
            'A': {'claim': 'A', 'victory': 'A wins', 'assumptions': [], 'non_negotiables': []}
        })

        json_output = engine.to_json()
        assert isinstance(json_output, str)
        assert 'problem' in json_output
        assert 'perspectives' in json_output


class TestSolutionCrystallizer:
    """Test solution crystallizer"""

    def test_detect_solution_type(self):
        """Test solution type detection"""
        crystallizer = SolutionCrystallizer()

        # Create negation zone with synthesis markers
        negation = NegationZone(
            contradiction="A vs B",
            both_true=["A is true", "B is true"],
            neither_sufficient=["A alone fails", "B alone fails"],
            impossibility_core="Need both but they contradict",
            creative_tension="Can we integrate and transcend both?"
        )

        detected = crystallizer.detect_type(negation)
        assert isinstance(detected, SolutionType)


class TestNegationMapper:
    """Test negation zone mapping"""

    def test_map_negation_zone(self):
        """Test negation zone mapping"""
        mapper = NegationMapper()

        perspective_a = Perspective(
            name='A',
            claim='Maximize freedom',
            victory_condition='Individual autonomy',
            assumptions=['Freedom is paramount'],
            non_negotiables=['No coercion']
        )

        perspective_b = Perspective(
            name='B',
            claim='Ensure safety',
            victory_condition='Collective security',
            assumptions=['Safety first'],
            non_negotiables=['No harm']
        )

        zone = mapper.map_zone(perspective_a, perspective_b)

        assert isinstance(zone, NegationZone)
        assert len(zone.both_true) > 0
        assert len(zone.neither_sufficient) > 0
        assert zone.impossibility_core is not None

    def test_tension_analysis(self):
        """Test tension point analysis"""
        mapper = NegationMapper()

        perspective_a = Perspective(
            name='A',
            claim='Speed',
            victory_condition='Fast delivery',
            assumptions=[],
            non_negotiables=['Cannot be slow']
        )

        perspective_b = Perspective(
            name='B',
            claim='Quality',
            victory_condition='High quality',
            assumptions=[],
            non_negotiables=['Cannot be buggy']
        )

        tensions = mapper.analyze_tensions(perspective_a, perspective_b)

        assert len(tensions) > 0
        assert all(isinstance(t, TensionPoint) for t in tensions)

    def test_tension_strength_calculation(self):
        """Test tension strength calculation"""
        mapper = NegationMapper()

        # Very different positions = high tension
        strength_high = mapper._calculate_tension_strength(
            "maximize individual freedom",
            "ensure collective security"
        )

        # Similar positions = low tension
        strength_low = mapper._calculate_tension_strength(
            "maximize freedom",
            "maximize liberty"
        )

        assert strength_high > strength_low


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

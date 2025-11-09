"""
Tests for domain style generators
"""

import pytest
from src.generators.domain_style import DomainStyleGenerator, DomainProtocol


class TestDomainStyleGenerator:
    """Test domain-specific protocol generation"""

    def test_healthcare_protocol(self):
        """Test healthcare domain protocol"""
        generator = DomainStyleGenerator()
        protocol = generator.create_protocol("healthcare")

        assert protocol.domain == "healthcare"
        assert len(protocol.core_tensions) > 0
        assert len(protocol.crystallization_patterns) > 0
        assert len(protocol.solution_archetypes) > 0

    def test_ethics_protocol(self):
        """Test ethics domain protocol"""
        generator = DomainStyleGenerator()
        protocol = generator.create_protocol("ethics")

        assert protocol.domain == "ethics"
        assert len(protocol.core_tensions) > 0
        # Should include classic ethical tensions
        tension_str = ' '.join(protocol.core_tensions).lower()
        assert 'consequentialism' in tension_str or 'deontology' in tension_str

    def test_technology_protocol(self):
        """Test technology domain protocol"""
        generator = DomainStyleGenerator()
        protocol = generator.create_protocol("technology")

        assert protocol.domain == "technology"
        assert len(protocol.solution_archetypes) > 0

    def test_custom_protocol(self):
        """Test custom domain protocol"""
        generator = DomainStyleGenerator()
        protocol = generator.create_protocol(
            "quantum physics",
            core_tensions=[
                "wave vs particle",
                "determinism vs probability",
                "measurement vs state"
            ]
        )

        assert protocol.domain == "quantum physics"
        assert "wave vs particle" in protocol.core_tensions

    def test_markdown_export(self):
        """Test markdown export"""
        generator = DomainStyleGenerator()
        protocol = generator.create_protocol("healthcare")

        markdown = protocol.to_markdown()

        assert isinstance(markdown, str)
        assert "# Dialectical Protocol" in markdown
        assert "healthcare" in markdown
        assert "## Core Tensions" in markdown

    def test_skill_export(self):
        """Test skill export"""
        generator = DomainStyleGenerator()
        protocol = generator.create_protocol("ethics")

        skill = protocol.to_skill()

        assert isinstance(skill, str)
        assert "ethics" in skill.lower()
        assert "Protocol" in skill

    def test_all_templates(self):
        """Test all built-in templates"""
        generator = DomainStyleGenerator()

        domains = ['healthcare', 'ethics', 'technology', 'research', 'policy']

        for domain in domains:
            protocol = generator.create_protocol(domain)
            assert protocol.domain == domain
            assert len(protocol.core_tensions) >= 3
            assert len(protocol.solution_archetypes) >= 1


class TestDomainProtocol:
    """Test domain protocol class"""

    def test_protocol_creation(self):
        """Test basic protocol creation"""
        protocol = DomainProtocol(
            domain="test",
            core_tensions=["A vs B"],
            crystallization_patterns=["Either A or B"],
            common_negation_zones=["Need both A and B"],
            solution_archetypes=[{
                'name': 'Test',
                'description': 'Test solution',
                'when_to_use': 'Always'
            }],
            validation_criteria=["Works"],
            example_applications=["Example 1"]
        )

        assert protocol.domain == "test"
        assert len(protocol.core_tensions) == 1

    def test_markdown_format(self):
        """Test markdown formatting"""
        protocol = DomainProtocol(
            domain="test",
            core_tensions=["tension1"],
            crystallization_patterns=["pattern1"],
            common_negation_zones=["zone1"],
            solution_archetypes=[{
                'name': 'Archetype1',
                'description': 'Desc',
                'when_to_use': 'When'
            }],
            validation_criteria=["criterion1"],
            example_applications=["example1"]
        )

        md = protocol.to_markdown()

        assert "# Dialectical Protocol: test" in md
        assert "tension1" in md
        assert "Archetype1" in md

    def test_skill_format(self):
        """Test skill formatting"""
        protocol = DomainProtocol(
            domain="test domain",
            core_tensions=["tension1", "tension2"],
            crystallization_patterns=["pattern1"],
            common_negation_zones=["zone1"],
            solution_archetypes=[{
                'name': 'Arch',
                'description': 'D',
                'when_to_use': 'W'
            }],
            validation_criteria=["crit1"],
            example_applications=["ex1"]
        )

        skill = protocol.to_skill()

        assert "Test Domain" in skill
        assert "Protocol" in skill


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

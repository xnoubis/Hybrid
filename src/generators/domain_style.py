"""
Domain Style Generator
Create domain-specific dialectical protocols automatically
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
import json


@dataclass
class DomainProtocol:
    """Domain-specific dialectical protocol"""

    domain: str
    core_tensions: List[str]
    crystallization_patterns: List[str]
    common_negation_zones: List[str]
    solution_archetypes: List[Dict[str, str]]
    validation_criteria: List[str]
    example_applications: List[str]

    def to_markdown(self) -> str:
        """Export as markdown documentation"""
        md = f"""# Dialectical Protocol: {self.domain}

## Core Tensions

"""
        for tension in self.core_tensions:
            md += f"- {tension}\n"

        md += """
## Crystallization Patterns

These patterns help identify dialectical problems in this domain:

"""
        for pattern in self.crystallization_patterns:
            md += f"- {pattern}\n"

        md += """
## Common Negation Zones

Typical impossibility zones in this domain:

"""
        for zone in self.common_negation_zones:
            md += f"- {zone}\n"

        md += """
## Solution Archetypes

"""
        for archetype in self.solution_archetypes:
            md += f"### {archetype['name']}\n\n"
            md += f"{archetype['description']}\n\n"
            md += f"**When to use:** {archetype['when_to_use']}\n\n"

        md += """
## Validation Criteria

Solutions in this domain should meet these criteria:

"""
        for criterion in self.validation_criteria:
            md += f"- {criterion}\n"

        md += """
## Example Applications

"""
        for example in self.example_applications:
            md += f"- {example}\n"

        return md

    def to_skill(self) -> str:
        """Export as Claude skill definition"""
        skill = f"""# {self.domain.title()} - Dialectical Reasoning

A specialized dialectical reasoning skill for {self.domain}.

## Purpose

Apply dialectical solution methodology to problems in {self.domain}.

## Core Tensions in {self.domain}

"""
        for tension in self.core_tensions[:3]:  # Top 3 tensions
            skill += f"- {tension}\n"

        skill += f"""
## Protocol

When working with {self.domain} problems:

1. **Crystallize the Problem**
   - Identify which core tension is activated
   - Look for patterns: {', '.join(self.crystallization_patterns[:3])}

2. **Map Perspectives**
   - Find the extreme positions
   - Identify non-negotiables

3. **Find Negation Zone**
   - Common zones: {', '.join(self.common_negation_zones[:2])}
   - What's impossible but necessary?

4. **Crystallize Solution**
   - Apply relevant archetype
   - Preserve both extremes
   - Embrace the impossibility

5. **Validate**
   - Check criteria: {', '.join(self.validation_criteria[:3])}

## Example

"""
        if self.example_applications:
            skill += f"{self.example_applications[0]}\n"

        return skill

    def save(self, filepath: str):
        """Save protocol to file"""
        with open(filepath, 'w') as f:
            f.write(self.to_markdown())


class DomainStyleGenerator:
    """Generate domain-specific dialectical protocols"""

    def __init__(self):
        self.domain_templates = {
            'healthcare': self._healthcare_template,
            'ethics': self._ethics_template,
            'technology': self._technology_template,
            'research': self._research_template,
            'policy': self._policy_template,
        }

    def create_protocol(
        self,
        domain: str,
        core_tensions: Optional[List[str]] = None
    ) -> DomainProtocol:
        """
        Create domain-specific protocol

        Args:
            domain: Domain name (e.g., "healthcare ethics")
            core_tensions: Optional list of core tensions

        Returns:
            DomainProtocol object
        """
        # Check if we have a template
        domain_key = domain.lower().split()[0]  # First word

        if domain_key in self.domain_templates:
            # Use template
            protocol = self.domain_templates[domain_key](domain, core_tensions)
        else:
            # Generate from scratch
            protocol = self._generate_custom_protocol(domain, core_tensions)

        return protocol

    def _healthcare_template(
        self,
        domain: str,
        core_tensions: Optional[List[str]]
    ) -> DomainProtocol:
        """Healthcare domain template"""
        if core_tensions is None:
            core_tensions = [
                "Individual autonomy vs public health",
                "Cost containment vs quality care",
                "Innovation vs proven safety",
                "Specialist expertise vs holistic care",
                "Evidence-based vs patient-centered"
            ]

        return DomainProtocol(
            domain=domain,
            core_tensions=core_tensions,
            crystallization_patterns=[
                "Either aggressive treatment or palliative care",
                "Either cut costs or maintain quality",
                "Either standardize or personalize",
                "Either innovate or minimize risk"
            ],
            common_negation_zones=[
                "Need both individual choice and collective benefit",
                "Need both affordable and excellent care",
                "Need both innovation and safety",
                "Need both specialization and integration"
            ],
            solution_archetypes=[
                {
                    'name': 'Tiered Access',
                    'description': 'Multiple levels preserving both universal access and individual choice',
                    'when_to_use': 'When autonomy and equity are in tension'
                },
                {
                    'name': 'Outcome-Based Flexibility',
                    'description': 'Standardize outcomes, not methods',
                    'when_to_use': 'When evidence and personalization conflict'
                },
                {
                    'name': 'Staged Innovation',
                    'description': 'Safe pathways for novel approaches',
                    'when_to_use': 'When innovation and safety are in tension'
                }
            ],
            validation_criteria=[
                "Patient outcomes improved",
                "Healthcare workers satisfied",
                "Costs sustainable",
                "Equitable access maintained",
                "Innovation continues"
            ],
            example_applications=[
                "End-of-life care: autonomy vs family wishes vs resource allocation",
                "Vaccine mandates: individual freedom vs public health",
                "Experimental treatments: hope vs evidence vs cost"
            ]
        )

    def _ethics_template(
        self,
        domain: str,
        core_tensions: Optional[List[str]]
    ) -> DomainProtocol:
        """Ethics domain template"""
        if core_tensions is None:
            core_tensions = [
                "Consequentialism vs deontology",
                "Individual rights vs collective good",
                "Ought vs is",
                "Universal principles vs contextual judgment",
                "Intention vs outcome"
            ]

        return DomainProtocol(
            domain=domain,
            core_tensions=core_tensions,
            crystallization_patterns=[
                "Either maximize utility or respect rights",
                "Either follow rules or judge contexts",
                "Either absolute principles or relativism",
                "Either intention matters or only outcomes matter"
            ],
            common_negation_zones=[
                "Need both good outcomes and respect for rights",
                "Need both principles and context",
                "Need both is and ought",
                "Need both intention and outcome to matter"
            ],
            solution_archetypes=[
                {
                    'name': 'Threshold Deontology',
                    'description': 'Rights as constraints, consequences within bounds',
                    'when_to_use': 'When utility and rights conflict'
                },
                {
                    'name': 'Principled Particularism',
                    'description': 'Universal principles applied contextually',
                    'when_to_use': 'When rules and context are in tension'
                },
                {
                    'name': 'Virtue Framework',
                    'description': 'Character-based approach transcending outcome/duty divide',
                    'when_to_use': 'When consequentialist and deontological approaches clash'
                }
            ],
            validation_criteria=[
                "Preserves moral intuitions from both sides",
                "Provides action guidance",
                "Handles edge cases",
                "Maintains consistency",
                "Generates new moral insights"
            ],
            example_applications=[
                "Trolley problem: act vs omission",
                "Lying to save lives: truth vs welfare",
                "Just war: pacifism vs defense"
            ]
        )

    def _technology_template(
        self,
        domain: str,
        core_tensions: Optional[List[str]]
    ) -> DomainProtocol:
        """Technology domain template"""
        if core_tensions is None:
            core_tensions = [
                "Move fast vs be safe",
                "Open vs proprietary",
                "Privacy vs utility",
                "Accessibility vs security",
                "Innovation vs regulation"
            ]

        return DomainProtocol(
            domain=domain,
            core_tensions=core_tensions,
            crystallization_patterns=[
                "Either ship quickly or ensure quality",
                "Either open source or protect IP",
                "Either collect data or protect privacy",
                "Either secure or usable"
            ],
            common_negation_zones=[
                "Need both speed and safety",
                "Need both openness and sustainability",
                "Need both privacy and personalization",
                "Need both security and accessibility"
            ],
            solution_archetypes=[
                {
                    'name': 'Continuous Deployment with Rollback',
                    'description': 'Move fast with instant reversion capability',
                    'when_to_use': 'When speed and safety are in tension'
                },
                {
                    'name': 'Open Core',
                    'description': 'Open infrastructure, proprietary features',
                    'when_to_use': 'When open and commercial models conflict'
                },
                {
                    'name': 'Privacy-Preserving Computation',
                    'description': 'Process data without seeing it',
                    'when_to_use': 'When utility requires privacy-sensitive data'
                }
            ],
            validation_criteria=[
                "Technical feasibility proven",
                "User adoption metrics",
                "Security audit passed",
                "Privacy preserved",
                "Business model sustainable"
            ],
            example_applications=[
                "AI deployment: capability vs safety",
                "Social media: free speech vs harm prevention",
                "Encryption: security vs lawful access"
            ]
        )

    def _research_template(
        self,
        domain: str,
        core_tensions: Optional[List[str]]
    ) -> DomainProtocol:
        """Scientific research template"""
        if core_tensions is None:
            core_tensions = [
                "Rigor vs discovery",
                "Specialization vs synthesis",
                "Novelty vs replication",
                "Publish or perish vs quality",
                "Basic vs applied research"
            ]

        return DomainProtocol(
            domain=domain,
            core_tensions=core_tensions,
            crystallization_patterns=[
                "Either rigorous or exploratory",
                "Either deep specialist or broad generalist",
                "Either novel or replicated",
                "Either publish fast or ensure quality"
            ],
            common_negation_zones=[
                "Need both rigor and creativity",
                "Need both depth and breadth",
                "Need both novelty and reliability",
                "Need both basic understanding and application"
            ],
            solution_archetypes=[
                {
                    'name': 'Registered Reports',
                    'description': 'Pre-commit to rigorous method while exploring',
                    'when_to_use': 'When rigor and discovery are in tension'
                },
                {
                    'name': 'Interdisciplinary Teams',
                    'description': 'Specialists collaborating across boundaries',
                    'when_to_use': 'When depth and breadth conflict'
                },
                {
                    'name': 'Two-Stage Publishing',
                    'description': 'Fast preprint, peer-reviewed later',
                    'when_to_use': 'When speed and quality are in tension'
                }
            ],
            validation_criteria=[
                "Methodology sound",
                "Results reproducible",
                "Insights novel",
                "Practical implications identified",
                "Builds on existing work"
            ],
            example_applications=[
                "Exploratory data analysis: fishing vs hypothesis testing",
                "Interdisciplinary work: depth vs breadth",
                "COVID research: speed vs rigor"
            ]
        )

    def _policy_template(
        self,
        domain: str,
        core_tensions: Optional[List[str]]
    ) -> DomainProtocol:
        """Policy domain template"""
        if core_tensions is None:
            core_tensions = [
                "Individual freedom vs collective welfare",
                "Short-term vs long-term",
                "Equality vs efficiency",
                "Local autonomy vs national coordination",
                "Ideals vs pragmatism"
            ]

        return DomainProtocol(
            domain=domain,
            core_tensions=core_tensions,
            crystallization_patterns=[
                "Either free markets or regulation",
                "Either immediate relief or sustainable solutions",
                "Either equal outcomes or merit-based",
                "Either local control or coordinated action"
            ],
            common_negation_zones=[
                "Need both freedom and coordination",
                "Need both current relief and long-term sustainability",
                "Need both equality and incentives",
                "Need both local adaptation and national coherence"
            ],
            solution_archetypes=[
                {
                    'name': 'Subsidiarity Principle',
                    'description': 'Decisions at lowest effective level',
                    'when_to_use': 'When local and central control conflict'
                },
                {
                    'name': 'Market with Guardrails',
                    'description': 'Markets within ethical/safety bounds',
                    'when_to_use': 'When freedom and regulation are in tension'
                },
                {
                    'name': 'Progressive Universalism',
                    'description': 'Universal programs with progressive funding',
                    'when_to_use': 'When equality and efficiency conflict'
                }
            ],
            validation_criteria=[
                "Politically feasible",
                "Economically sustainable",
                "Ethically defensible",
                "Administratively practical",
                "Measurable outcomes"
            ],
            example_applications=[
                "Climate policy: growth vs environment",
                "Healthcare: access vs cost",
                "Immigration: security vs humanitarian concerns"
            ]
        )

    def _generate_custom_protocol(
        self,
        domain: str,
        core_tensions: Optional[List[str]]
    ) -> DomainProtocol:
        """Generate protocol for custom domain"""
        if core_tensions is None:
            core_tensions = [
                f"Core tension 1 in {domain}",
                f"Core tension 2 in {domain}",
                f"Core tension 3 in {domain}"
            ]

        return DomainProtocol(
            domain=domain,
            core_tensions=core_tensions,
            crystallization_patterns=[
                f"Either-or pattern related to {tension}"
                for tension in core_tensions
            ],
            common_negation_zones=[
                f"Need both sides of: {tension}"
                for tension in core_tensions
            ],
            solution_archetypes=[
                {
                    'name': 'Synthesis Approach',
                    'description': f'Integrate both poles of {core_tensions[0]}',
                    'when_to_use': 'When direct synthesis is possible'
                }
            ],
            validation_criteria=[
                "Domain experts satisfied",
                "Practical implementation exists",
                "Stakeholders heard",
                "Results measurable"
            ],
            example_applications=[
                f"Example application in {domain}"
            ]
        )


def main():
    """CLI for domain style generation"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate Domain-Specific Protocols')
    parser.add_argument('--domain', required=True, help='Domain name')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['markdown', 'skill', 'json'],
                       default='markdown', help='Output format')

    args = parser.parse_args()

    # Generate protocol
    generator = DomainStyleGenerator()
    protocol = generator.create_protocol(args.domain)

    # Format output
    if args.format == 'markdown':
        output = protocol.to_markdown()
    elif args.format == 'skill':
        output = protocol.to_skill()
    else:  # json
        output = json.dumps(asdict(protocol), indent=2)

    # Save or print
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Protocol saved to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()

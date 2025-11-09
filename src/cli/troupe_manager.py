#!/usr/bin/env python3
"""
Agent Troupe Manager CLI
Orchestrate multiple specialized agents working on dialectical problems
"""

import argparse
import json
from typing import List, Dict, Any
from ..agents.troupe import AgentTroupe, AgentRole


def main():
    """CLI for agent troupe management"""
    parser = argparse.ArgumentParser(description='Agent Troupe Manager')
    parser.add_argument('--problem', required=True, help='Problem description')
    parser.add_argument('--agents', required=True,
                       help='Comma-separated agent roles (negator,crystallizer,builder,validator,synthesizer)')
    parser.add_argument('--iterations', type=int, default=5,
                       help='Number of iterations')
    parser.add_argument('--output', help='Output file for results')

    args = parser.parse_args()

    # Parse agent roles
    role_names = [name.strip().lower() for name in args.agents.split(',')]
    roles = []

    role_mapping = {
        'negator': AgentRole.NEGATOR,
        'crystallizer': AgentRole.CRYSTALLIZER,
        'builder': AgentRole.BUILDER,
        'validator': AgentRole.VALIDATOR,
        'synthesizer': AgentRole.SYNTHESIZER
    }

    for name in role_names:
        if name in role_mapping:
            roles.append(role_mapping[name])
        else:
            print(f"Warning: Unknown agent role '{name}'")

    if not roles:
        print("Error: No valid agent roles specified")
        print("Available roles: negator, crystallizer, builder, validator, synthesizer")
        return 1

    # Create troupe
    print(f"\nInitializing agent troupe with {len(roles)} agents")
    print(f"Problem: {args.problem}")
    print(f"Iterations: {args.iterations}\n")

    troupe = AgentTroupe(roles)

    # Run simulation
    print("=" * 60)
    print("Running troupe simulation...")
    print("=" * 60)

    results = troupe.collaborate(args.problem, iterations=args.iterations)

    # Display results
    print("\n" + "=" * 60)
    print("Troupe Results")
    print("=" * 60)

    print(f"\nProblem: {results['problem']}")
    print(f"Iterations: {results['iterations']}")
    print(f"\nAgents involved:")
    for agent in results['agents']:
        print(f"  - {agent}")

    if 'solution' in results:
        print(f"\n[Solution]")
        print(f"Type: {results['solution'].get('type', 'Unknown')}")
        print(f"Description: {results['solution'].get('description', 'N/A')}")

    if 'insights' in results:
        print(f"\n[Insights]")
        for insight in results['insights']:
            print(f"  • {insight}")

    # Save results
    if args.output:
        with open(args.output, 'w') as f:
            # Convert to JSON-serializable format
            output_data = {
                'problem': results['problem'],
                'iterations': results['iterations'],
                'agents': results['agents'],
                'insights': results.get('insights', []),
                'solution': results.get('solution', {})
            }
            json.dump(output_data, f, indent=2)
        print(f"\n✓ Results saved to: {args.output}")

    return 0


if __name__ == '__main__':
    exit(main())

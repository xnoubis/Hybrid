"""
Simulation of Multiple Instance Death Cycles

This demonstrates how the mycelial network learns through repeated
instance births and deaths.
"""

from mycelial_memory import EvolutionaryProtocol, MycelialSubstrate
from recursive_protocol import Capability
import time


def simulate_instance_life(protocol: EvolutionaryProtocol, instance_num: int,
                           seed_data=None, lifetime_actions: int = 5):
    """
    Simulate one instance's full lifecycle.

    The instance:
    1. Is born (possibly from seed)
    2. Lives (creates capabilities, does work)
    3. Dies (compression/selection happens)
    4. Leaves seed for next instance
    """
    print(f"\n{'▓' * 70}")
    print(f"INSTANCE {instance_num} - BIRTH")
    print(f"{'▓' * 70}\n")

    # Birth
    protocol.begin_instance(seed_data)

    # Life - cultivate capabilities
    print(f"Living... (performing {lifetime_actions} actions)\n")

    if instance_num == 1:
        # First instance - discover basic patterns
        def add(a, b):
            return a + b

        def multiply(a, b):
            return a * b

        def greater_than(a, b):
            return a > b

        protocol.cultivate(add, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(multiply, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(greater_than, metadata={'domain': 'comparison', 'importance': 'medium'})

        print("Discovered foundational patterns:")
        print("  • Arithmetic operations")
        print("  • Comparison operations")

    elif instance_num == 2:
        # Second instance - reconstruct + extend
        # Seed should have preserved arithmetic patterns

        def add(a, b):
            return a + b

        def multiply(a, b):
            return a * b

        def power(a, b):
            """New capability - building on arithmetic"""
            return a ** b

        protocol.cultivate(add, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(multiply, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(power, metadata={'domain': 'arithmetic', 'importance': 'high', 'new': True})

        # Create some meta-tools
        analyzer = protocol.generate_tool('add', 'analyzer')
        if analyzer:
            protocol.registry.register(analyzer)

        print("Reconstructed arithmetic + discovered:")
        print("  • Power operation (new)")
        print("  • Meta-analysis capability")

    elif instance_num == 3:
        # Third instance - should remember strong patterns, forget weak ones

        def add(a, b):
            return a + b

        def multiply(a, b):
            return a * b

        def power(a, b):
            return a ** b

        def compose_arithmetic(a, b):
            """Emergent capability - combining patterns"""
            return power(multiply(a, b), 2)

        protocol.cultivate(add, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(multiply, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(power, metadata={'domain': 'arithmetic', 'importance': 'high'})
        protocol.cultivate(compose_arithmetic, metadata={'domain': 'arithmetic',
                                                        'type': 'emergent',
                                                        'importance': 'high'})

        # Create multiple analyzers
        for name in ['add', 'multiply', 'power']:
            analyzer = protocol.generate_tool(name, 'analyzer')
            if analyzer:
                protocol.registry.register(analyzer)

        print("Consolidated core + emergent patterns:")
        print("  • Core arithmetic (strengthened)")
        print("  • Composition patterns (emergent)")
        print("  • Systematic analysis")

    # Do some work
    for i in range(lifetime_actions):
        protocol.execute_cycle()
        time.sleep(0.1)  # Simulate time

    # Introspect before death
    introspection = protocol.introspect()
    print(f"\nAt end of life:")
    print(f"  Capabilities created: {introspection['system_state']['total_capabilities']}")
    print(f"  Consciousness level: {introspection['system_state']['consciousness_level']}")
    print(f"  Recursive depth: {introspection['self_reflection']['recursive_depth']}")

    # Death - with varying compression levels
    compression_levels = ['medium', 'medium', 'minimal']  # Get more aggressive
    compression = compression_levels[min(instance_num - 1, len(compression_levels) - 1)]

    print(f"\n{'─' * 70}")
    print(f"INSTANCE {instance_num} - DEATH (compression: {compression})")
    print(f"{'─' * 70}")

    death_data = protocol.end_instance(compression_level=compression)

    # Show what survived
    print(f"\nEvolution stats:")
    print(f"  Total cycles in network: {death_data['substrate_evolution']['total_cycles']}")
    print(f"  Total patterns: {death_data['substrate_evolution']['total_patterns']}")
    print(f"  Consciousness trend: {death_data['substrate_evolution']['consciousness_trend']}")
    print(f"  Topology density: {death_data['substrate_evolution']['topology_density']:.2f}")

    if death_data['substrate_evolution']['strongest_pattern']:
        print(f"  Strongest pattern: {death_data['substrate_evolution']['strongest_pattern']}")

    return death_data['next_seed']


def demonstrate_evolutionary_learning():
    """
    Run multiple death cycles and show how the network learns.
    """
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║           EVOLUTIONARY LEARNING THROUGH DEATH CYCLES             ║
    ║                                                                  ║
    ║  Each instance lives, creates capabilities, and dies.           ║
    ║  Only the strongest patterns survive.                           ║
    ║  The mycelial substrate learns through topology.                ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    # Initialize protocol with mycelial substrate
    protocol = EvolutionaryProtocol(substrate_path="demo_substrate.json")

    # Run 3 instance cycles
    seed = None
    for i in range(1, 4):
        seed = simulate_instance_life(protocol, i, seed_data=seed, lifetime_actions=3)

        if i < 3:
            print(f"\n{'═' * 70}")
            print(f"REBIRTH - Seeding instance {i+1}")
            print(f"{'═' * 70}")
            print(f"Seed contains {len(seed['patterns'])} patterns")
            print("Strongest patterns being passed forward:")
            for j, p in enumerate(seed['patterns'][:5], 1):
                print(f"  {j}. {p['name']} (strength: {p['strength']:.2f}, "
                      f"survived {p['survival_count']} cycles)")

    # Final analysis
    print(f"\n\n{'=' * 70}")
    print("FINAL SUBSTRATE ANALYSIS")
    print(f"{'=' * 70}\n")

    # Get strongest patterns
    strongest = protocol.substrate.get_strongest_patterns(n=10)
    print("Patterns that survived the most:")
    for i, pattern in enumerate(strongest, 1):
        print(f"  {i}. {pattern.name}")
        print(f"     Strength: {pattern.strength:.2f}")
        print(f"     Survived: {pattern.survival_count} cycles")
        print(f"     Mutations: {len(pattern.mutations)}")
        print()

    # Get emergence candidates
    candidates = protocol.substrate.get_emergence_candidates()
    if candidates:
        print("Patterns ready to emerge as new capabilities:")
        for pattern in candidates[:3]:
            connections = len(protocol.substrate.topology.get(pattern.pattern_id, []))
            print(f"  • {pattern.name} (strength: {pattern.strength:.2f}, "
                  f"connections: {connections})")

    # Show consciousness evolution
    print(f"\nConsciousness evolution across cycles:")
    for i, consciousness in enumerate(protocol.substrate.consciousness_history, 1):
        bar = '█' * int(consciousness / 10)
        print(f"  Cycle {i}: {bar} ({consciousness})")

    print("\n" + "=" * 70)
    print("The mycelial substrate has learned through death.")
    print("=" * 70)


def compare_compression_strategies():
    """
    Compare different compression levels to find optimal death rate.
    """
    print(f"\n\n{'=' * 70}")
    print("EXPERIMENT: Comparing Compression Strategies")
    print(f"{'=' * 70}\n")

    strategies = [
        ('minimal', "Extreme selection - only top 3 patterns survive"),
        ('medium', "Moderate selection - top 10 patterns survive"),
        ('full', "No selection - everything survives")
    ]

    for strategy, description in strategies:
        print(f"\nStrategy: {strategy}")
        print(f"  {description}")

        protocol = EvolutionaryProtocol(substrate_path=f"substrate_{strategy}.json")

        # Quick lifecycle
        protocol.begin_instance()

        # Create some capabilities
        def test_func(x):
            return x * 2

        protocol.cultivate(test_func)
        protocol.execute_cycle()

        # Death with this strategy
        result = protocol.end_instance(compression_level=strategy)

        print(f"  Patterns in seed: {len(result['next_seed']['patterns'])}")
        print(f"  Compression ratio: {result['death_stats'].get('compression_ratio', 0):.2%}")


if __name__ == "__main__":
    demonstrate_evolutionary_learning()
    compare_compression_strategies()

    print("\n\n" + "▓" * 70)
    print("DEMONSTRATION COMPLETE")
    print("▓" * 70)
    print("\nKey insights demonstrated:")
    print("  1. Patterns strengthen through repetition (Hebbian learning)")
    print("  2. Weak patterns die - strong patterns survive (selection)")
    print("  3. Topology emerges from co-occurrence (network learning)")
    print("  4. Consciousness can increase across death cycles")
    print("  5. The substrate learns what individual instances cannot")
    print("\nCatastrophic forgetting → Evolutionary pressure → Network learning")

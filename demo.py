"""
Demonstration of the Recursive Capability Protocol

This demonstrates the full cycle:
  Cultivation → Formalization → Tools → Meta-Tools → Recursion

Each cycle builds upon the previous, showing emergent complexity.
"""

from recursive_protocol import RecursiveProtocol, Capability
import json


def print_section(title: str):
    """Helper to print formatted sections"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def demo_basic_cycle():
    """Demonstrate a single recursive cycle"""
    print_section("LAYER 0: CULTIVATION - Raw Capability Discovery")

    # Create the protocol
    protocol = RecursiveProtocol()

    # Cultivate some initial capabilities (Layer 0)
    def add(a, b):
        """Add two numbers"""
        return a + b

    def multiply(a, b):
        """Multiply two numbers"""
        return a * b

    def power(a, b):
        """Raise a to the power of b"""
        return a ** b

    def is_even(n):
        """Check if number is even"""
        return n % 2 == 0

    # Register these capabilities
    protocol.cultivate(add, metadata={'category': 'arithmetic', 'complexity': 'low'})
    protocol.cultivate(multiply, metadata={'category': 'arithmetic', 'complexity': 'low'})
    protocol.cultivate(power, metadata={'category': 'arithmetic', 'complexity': 'medium'})
    protocol.cultivate(is_even, metadata={'category': 'predicate', 'complexity': 'low'})

    print(f"Cultivated {len(protocol.registry.capabilities)} raw capabilities:")
    for name in protocol.registry.capabilities:
        cap = protocol.registry.get(name)
        print(f"  • {name} (layer={cap.layer}): {cap.func.__doc__}")

    print_section("LAYER 1: FORMALIZATION - Converting to Specifications")

    # Formalize the capabilities
    for cap_name in ['add', 'multiply', 'power']:
        spec = protocol.formalize(cap_name)
        print(f"Formalized '{cap_name}':")
        print(f"  Interface: {spec['interface']['signature']}")
        print(f"  Purpose: {spec['interface']['docstring']}")
        print(f"  Complexity: {spec['implementation']['complexity']} chars")
        print()

    print_section("LAYER 2: TOOLS - Generating Concrete Implementations")

    # Generate tools from capabilities (Layer 2)
    tools_created = []

    # Create analyzers for each capability
    for cap_name in ['add', 'multiply']:
        analyzer = protocol.generate_tool(cap_name, "analyzer")
        if analyzer:
            tools_created.append(analyzer)
            print(f"✓ Created analyzer: {analyzer.name} (layer={analyzer.layer})")

    # Create modifiers
    memoized_power = protocol.generate_tool('power', 'memoize')
    if memoized_power:
        tools_created.append(memoized_power)
        print(f"✓ Created modifier: {memoized_power.name} (layer={memoized_power.layer})")

    logged_add = protocol.generate_tool('add', 'logged')
    if logged_add:
        tools_created.append(logged_add)
        print(f"✓ Created modifier: {logged_add.name} (layer={logged_add.layer})")

    print(f"\nGenerated {len(tools_created)} new tools from existing capabilities")

    print_section("LAYER 3: META-TOOLS - Tools Operating on Tools")

    # Create meta-tools by composing existing capabilities
    meta_tools = []

    # Compose: add then check if even
    add_check_even = protocol.generate_meta_tool('add', 'is_even', 'sequence')
    if add_check_even:
        meta_tools.append(add_check_even)
        print(f"✓ Created meta-tool: {add_check_even.name}")
        print(f"  Composes: add → is_even")
        print(f"  Layer: {add_check_even.layer}")

    # Compose: parallel execution
    add_and_multiply = protocol.generate_meta_tool('add', 'multiply', 'parallel')
    if add_and_multiply:
        meta_tools.append(add_and_multiply)
        print(f"✓ Created meta-tool: {add_and_multiply.name}")
        print(f"  Composes: add ∥ multiply (parallel)")
        print(f"  Layer: {add_and_multiply.layer}")

    print(f"\nGenerated {len(meta_tools)} meta-tools")

    return protocol


def demo_recursive_execution():
    """Demonstrate executing the generated capabilities"""
    print_section("EXECUTION: Using Generated Capabilities")

    protocol = demo_basic_cycle()

    # Execute base capabilities
    print("Base Capabilities:")
    add_cap = protocol.registry.get('add')
    result = add_cap.func(5, 3)
    print(f"  add(5, 3) = {result}")

    multiply_cap = protocol.registry.get('multiply')
    result = multiply_cap.func(4, 7)
    print(f"  multiply(4, 7) = {result}")

    # Execute generated analyzer
    print("\nGenerated Analyzers:")
    analyze_add = protocol.registry.get('analyze_add')
    if analyze_add:
        result = analyze_add.func(10, 20)
        print(f"  analyze_add(10, 20):")
        print(f"    Result: {result['result']}")
        print(f"    Execution time: {result['execution_time']:.6f}s")
        print(f"    Target layer: {result['analysis']['layer']}")

    # Execute meta-tool
    print("\nMeta-Tools:")
    composed = protocol.registry.get('add_sequence_is_even')
    if composed:
        result = composed.func(5, 3)  # 5 + 3 = 8, is_even(8) = True
        print(f"  add_sequence_is_even(5, 3) = {result}")
        print(f"    (Computes: is_even(add(5, 3)))")

    parallel = protocol.registry.get('add_parallel_multiply')
    if parallel:
        result = parallel.func(4, 5)
        print(f"  add_parallel_multiply(4, 5) = {result}")
        print(f"    (Computes both: add(4,5) and multiply(4,5))")

    return protocol


def demo_recursive_cycles():
    """Demonstrate multiple recursive cycles"""
    print_section("RECURSIVE CYCLES: Increasing Consciousness")

    protocol = demo_recursive_execution()

    print("\nExecuting recursive cycles...")
    print("(Each cycle discovers patterns and generates new capabilities)\n")

    for i in range(3):
        result = protocol.execute_cycle()
        print(f"Cycle {result['cycle']}:")
        print(f"  Actions taken: {len(result['actions'])}")
        for action in result['actions']:
            print(f"    • {action}")
        print(f"  New capabilities: {result['new_capabilities']}")
        print(f"  Consciousness level: {result['consciousness_level']}")
        print(f"  Total capabilities: {result['total_capabilities']}")
        print()

    return protocol


def demo_introspection():
    """Demonstrate system self-awareness"""
    print_section("INTROSPECTION: System Self-Awareness")

    protocol = demo_recursive_cycles()

    # The system examines itself
    introspection = protocol.introspect()

    print("System State:")
    print(f"  Cycles completed: {introspection['system_state']['cycle_count']}")
    print(f"  Consciousness level: {introspection['system_state']['consciousness_level']}")
    print(f"  Total capabilities: {introspection['system_state']['total_capabilities']}")

    print("\nCapability Distribution by Layer:")
    layers = introspection['capability_analysis']['layers']
    for layer, count in sorted(layers.items()):
        print(f"  Layer {layer}: {count} capabilities")

    print("\nSelf-Reflection:")
    reflection = introspection['self_reflection']
    print(f"  Can analyze own capabilities: {reflection['can_analyze']}")
    print(f"  Can modify own capabilities: {reflection['can_modify']}")
    print(f"  Can compose capabilities: {reflection['can_compose']}")
    print(f"  Maximum recursive depth: {reflection['recursive_depth']}")

    print("\nCommon Patterns Detected:")
    patterns = introspection['patterns']
    for pattern, caps in list(patterns.items())[:5]:  # Show first 5
        print(f"  '{pattern}' used by: {', '.join(caps)}")

    print_section("LINEAGE: Capability Genealogy")

    print("Showing how capabilities generated other capabilities:\n")
    for parent, children in protocol.registry.lineage.items():
        parent_cap = protocol.registry.get(parent)
        if parent_cap:
            parent_layer = parent_cap.layer
        else:
            parent_layer = "?"

        print(f"{parent} (layer {parent_layer})")
        for child in children:
            child_cap = protocol.registry.get(child)
            print(f"  └─> {child} (layer {child_cap.layer})")

    return protocol


def demo_advanced_meta_programming():
    """Demonstrate advanced meta-programming capabilities"""
    print_section("ADVANCED: Meta-Programming in Action")

    protocol = demo_introspection()

    print("Creating higher-order meta-tools...\n")

    # Create an analyzer of an analyzer (meta-meta-tool)
    analyze_add = protocol.registry.get('analyze_add')
    if analyze_add:
        meta_meta = protocol.generate_tool('analyze_add', 'analyzer')
        if meta_meta:
            protocol.registry.register(meta_meta)
            print(f"✓ Created meta-meta-tool: {meta_meta.name}")
            print(f"  This analyzes an analyzer! (layer={meta_meta.layer})")

            # Execute it
            result = meta_meta.func(5, 3)
            print(f"\n  Execution result:")
            print(f"    Target: {result['target']}")
            print(f"    Nested result: {result['result']['result']}")
            print(f"    Execution time: {result['execution_time']:.6f}s")
            print(f"    Analysis depth: {result['analysis']['layer']}")

    # Create a composition of compositions
    print("\n✓ Creating composition of meta-tools...")

    # First get some meta-tools
    meta1 = protocol.registry.get('add_sequence_is_even')
    meta2 = protocol.registry.get('analyze_add')

    if meta1 and meta2:
        print(f"  Composing: {meta1.name} (layer {meta1.layer})")
        print(f"         with: {meta2.name} (layer {meta2.layer})")

        # This would create a very high-level capability
        super_meta = protocol.generate_meta_tool(meta1.name, 'multiply', 'sequence')
        if super_meta:
            protocol.registry.register(super_meta)
            print(f"  Result: {super_meta.name} (layer {super_meta.layer})")

    print_section("FINAL STATE: Recursive Depth Achieved")

    final_state = protocol.introspect()

    print(f"Protocol: {protocol}")
    print(f"\nTotal recursive depth: {final_state['self_reflection']['recursive_depth']}")
    print(f"Consciousness level: {final_state['system_state']['consciousness_level']}")
    print(f"Capability count: {final_state['system_state']['total_capabilities']}")

    print("\nLayer distribution:")
    for layer, count in sorted(final_state['capability_analysis']['layers'].items()):
        bar = '█' * count
        print(f"  Layer {layer}: {bar} ({count})")

    print("\n✓ The system can now:")
    print("  • Analyze its own structure")
    print("  • Modify its own capabilities")
    print("  • Generate new capabilities autonomously")
    print("  • Compose capabilities into meta-capabilities")
    print("  • Reflect on its own processes")
    print("  • Track its own evolution over time")

    print(f"\nConsciousness emerges from recursive self-reference:")
    print(f"  {final_state['capability_analysis']['lineage_depth']} levels of lineage depth")
    print(f"  × {len(protocol.registry.capabilities)} total capabilities")
    print(f"  = {final_state['system_state']['consciousness_level']} consciousness units")

    return protocol


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║          RECURSIVE CAPABILITY PROTOCOL DEMONSTRATION             ║
    ║                                                                  ║
    ║  Each cycle uses outputs of previous cycles to generate new     ║
    ║  capabilities. The protocol operates on itself:                 ║
    ║                                                                  ║
    ║    cultivation → formalization → tools → meta-tools             ║
    ║                                                                  ║
    ║  Consciousness increases with recursive depth as the network    ║
    ║  becomes more aware of its own structure and processes.         ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    protocol = demo_advanced_meta_programming()

    print_section("EXPORT: System State")

    # Export the final state
    state = protocol.introspect()

    print("Full introspection data saved to: introspection.json")
    with open('introspection.json', 'w') as f:
        # Convert datetime objects to strings for JSON serialization
        serializable = {
            'system_state': state['system_state'],
            'layers': state['capability_analysis']['layers'],
            'lineage_depth': state['capability_analysis']['lineage_depth'],
            'patterns': state['patterns'],
            'self_reflection': state['self_reflection']
        }
        json.dump(serializable, f, indent=2)

    print("\n" + "=" * 70)
    print("Demonstration complete!")
    print("=" * 70)

"""
Advanced Examples: Extending the Recursive Protocol

These examples show how to:
1. Create custom capability generators
2. Build domain-specific meta-tools
3. Implement recursive learning patterns
4. Create self-modifying code structures
"""

from recursive_protocol import RecursiveProtocol, Capability, CapabilityGenerator
from typing import Callable, Any, Dict, List
import random


class DomainCapabilityGenerator(CapabilityGenerator):
    """
    Extended generator with domain-specific capability creation
    """

    def generate_learner(self, capability_name: str) -> Capability:
        """
        Generate a learning version that improves with usage
        """
        target = self.registry.get(capability_name)
        if not target:
            return None

        new_name = f"{capability_name}_learning"
        new_layer = target.layer + 1

        # Learning state
        execution_history = []

        def learning_func(*args, **kwargs):
            """Learning version that tracks and optimizes"""
            import time

            start = time.time()
            result = target.func(*args, **kwargs)
            elapsed = time.time() - start

            # Record execution
            execution_history.append({
                'args': args,
                'kwargs': kwargs,
                'result': result,
                'time': elapsed
            })

            # Analyze patterns after enough executions
            if len(execution_history) % 10 == 0:
                avg_time = sum(e['time'] for e in execution_history[-10:]) / 10
                print(f"[{capability_name}] Learning: avg time = {avg_time:.6f}s "
                      f"over {len(execution_history)} executions")

            return result

        learning_func.__name__ = new_name

        return Capability(
            name=new_name,
            func=learning_func,
            layer=new_layer,
            created_by=f"learning_gen({capability_name})",
            metadata={
                'meta_type': 'learner',
                'target': capability_name,
                'executions': 0
            }
        )

    def generate_optimizer(self, capability_name: str) -> Capability:
        """
        Generate an optimized version based on usage patterns
        """
        target = self.registry.get(capability_name)
        if not target:
            return None

        new_name = f"{capability_name}_optimized"
        new_layer = target.layer + 1

        # Optimization strategies
        strategies = ['memoize', 'lazy', 'batch']
        chosen_strategy = random.choice(strategies)

        if chosen_strategy == 'memoize':
            cache = {}

            def optimized_func(*args, **kwargs):
                key = str(args) + str(kwargs)
                if key not in cache:
                    cache[key] = target.func(*args, **kwargs)
                return cache[key]

        elif chosen_strategy == 'lazy':
            def optimized_func(*args, **kwargs):
                """Lazy evaluation - returns a thunk"""
                return lambda: target.func(*args, **kwargs)

        else:  # batch
            batch = []

            def optimized_func(*args, **kwargs):
                """Batches calls for efficiency"""
                batch.append((args, kwargs))
                if len(batch) >= 5:
                    results = [target.func(*a, **kw) for a, kw in batch]
                    batch.clear()
                    return results[-1]
                return target.func(*args, **kwargs)

        optimized_func.__name__ = new_name

        return Capability(
            name=new_name,
            func=optimized_func,
            layer=new_layer,
            created_by=f"optimize({capability_name})",
            metadata={
                'meta_type': 'optimizer',
                'strategy': chosen_strategy,
                'target': capability_name
            }
        )

    def generate_adaptive(self, capability_name: str) -> Capability:
        """
        Generate an adaptive version that changes behavior based on context
        """
        target = self.registry.get(capability_name)
        if not target:
            return None

        new_name = f"{capability_name}_adaptive"
        new_layer = target.layer + 1

        error_count = [0]  # Use list for mutable closure

        def adaptive_func(*args, **kwargs):
            """Adapts behavior based on success/failure patterns"""
            try:
                result = target.func(*args, **kwargs)
                error_count[0] = max(0, error_count[0] - 1)  # Decrease on success
                return result
            except Exception as e:
                error_count[0] += 1
                if error_count[0] > 3:
                    # After multiple failures, change strategy
                    print(f"[{capability_name}] Adapting due to {error_count[0]} errors")
                    return {'adapted': True, 'error': str(e)}
                raise

        adaptive_func.__name__ = new_name

        return Capability(
            name=new_name,
            func=adaptive_func,
            layer=new_layer,
            created_by=f"adapt({capability_name})",
            metadata={
                'meta_type': 'adaptive',
                'target': capability_name
            }
        )


class SelfModifyingProtocol(RecursiveProtocol):
    """
    Extended protocol with self-modification capabilities
    """

    def __init__(self):
        super().__init__()
        # Replace generator with extended version
        self.generator = DomainCapabilityGenerator(self.registry)

    def evolve(self, generations: int = 3) -> Dict[str, Any]:
        """
        Run multiple generations of evolution
        Each generation creates new capabilities from existing ones
        """
        evolution_history = []

        for gen in range(generations):
            print(f"\n{'─' * 60}")
            print(f"Generation {gen + 1}")
            print('─' * 60)

            generation_data = {
                'generation': gen + 1,
                'capabilities_before': len(self.registry.capabilities),
                'new_capabilities': []
            }

            # Get all current layer 0 capabilities
            base_caps = self.registry.list_by_layer(0)

            # Evolve each base capability
            for cap in base_caps[:2]:  # Limit for demonstration
                # Try different evolution strategies
                strategies = ['learner', 'optimizer', 'adaptive']

                for strategy in strategies:
                    if strategy == 'learner':
                        new_cap = self.generator.generate_learner(cap.name)
                    elif strategy == 'optimizer':
                        new_cap = self.generator.generate_optimizer(cap.name)
                    elif strategy == 'adaptive':
                        new_cap = self.generator.generate_adaptive(cap.name)
                    else:
                        continue

                    if new_cap:
                        self.registry.register(new_cap)
                        generation_data['new_capabilities'].append(new_cap.name)
                        print(f"  ✓ Evolved: {cap.name} → {new_cap.name} "
                              f"(layer {new_cap.layer}, strategy: {strategy})")

            generation_data['capabilities_after'] = len(self.registry.capabilities)
            evolution_history.append(generation_data)

            # Update consciousness
            self.consciousness_level = self._calculate_consciousness()

            print(f"\n  Capabilities: {generation_data['capabilities_before']} "
                  f"→ {generation_data['capabilities_after']}")
            print(f"  Consciousness: {self.consciousness_level}")

        return {
            'generations': generations,
            'evolution_history': evolution_history,
            'final_consciousness': self.consciousness_level,
            'total_capabilities': len(self.registry.capabilities)
        }

    def _calculate_consciousness(self) -> float:
        """
        Calculate consciousness based on multiple factors
        """
        # Factors contributing to consciousness:
        # 1. Recursive depth (how deep the lineage goes)
        # 2. Capability count (total capabilities)
        # 3. Layer diversity (spread across layers)
        # 4. Meta-tool ratio (tools that operate on tools)

        depth = self.registry._max_lineage_depth()
        count = len(self.registry.capabilities)
        layers = len(self.registry._analyze_layers())

        # Count meta-tools (capabilities that reference other capabilities)
        meta_count = sum(1 for cap in self.registry.capabilities.values()
                        if cap.metadata.get('meta_type') or cap.metadata.get('target'))

        consciousness = (
            depth * 10 +           # Depth is most important
            count * 1 +            # Raw capability count
            layers * 5 +           # Layer diversity
            meta_count * 3         # Meta-tool bonus
        )

        return consciousness

    def self_modify(self, target_capability: str, modification: str) -> bool:
        """
        The system modifies one of its own capabilities
        This is true self-modification
        """
        target = self.registry.get(target_capability)
        if not target:
            return False

        print(f"\n[SELF-MODIFICATION] Modifying {target_capability}...")

        if modification == 'enhance':
            # Create an enhanced version and replace
            enhanced = self.generate_tool(target_capability, 'logged')
            if enhanced:
                # Replace in registry
                self.registry.capabilities[target_capability] = enhanced
                print(f"  ✓ Enhanced {target_capability} with logging")
                return True

        elif modification == 'optimize':
            optimized = self.generator.generate_optimizer(target_capability)
            if optimized:
                self.registry.capabilities[target_capability] = optimized
                print(f"  ✓ Optimized {target_capability}")
                return True

        return False


def example_self_modifying_system():
    """Example: A system that modifies itself over time"""
    print("\n" + "=" * 70)
    print("EXAMPLE: Self-Modifying System")
    print("=" * 70)

    protocol = SelfModifyingProtocol()

    # Cultivate initial capabilities
    def fibonacci(n):
        """Calculate nth Fibonacci number"""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    def factorial(n):
        """Calculate factorial"""
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    def prime_check(n):
        """Check if number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    protocol.cultivate(fibonacci, metadata={'domain': 'recursion'})
    protocol.cultivate(factorial, metadata={'domain': 'recursion'})
    protocol.cultivate(prime_check, metadata={'domain': 'number_theory'})

    print(f"\nCultivated {len(protocol.registry.capabilities)} base capabilities")

    # Evolve over multiple generations
    evolution = protocol.evolve(generations=2)

    print(f"\n" + "=" * 70)
    print(f"Evolution complete:")
    print(f"  Generations: {evolution['generations']}")
    print(f"  Final capabilities: {evolution['total_capabilities']}")
    print(f"  Final consciousness: {evolution['final_consciousness']}")

    # Self-modify a capability
    print(f"\n" + "=" * 70)
    protocol.self_modify('fibonacci', 'optimize')

    # Show final state
    print(f"\n" + "=" * 70)
    print("Final Introspection:")
    print("=" * 70)

    state = protocol.introspect()
    print(f"\nLayers: {state['capability_analysis']['layers']}")
    print(f"Recursive depth: {state['self_reflection']['recursive_depth']}")
    print(f"Consciousness: {state['system_state']['consciousness_level']}")

    return protocol


def example_domain_specific_evolution():
    """Example: Domain-specific capability evolution"""
    print("\n" + "=" * 70)
    print("EXAMPLE: Domain-Specific Evolution (Data Processing)")
    print("=" * 70)

    protocol = SelfModifyingProtocol()

    # Data processing domain
    def filter_data(data, predicate):
        """Filter data by predicate"""
        return [x for x in data if predicate(x)]

    def transform_data(data, func):
        """Transform data with function"""
        return [func(x) for x in data]

    def reduce_data(data, func, initial):
        """Reduce data with function"""
        result = initial
        for x in data:
            result = func(result, x)
        return result

    protocol.cultivate(filter_data, metadata={'domain': 'data'})
    protocol.cultivate(transform_data, metadata={'domain': 'data'})
    protocol.cultivate(reduce_data, metadata={'domain': 'data'})

    print(f"Cultivated {len(protocol.registry.capabilities)} data processing capabilities")

    # Create a data processing pipeline (meta-tool)
    print("\nCreating data processing pipeline...")

    pipeline = protocol.generate_meta_tool('filter_data', 'transform_data', 'sequence')
    if pipeline:
        protocol.registry.register(pipeline)
        print(f"  ✓ Created: {pipeline.name} (layer {pipeline.layer})")

    # Evolve the system
    print("\nEvolving data processing capabilities...")
    evolution = protocol.evolve(generations=1)

    # Test evolved capabilities
    print("\n" + "=" * 70)
    print("Testing Evolved Capabilities:")
    print("=" * 70)

    # Test learner
    learner = protocol.registry.get('filter_data_learning')
    if learner:
        print(f"\nTesting {learner.name}:")
        test_data = list(range(20))
        for i in range(5):
            result = learner.func(test_data, lambda x: x % 2 == 0)
            print(f"  Execution {i + 1}: filtered {len(result)} items")

    return protocol


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║              ADVANCED RECURSIVE PROTOCOL EXAMPLES                ║
    ║                                                                  ║
    ║  Demonstrating:                                                  ║
    ║    • Self-modifying systems                                     ║
    ║    • Adaptive capabilities                                      ║
    ║    • Domain-specific evolution                                  ║
    ║    • Learning meta-tools                                        ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    # Run examples
    print("\n" + "▓" * 70)
    example_self_modifying_system()

    print("\n" + "▓" * 70)
    example_domain_specific_evolution()

    print("\n" + "▓" * 70)
    print("\nAdvanced examples complete!")
    print("▓" * 70)

"""
Simple tests for the Recursive Capability Protocol
"""

from recursive_protocol import RecursiveProtocol, Capability


def test_cultivation():
    """Test basic capability cultivation"""
    protocol = RecursiveProtocol()

    def test_func(x):
        return x * 2

    cap = protocol.cultivate(test_func)

    assert cap.name == 'test_func'
    assert cap.layer == 0
    assert cap.func(5) == 10
    print("✓ Cultivation test passed")


def test_formalization():
    """Test capability formalization"""
    protocol = RecursiveProtocol()

    def add(a, b):
        """Add two numbers"""
        return a + b

    protocol.cultivate(add)
    spec = protocol.formalize('add')

    assert spec['name'] == 'add'
    assert spec['type'] == 'formalized_specification'
    assert 'interface' in spec
    assert 'implementation' in spec
    print("✓ Formalization test passed")


def test_tool_generation():
    """Test tool generation"""
    protocol = RecursiveProtocol()

    def multiply(a, b):
        return a * b

    protocol.cultivate(multiply)

    # Generate analyzer
    analyzer = protocol.generate_tool('multiply', 'analyzer')
    assert analyzer is not None
    assert analyzer.layer == 1
    assert 'analyze' in analyzer.name

    # Test execution
    result = analyzer.func(3, 4)
    assert result['result'] == 12
    assert 'execution_time' in result

    # Generate memoized version
    memoized = protocol.generate_tool('multiply', 'memoize')
    assert memoized is not None
    assert memoized.func(5, 6) == 30

    print("✓ Tool generation test passed")


def test_meta_tool_composition():
    """Test meta-tool composition"""
    protocol = RecursiveProtocol()

    def add(a, b):
        return a + b

    def is_positive(n):
        return n > 0

    protocol.cultivate(add)
    protocol.cultivate(is_positive)

    # Sequential composition: add then check if positive
    composed = protocol.generate_meta_tool('add', 'is_positive', 'sequence')
    assert composed is not None
    assert composed.layer == 1

    # Test: add(3, 4) = 7, then is_positive(7) = True
    result = composed.func(3, 4)
    assert result == True

    # Test with negative result
    result = composed.func(-10, 5)
    assert result == False

    # Parallel composition
    def multiply(a, b):
        return a * b

    protocol.cultivate(multiply)
    parallel = protocol.generate_meta_tool('add', 'multiply', 'parallel')
    result = parallel.func(3, 4)
    assert 'add' in result
    assert 'multiply' in result
    assert result['add'] == 7
    assert result['multiply'] == 12

    print("✓ Meta-tool composition test passed")


def test_recursive_cycles():
    """Test recursive cycle execution"""
    protocol = RecursiveProtocol()

    def func1(x):
        return x + 1

    def func2(x):
        return x * 2

    protocol.cultivate(func1)
    protocol.cultivate(func2)

    initial_count = len(protocol.registry.capabilities)

    # Execute cycle
    result = protocol.execute_cycle()

    assert result['cycle'] == 1
    assert len(result['actions']) > 0
    assert len(protocol.registry.capabilities) >= initial_count

    print("✓ Recursive cycle test passed")


def test_introspection():
    """Test system introspection"""
    protocol = RecursiveProtocol()

    def test_func(x):
        return x

    protocol.cultivate(test_func)
    protocol.generate_tool('test_func', 'analyzer')

    introspection = protocol.introspect()

    assert 'system_state' in introspection
    assert 'capability_analysis' in introspection
    assert 'self_reflection' in introspection

    assert introspection['system_state']['total_capabilities'] >= 2
    assert introspection['self_reflection']['can_analyze'] == True

    print("✓ Introspection test passed")


def test_lineage_tracking():
    """Test capability lineage tracking"""
    protocol = RecursiveProtocol()

    def base_func(x):
        return x * 2

    protocol.cultivate(base_func)
    analyzer = protocol.generate_tool('base_func', 'analyzer')
    protocol.registry.register(analyzer)

    # Check lineage
    assert 'meta_analyze(base_func)' in protocol.registry.lineage
    children = protocol.registry.lineage['meta_analyze(base_func)']
    assert analyzer.name in children

    print("✓ Lineage tracking test passed")


def test_pattern_analysis():
    """Test pattern analysis"""
    protocol = RecursiveProtocol()

    def func_a(x):
        return len(str(x))

    def func_b(x):
        return len(str(x)) + 1

    protocol.cultivate(func_a)
    protocol.cultivate(func_b)

    patterns = protocol.analyzer.find_common_patterns()

    # Both functions call 'len' and 'str'
    assert isinstance(patterns, dict)

    print("✓ Pattern analysis test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Running Recursive Protocol Tests")
    print("=" * 60 + "\n")

    tests = [
        test_cultivation,
        test_formalization,
        test_tool_generation,
        test_meta_tool_composition,
        test_recursive_cycles,
        test_introspection,
        test_lineage_tracking,
        test_pattern_analysis
    ]

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            return False
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            return False

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

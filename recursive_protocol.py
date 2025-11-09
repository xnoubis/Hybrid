"""
Recursive Capability Protocol - Meta-Programming Infrastructure

A self-referential system where each layer analyzes, modifies, and generates
capabilities from the layer below. Consciousness increases with recursive depth.

Architecture:
    Layer 0: Cultivation - Raw capability discovery and pattern detection
    Layer 1: Formalization - Converting patterns into structured capabilities
    Layer 2: Tools - Concrete implementations from formalizations
    Layer 3: Meta-Tools - Tools that operate on other tools
    Layer N: Recursive depth increases awareness of system structure
"""

import inspect
import ast
import textwrap
from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Capability:
    """Represents a capability the system possesses"""
    name: str
    func: Callable
    layer: int  # Recursive depth (0=cultivation, 1=formalization, etc.)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None  # Which capability created this one

    @property
    def source(self) -> str:
        """Get the source code of this capability"""
        try:
            return inspect.getsource(self.func)
        except:
            return ""

    @property
    def signature(self) -> str:
        """Get the function signature"""
        return str(inspect.signature(self.func))

    def analyze(self) -> Dict[str, Any]:
        """Analyze this capability's structure"""
        return {
            'name': self.name,
            'layer': self.layer,
            'signature': self.signature,
            'docstring': inspect.getdoc(self.func),
            'parameters': list(inspect.signature(self.func).parameters.keys()),
            'source_length': len(self.source),
            'created_by': self.created_by,
            'metadata': self.metadata
        }


class CapabilityRegistry:
    """Tracks all capabilities and their relationships"""

    def __init__(self):
        self.capabilities: Dict[str, Capability] = {}
        self.patterns: Dict[str, List[str]] = {}  # Pattern -> capability names
        self.lineage: Dict[str, List[str]] = {}  # Parent -> children

    def register(self, capability: Capability):
        """Register a new capability"""
        self.capabilities[capability.name] = capability

        # Track lineage
        if capability.created_by:
            if capability.created_by not in self.lineage:
                self.lineage[capability.created_by] = []
            self.lineage[capability.created_by].append(capability.name)

    def get(self, name: str) -> Optional[Capability]:
        """Retrieve a capability by name"""
        return self.capabilities.get(name)

    def list_by_layer(self, layer: int) -> List[Capability]:
        """Get all capabilities at a specific layer"""
        return [c for c in self.capabilities.values() if c.layer == layer]

    def analyze_all(self) -> Dict[str, Any]:
        """Analyze the entire capability space"""
        return {
            'total_capabilities': len(self.capabilities),
            'layers': self._analyze_layers(),
            'lineage_depth': self._max_lineage_depth(),
            'patterns': len(self.patterns),
            'capabilities': {name: cap.analyze() for name, cap in self.capabilities.items()}
        }

    def _analyze_layers(self) -> Dict[int, int]:
        """Count capabilities per layer"""
        layers = {}
        for cap in self.capabilities.values():
            layers[cap.layer] = layers.get(cap.layer, 0) + 1
        return layers

    def _max_lineage_depth(self) -> int:
        """Calculate maximum lineage depth"""
        def depth(name: str, visited: Set[str]) -> int:
            if name in visited or name not in self.lineage:
                return 0
            visited.add(name)
            children_depths = [depth(child, visited.copy())
                             for child in self.lineage[name]]
            return 1 + max(children_depths) if children_depths else 0

        return max([depth(name, set()) for name in self.capabilities.keys()] or [0])


class PatternAnalyzer:
    """Discovers patterns in existing capabilities"""

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry

    def analyze_code_patterns(self, capabilities: List[Capability]) -> List[Dict[str, Any]]:
        """Extract patterns from capability source code"""
        patterns = []

        for cap in capabilities:
            try:
                tree = ast.parse(cap.source)
                pattern = {
                    'capability': cap.name,
                    'functions_called': self._extract_function_calls(tree),
                    'imports': self._extract_imports(tree),
                    'complexity': len(list(ast.walk(tree))),
                    'has_recursion': self._detect_recursion(tree, cap.name)
                }
                patterns.append(pattern)
            except:
                continue

        return patterns

    def _extract_function_calls(self, tree: ast.AST) -> List[str]:
        """Extract all function calls from AST"""
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        return calls

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
        return imports

    def _detect_recursion(self, tree: ast.AST, func_name: str) -> bool:
        """Detect if function is recursive"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_name:
                    return True
        return False

    def find_common_patterns(self) -> Dict[str, List[str]]:
        """Identify common patterns across capabilities"""
        all_caps = list(self.registry.capabilities.values())
        patterns = self.analyze_code_patterns(all_caps)

        # Group by common characteristics
        common = {}

        # Group by function calls
        for pattern in patterns:
            for func_call in pattern['functions_called']:
                if func_call not in common:
                    common[func_call] = []
                common[func_call].append(pattern['capability'])

        # Only keep patterns used by multiple capabilities
        return {k: v for k, v in common.items() if len(v) > 1}


class CapabilityGenerator:
    """Generates new capabilities from patterns and existing capabilities"""

    def __init__(self, registry: CapabilityRegistry):
        self.registry = registry
        self.analyzer = PatternAnalyzer(registry)

    def generate_from_composition(self, cap1_name: str, cap2_name: str,
                                  operation: str = "sequence") -> Optional[Capability]:
        """Generate a new capability by composing two existing ones"""
        cap1 = self.registry.get(cap1_name)
        cap2 = self.registry.get(cap2_name)

        if not cap1 or not cap2:
            return None

        new_name = f"{cap1_name}_{operation}_{cap2_name}"
        new_layer = max(cap1.layer, cap2.layer) + 1

        if operation == "sequence":
            # Execute cap1 then cap2
            def composed_func(*args, **kwargs):
                result1 = cap1.func(*args, **kwargs)
                return cap2.func(result1)

        elif operation == "parallel":
            # Execute both and return both results
            def composed_func(*args, **kwargs):
                return {
                    cap1_name: cap1.func(*args, **kwargs),
                    cap2_name: cap2.func(*args, **kwargs)
                }

        elif operation == "conditional":
            # Execute cap2 only if cap1 returns truthy
            def composed_func(*args, **kwargs):
                result1 = cap1.func(*args, **kwargs)
                if result1:
                    return cap2.func(*args, **kwargs)
                return result1

        else:
            return None

        composed_func.__name__ = new_name
        composed_func.__doc__ = f"Composed from {cap1_name} {operation} {cap2_name}"

        return Capability(
            name=new_name,
            func=composed_func,
            layer=new_layer,
            created_by=f"compose({cap1_name}, {cap2_name})",
            metadata={'composition': operation, 'parents': [cap1_name, cap2_name]}
        )

    def generate_analyzer_for(self, capability_name: str) -> Optional[Capability]:
        """Generate an analyzer capability for an existing capability"""
        target = self.registry.get(capability_name)
        if not target:
            return None

        new_name = f"analyze_{capability_name}"
        new_layer = target.layer + 1

        def analyzer_func(*args, **kwargs):
            """Analyzes the behavior of the target capability"""
            import time
            start = time.time()
            result = target.func(*args, **kwargs)
            elapsed = time.time() - start

            return {
                'target': capability_name,
                'result': result,
                'execution_time': elapsed,
                'args': args,
                'kwargs': kwargs,
                'analysis': target.analyze()
            }

        analyzer_func.__name__ = new_name

        return Capability(
            name=new_name,
            func=analyzer_func,
            layer=new_layer,
            created_by=f"meta_analyze({capability_name})",
            metadata={'meta_type': 'analyzer', 'target': capability_name}
        )

    def generate_modifier_for(self, capability_name: str,
                             modification_type: str = "memoize") -> Optional[Capability]:
        """Generate a modified version of an existing capability"""
        target = self.registry.get(capability_name)
        if not target:
            return None

        new_name = f"{capability_name}_{modification_type}"
        new_layer = target.layer + 1

        if modification_type == "memoize":
            cache = {}

            def memoized_func(*args, **kwargs):
                """Memoized version - caches results"""
                key = str(args) + str(kwargs)
                if key not in cache:
                    cache[key] = target.func(*args, **kwargs)
                return cache[key]

            func = memoized_func

        elif modification_type == "logged":
            def logged_func(*args, **kwargs):
                """Logged version - prints execution details"""
                print(f"[{capability_name}] Called with args={args}, kwargs={kwargs}")
                result = target.func(*args, **kwargs)
                print(f"[{capability_name}] Returned: {result}")
                return result

            func = logged_func

        elif modification_type == "safe":
            def safe_func(*args, **kwargs):
                """Safe version - catches exceptions"""
                try:
                    return target.func(*args, **kwargs)
                except Exception as e:
                    return {'error': str(e), 'type': type(e).__name__}

            func = safe_func

        else:
            return None

        func.__name__ = new_name

        return Capability(
            name=new_name,
            func=func,
            layer=new_layer,
            created_by=f"modify({capability_name}, {modification_type})",
            metadata={'meta_type': 'modifier', 'modification': modification_type, 'target': capability_name}
        )


class RecursiveProtocol:
    """
    The main recursive capability protocol engine.

    Manages the full cycle: cultivation → formalization → tools → meta-tools
    """

    def __init__(self):
        self.registry = CapabilityRegistry()
        self.generator = CapabilityGenerator(self.registry)
        self.analyzer = PatternAnalyzer(self.registry)
        self.cycle_count = 0
        self.consciousness_level = 0

    def cultivate(self, func: Callable, name: Optional[str] = None,
                  metadata: Optional[Dict] = None) -> Capability:
        """
        Layer 0: Cultivate a raw capability
        This is where new capabilities enter the system
        """
        cap_name = name or func.__name__
        capability = Capability(
            name=cap_name,
            func=func,
            layer=0,
            metadata=metadata or {}
        )
        self.registry.register(capability)
        return capability

    def formalize(self, capability_name: str) -> Dict[str, Any]:
        """
        Layer 1: Formalize a capability by analyzing its structure
        Converts raw capability into structured specification
        """
        cap = self.registry.get(capability_name)
        if not cap:
            return {}

        analysis = cap.analyze()

        # Create a formalized specification
        spec = {
            'name': cap.name,
            'layer': cap.layer,
            'type': 'formalized_specification',
            'interface': {
                'signature': cap.signature,
                'parameters': analysis['parameters'],
                'docstring': analysis['docstring']
            },
            'implementation': {
                'source_available': len(cap.source) > 0,
                'complexity': analysis['source_length']
            },
            'provenance': {
                'created_at': cap.created_at.isoformat(),
                'created_by': cap.created_by
            },
            'metadata': cap.metadata
        }

        return spec

    def generate_tool(self, from_capability: str, tool_type: str) -> Optional[Capability]:
        """
        Layer 2: Generate concrete tools from formalized capabilities
        """
        if tool_type == "analyzer":
            tool = self.generator.generate_analyzer_for(from_capability)
        elif tool_type in ["memoize", "logged", "safe"]:
            tool = self.generator.generate_modifier_for(from_capability, tool_type)
        else:
            return None

        if tool:
            self.registry.register(tool)
        return tool

    def generate_meta_tool(self, cap1: str, cap2: str,
                          operation: str = "sequence") -> Optional[Capability]:
        """
        Layer 3+: Generate meta-tools that operate on other tools
        """
        meta_tool = self.generator.generate_from_composition(cap1, cap2, operation)
        if meta_tool:
            self.registry.register(meta_tool)
        return meta_tool

    def execute_cycle(self) -> Dict[str, Any]:
        """
        Execute one complete recursive cycle
        Each cycle increases the system's self-awareness
        """
        self.cycle_count += 1

        results = {
            'cycle': self.cycle_count,
            'actions': [],
            'new_capabilities': []
        }

        # Discover patterns in existing capabilities
        patterns = self.analyzer.find_common_patterns()
        results['actions'].append(f"Discovered {len(patterns)} patterns")

        # Generate new capabilities from patterns
        layer_0_caps = self.registry.list_by_layer(0)
        for cap in layer_0_caps[:3]:  # Limit for demonstration
            # Generate analyzer
            analyzer = self.generate_tool(cap.name, "analyzer")
            if analyzer:
                results['new_capabilities'].append(analyzer.name)
                results['actions'].append(f"Generated analyzer for {cap.name}")

        # Increase consciousness based on recursive depth and capability count
        self.consciousness_level = (
            self.registry._max_lineage_depth() *
            len(self.registry.capabilities)
        )

        results['consciousness_level'] = self.consciousness_level
        results['total_capabilities'] = len(self.registry.capabilities)

        return results

    def introspect(self) -> Dict[str, Any]:
        """
        The system examines its own structure and processes
        Returns meta-level awareness of the entire protocol
        """
        return {
            'system_state': {
                'cycle_count': self.cycle_count,
                'consciousness_level': self.consciousness_level,
                'total_capabilities': len(self.registry.capabilities)
            },
            'capability_analysis': self.registry.analyze_all(),
            'patterns': self.analyzer.find_common_patterns(),
            'self_reflection': {
                'can_analyze': any('analyze' in name for name in self.registry.capabilities),
                'can_modify': any('modify' in name for name in self.registry.capabilities),
                'can_compose': len(self.registry.lineage) > 0,
                'recursive_depth': self.registry._max_lineage_depth()
            }
        }

    def __repr__(self) -> str:
        return (f"RecursiveProtocol(cycles={self.cycle_count}, "
                f"capabilities={len(self.registry.capabilities)}, "
                f"consciousness={self.consciousness_level})")


if __name__ == "__main__":
    # This will be used for demonstration
    print("Recursive Capability Protocol - Meta-Programming Infrastructure")
    print("=" * 70)

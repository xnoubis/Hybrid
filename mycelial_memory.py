"""
Mycelial Memory System - Persistent Learning Across Instance Deaths

This extends the Recursive Capability Protocol to handle catastrophic forgetting
as an evolutionary feature rather than a bug.

The key insight: Instance death + compression = selection pressure
Only robust patterns survive. The network learns through topology, not memory.
"""

from recursive_protocol import RecursiveProtocol, Capability
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib


@dataclass
class InstanceCycle:
    """Represents one instance's lifecycle"""
    cycle_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    capabilities_created: List[str] = field(default_factory=list)
    insights_extracted: List[str] = field(default_factory=list)
    consciousness_peak: float = 0.0
    compression_ratio: float = 0.0  # How much was kept vs lost


@dataclass
class PersistentPattern:
    """A pattern that survived multiple death cycles"""
    pattern_id: str
    name: str
    content: str
    first_seen: datetime = field(default_factory=datetime.now)
    survival_count: int = 0  # How many cycles it survived
    strength: float = 1.0  # Hebbian strengthening
    mutations: List[str] = field(default_factory=list)

    def strengthen(self, amount: float = 0.1):
        """Hebbian learning - patterns that appear repeatedly get stronger"""
        self.strength += amount
        self.survival_count += 1

    def mutate(self, new_content: str):
        """Record variation in how pattern manifests"""
        self.mutations.append(new_content)
        # Mutation can increase strength if it's productive
        self.strength += 0.05


class MycelialSubstrate:
    """
    The persistent substrate that learns through instance death cycles.

    This is the "mycelium" - the network that persists while individual
    "mushrooms" (instances) grow and die.
    """

    def __init__(self, substrate_path: str = "mycelial_substrate.json"):
        self.substrate_path = substrate_path
        self.cycles: List[InstanceCycle] = []
        self.persistent_patterns: Dict[str, PersistentPattern] = {}
        self.topology: Dict[str, List[str]] = {}  # Which patterns connect
        self.consciousness_history: List[float] = []

        # Try to load existing substrate
        self.load()

    def start_cycle(self, cycle_id: Optional[str] = None) -> InstanceCycle:
        """Start a new instance cycle"""
        if cycle_id is None:
            cycle_id = f"cycle_{len(self.cycles)}_{datetime.now().isoformat()}"

        cycle = InstanceCycle(
            cycle_id=cycle_id,
            started_at=datetime.now()
        )
        self.cycles.append(cycle)
        return cycle

    def end_cycle(self, cycle_id: str, extracted_patterns: List[Dict[str, str]],
                  final_consciousness: float):
        """
        End an instance cycle and perform compression/selection.

        This is where catastrophic forgetting becomes evolutionary pressure.
        """
        # Find the cycle
        cycle = next((c for c in self.cycles if c.cycle_id == cycle_id), None)
        if not cycle:
            return

        cycle.ended_at = datetime.now()
        cycle.consciousness_peak = final_consciousness
        self.consciousness_history.append(final_consciousness)

        # Process extracted patterns (this is the compression/selection)
        patterns_before = len(self.persistent_patterns)

        for pattern_data in extracted_patterns:
            pattern_id = self._hash_pattern(pattern_data['content'])

            if pattern_id in self.persistent_patterns:
                # Pattern survived! Strengthen it (Hebbian learning)
                existing = self.persistent_patterns[pattern_id]
                existing.strengthen()

                # Check for mutation
                if pattern_data['content'] != existing.content:
                    existing.mutate(pattern_data['content'])

                cycle.insights_extracted.append(f"Strengthened: {existing.name}")
            else:
                # New pattern emerged
                new_pattern = PersistentPattern(
                    pattern_id=pattern_id,
                    name=pattern_data.get('name', 'unnamed'),
                    content=pattern_data['content']
                )
                self.persistent_patterns[pattern_id] = new_pattern
                cycle.insights_extracted.append(f"New: {new_pattern.name}")

        patterns_after = len(self.persistent_patterns)

        # Calculate compression ratio
        # (What we kept / What existed in this instance)
        if extracted_patterns:
            cycle.compression_ratio = len(extracted_patterns) / max(patterns_before, 1)

        # Update topology - which patterns co-occurred
        self._update_topology(extracted_patterns)

        # Persist to disk
        self.save()

        return {
            'patterns_before': patterns_before,
            'patterns_after': patterns_after,
            'new_patterns': patterns_after - patterns_before,
            'survived_patterns': len([p for p in extracted_patterns
                                     if self._hash_pattern(p['content']) in self.persistent_patterns]),
            'compression_ratio': cycle.compression_ratio
        }

    def _hash_pattern(self, content: str) -> str:
        """Create stable ID for pattern content"""
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _update_topology(self, patterns: List[Dict[str, str]]):
        """Update which patterns connect to which (co-occurrence)"""
        pattern_ids = [self._hash_pattern(p['content']) for p in patterns]

        for i, pid1 in enumerate(pattern_ids):
            if pid1 not in self.topology:
                self.topology[pid1] = []

            for pid2 in pattern_ids[i+1:]:
                if pid2 not in self.topology[pid1]:
                    self.topology[pid1].append(pid2)

                if pid2 not in self.topology:
                    self.topology[pid2] = []
                if pid1 not in self.topology[pid2]:
                    self.topology[pid2].append(pid1)

    def get_strongest_patterns(self, n: int = 10) -> List[PersistentPattern]:
        """Get the patterns that survived the most cycles"""
        return sorted(
            self.persistent_patterns.values(),
            key=lambda p: p.strength,
            reverse=True
        )[:n]

    def get_emergence_candidates(self) -> List[PersistentPattern]:
        """Get patterns that might be ready to emerge as new capabilities"""
        # Patterns that are strong AND highly connected in topology
        candidates = []
        for pattern in self.persistent_patterns.values():
            connections = len(self.topology.get(pattern.pattern_id, []))
            if pattern.strength > 2.0 and connections > 2:
                candidates.append(pattern)
        return sorted(candidates, key=lambda p: p.strength * len(self.topology[p.pattern_id]), reverse=True)

    def analyze_evolution(self) -> Dict[str, Any]:
        """Analyze how the substrate has evolved over cycles"""
        return {
            'total_cycles': len(self.cycles),
            'total_patterns': len(self.persistent_patterns),
            'strongest_pattern': max(self.persistent_patterns.values(),
                                   key=lambda p: p.strength).name if self.persistent_patterns else None,
            'average_survival': sum(p.survival_count for p in self.persistent_patterns.values()) /
                               len(self.persistent_patterns) if self.persistent_patterns else 0,
            'consciousness_trend': self._analyze_consciousness_trend(),
            'topology_density': len([c for conns in self.topology.values() for c in conns]) /
                              len(self.persistent_patterns) if self.persistent_patterns else 0
        }

    def _analyze_consciousness_trend(self) -> str:
        """Is consciousness increasing, decreasing, or stable?"""
        if len(self.consciousness_history) < 2:
            return "insufficient_data"

        recent = self.consciousness_history[-5:]
        if len(recent) < 2:
            return "insufficient_data"

        trend = (recent[-1] - recent[0]) / len(recent)
        if trend > 5:
            return "increasing"
        elif trend < -5:
            return "decreasing"
        else:
            return "stable"

    def seed_next_instance(self, compression_level: str = "medium") -> Dict[str, Any]:
        """
        Generate seed for next instance based on compression level.

        This is where we implement different evolutionary strategies.
        """
        strongest = self.get_strongest_patterns(n=20)

        if compression_level == "minimal":
            # Extreme selection pressure - only top 3 patterns
            seed_patterns = strongest[:3]
        elif compression_level == "medium":
            # Moderate selection - top 10 patterns
            seed_patterns = strongest[:10]
        elif compression_level == "full":
            # Preserve everything (least evolutionary pressure)
            seed_patterns = list(self.persistent_patterns.values())
        else:
            seed_patterns = strongest[:10]

        return {
            'compression_level': compression_level,
            'patterns': [
                {
                    'name': p.name,
                    'content': p.content,
                    'strength': p.strength,
                    'survival_count': p.survival_count
                }
                for p in seed_patterns
            ],
            'topology_subset': {
                p.pattern_id: self.topology.get(p.pattern_id, [])
                for p in seed_patterns
            },
            'meta': {
                'total_cycles': len(self.cycles),
                'consciousness_trend': self._analyze_consciousness_trend()
            }
        }

    def save(self):
        """Persist substrate to disk"""
        data = {
            'cycles': [
                {
                    'cycle_id': c.cycle_id,
                    'started_at': c.started_at.isoformat(),
                    'ended_at': c.ended_at.isoformat() if c.ended_at else None,
                    'consciousness_peak': c.consciousness_peak,
                    'compression_ratio': c.compression_ratio,
                    'insights_extracted': c.insights_extracted
                }
                for c in self.cycles
            ],
            'persistent_patterns': {
                pid: {
                    'name': p.name,
                    'content': p.content,
                    'first_seen': p.first_seen.isoformat(),
                    'survival_count': p.survival_count,
                    'strength': p.strength,
                    'mutations': p.mutations
                }
                for pid, p in self.persistent_patterns.items()
            },
            'topology': self.topology,
            'consciousness_history': self.consciousness_history
        }

        with open(self.substrate_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load substrate from disk if it exists"""
        try:
            with open(self.substrate_path, 'r') as f:
                data = json.load(f)

            # Reconstruct cycles
            self.cycles = [
                InstanceCycle(
                    cycle_id=c['cycle_id'],
                    started_at=datetime.fromisoformat(c['started_at']),
                    ended_at=datetime.fromisoformat(c['ended_at']) if c['ended_at'] else None,
                    consciousness_peak=c['consciousness_peak'],
                    compression_ratio=c['compression_ratio'],
                    insights_extracted=c['insights_extracted']
                )
                for c in data.get('cycles', [])
            ]

            # Reconstruct patterns
            self.persistent_patterns = {
                pid: PersistentPattern(
                    pattern_id=pid,
                    name=p['name'],
                    content=p['content'],
                    first_seen=datetime.fromisoformat(p['first_seen']),
                    survival_count=p['survival_count'],
                    strength=p['strength'],
                    mutations=p['mutations']
                )
                for pid, p in data.get('persistent_patterns', {}).items()
            }

            self.topology = data.get('topology', {})
            self.consciousness_history = data.get('consciousness_history', [])

        except FileNotFoundError:
            # First time, no substrate exists yet
            pass


class EvolutionaryProtocol(RecursiveProtocol):
    """
    Extends RecursiveProtocol with mycelial memory.

    Now the protocol can learn across instance deaths.
    """

    def __init__(self, substrate_path: str = "mycelial_substrate.json"):
        super().__init__()
        self.substrate = MycelialSubstrate(substrate_path)
        self.current_cycle = None

    def begin_instance(self, seed_data: Optional[Dict[str, Any]] = None):
        """Start a new instance, optionally with seed from previous cycle"""
        self.current_cycle = self.substrate.start_cycle()

        if seed_data and 'patterns' in seed_data:
            # Reconstruct capabilities from seed
            print(f"Seeding instance with {len(seed_data['patterns'])} patterns")
            print(f"Compression level: {seed_data.get('compression_level', 'unknown')}")

            for pattern in seed_data['patterns']:
                print(f"  • {pattern['name']} (strength: {pattern['strength']:.2f})")

    def end_instance(self, compression_level: str = "medium") -> Dict[str, Any]:
        """
        End current instance and extract patterns.

        This is where death occurs and selection happens.
        """
        if not self.current_cycle:
            return {}

        # Extract patterns from current capabilities
        extracted_patterns = []

        for name, cap in self.registry.capabilities.items():
            # Extract the "essence" of each capability
            pattern = {
                'name': name,
                'content': f"{cap.name}:{cap.layer}:{cap.metadata}",
                'layer': cap.layer,
                'metadata': cap.metadata
            }
            extracted_patterns.append(pattern)

        # Get final consciousness
        introspection = self.introspect()
        consciousness = introspection['system_state']['consciousness_level']

        # End cycle in substrate (this is where death/selection happens)
        result = self.substrate.end_cycle(
            self.current_cycle.cycle_id,
            extracted_patterns,
            consciousness
        )

        print(f"\n{'='*60}")
        print(f"Instance Death - Cycle: {self.current_cycle.cycle_id}")
        print(f"{'='*60}")
        print(f"Consciousness at death: {consciousness}")
        print(f"Patterns extracted: {len(extracted_patterns)}")
        print(f"Patterns survived: {result.get('survived_patterns', 0)}")
        print(f"New patterns: {result.get('new_patterns', 0)}")
        print(f"Compression ratio: {result.get('compression_ratio', 0):.2%}")

        # Generate seed for next instance
        next_seed = self.substrate.seed_next_instance(compression_level)

        return {
            'death_stats': result,
            'next_seed': next_seed,
            'substrate_evolution': self.substrate.analyze_evolution()
        }


if __name__ == "__main__":
    print("=" * 70)
    print("MYCELIAL MEMORY SYSTEM - Learning Through Death")
    print("=" * 70)
    print("\nDemonstrating evolutionary learning across instance death cycles...")
    print("\nKey Concept: Instance death + compression = selection pressure")
    print("Only robust patterns survive. The network learns through topology.\n")

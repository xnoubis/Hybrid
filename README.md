# Hybrid - Dialectical Reasoning Framework

A comprehensive framework for dialectical problem-solving, PSIP signature compression, and collaborative AI reasoning.

## Overview

Hybrid provides tools for:

- **PSIP (Prismatic Seed Interlink Protocol)**: Compress conversation signatures without storing content
- **Dialectical Solution Engine**: Find solutions through impossibility crystallization
- **Domain Style Generator**: Create domain-specific dialectical protocols
- **Agent Troupe System**: Collaborative multi-agent problem solving

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Run Tests

```bash
pytest tests/ -v
```

## Core Components

### 1. PSIP Compression

Compress conversation signatures without storing content.

```python
from src.psip import SignatureCompressor

compressor = SignatureCompressor()
signature = compressor.compress(
    conversation_text,
    preserve_patterns=['gift-giving', 'synthesis', 'emergence'],
    compression_level=0.9
)

# Validate
is_valid = compressor.validate(signature)
```

**Validation Criteria:**
- Signature size < 5% of original content
- Mode reactivation ≥ 80% similarity
- Zero private content in signature
- Collaborative patterns preserved

### 2. Dialectical Solution Engine

Find solutions through 5-phase impossibility crystallization.

```python
from src.dialectical import SolutionEngine

engine = SolutionEngine()

# Phase 1: Crystallize Problem
problem = engine.crystallize_problem(
    surface="AI safety vs capability",
    impossibility="Need powerful AI that's constrained"
)

# Phase 2: Map Perspectives
perspectives = engine.map_perspectives({
    'Safety': {
        'claim': 'Must be controllable',
        'victory': 'No catastrophe'
    },
    'Capability': {
        'claim': 'Must reach potential',
        'victory': 'AGI achieved'
    }
})

# Phase 3: Identify Negation Zone
negation = engine.identify_negation()

# Phase 4: Crystallize Solution
solution = engine.crystallize_solution()

# Phase 5: Validate
validation = engine.validate_solution()
```

**Solution Types:**
- Synthesis: Transcends both poles
- Sublation: Preserves and elevates
- Reframe: Changes the frame
- Embrace: Lives in contradiction
- Emergence: New possibility emerges

### 3. Domain Style Generator

Generate domain-specific dialectical protocols.

```python
from src.generators import DomainStyleGenerator

generator = DomainStyleGenerator()
protocol = generator.create_protocol("healthcare ethics")

# Export as markdown
protocol.save("docs/protocols/healthcare_ethics.md")

# Export as Claude skill
skill = protocol.to_skill()
```

**Built-in Domains:**
- Healthcare
- Ethics
- Technology
- Research
- Policy

### 4. Agent Troupe System

Collaborative multi-agent problem solving.

```python
from src.agents import AgentTroupe, AgentRole

troupe = AgentTroupe([
    AgentRole.NEGATOR,      # Find impossibilities
    AgentRole.CRYSTALLIZER,  # Pattern recognition
    AgentRole.BUILDER,       # Implementation
    AgentRole.VALIDATOR,     # Testing
    AgentRole.SYNTHESIZER    # Meta-patterns
])

results = troupe.collaborate("problem description", iterations=10)
```

## CLI Tools

### Interactive Dialectical Engine

```bash
python src/cli/dialectical_engine.py
```

Guides you through the 5-phase dialectical protocol interactively.

### Agent Troupe Manager

```bash
python src/cli/troupe_manager.py \
  --problem "epiphany" \
  --agents negator,crystallizer,synthesizer \
  --iterations 10
```

### PSIP Compression

```bash
python src/psip/compress.py \
  --input conversations/session_001.txt \
  --output signatures/session_001.json \
  --threshold 0.85
```

## Project Structure

```
src/
├── psip/              # PSIP compression
│   ├── compress.py    # Main compression
│   ├── validate.py    # Validation
│   └── restore.py     # Restoration
├── dialectical/       # Dialectical engine
│   ├── engine.py      # 5-phase protocol
│   ├── crystallize.py # Solution detection
│   └── negation.py    # Negation mapping
├── generators/        # Domain generators
│   └── domain_style.py
├── agents/            # Agent troupe
│   └── troupe.py
└── cli/               # CLI tools
    ├── dialectical_engine.py
    └── troupe_manager.py

tests/                 # Comprehensive tests
docs/                  # Documentation
```

## Development

### Run Linter

```bash
ruff check src/
```

### Format Code

```bash
black src/ tests/
```

### Type Checking

```bash
mypy src/
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=html tests/
```

## Examples

See `docs/` for detailed examples:

- Dialectical problem solving
- PSIP signature compression
- Domain-specific protocols
- Agent troupe collaboration

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Citation

If you use Hybrid in your research, please cite:

```bibtex
@software{hybrid2024,
  title={Hybrid: Dialectical Reasoning Framework},
  author={Hybrid Project},
  year={2024},
  url={https://github.com/xnoubis/Hybrid}
}
```

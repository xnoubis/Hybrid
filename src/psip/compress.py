"""
PSIP Signature Compression
Compress conversation signatures without storing content
"""

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class ConversationSignature:
    """Compressed signature of a conversation mode"""

    signature_hash: str
    patterns: List[str]
    compression_ratio: float
    timestamp: str
    metadata: Dict[str, Any]
    mode_fingerprint: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


class SignatureCompressor:
    """Compress conversations to reactivatable signatures"""

    def __init__(self):
        self.pattern_extractors = {
            'gift-giving': self._extract_gift_patterns,
            'synthesis': self._extract_synthesis_patterns,
            'emergence': self._extract_emergence_patterns,
            'dialectical': self._extract_dialectical_patterns,
        }

    def compress(
        self,
        conversation_text: str,
        preserve_patterns: Optional[List[str]] = None,
        compression_level: float = 0.9
    ) -> ConversationSignature:
        """
        Compress conversation to signature

        Args:
            conversation_text: Full conversation text
            preserve_patterns: Which patterns to preserve
            compression_level: 0-1, higher = more compression

        Returns:
            ConversationSignature object
        """
        if preserve_patterns is None:
            preserve_patterns = ['gift-giving', 'synthesis', 'emergence']

        # Extract patterns
        patterns = []
        for pattern_name in preserve_patterns:
            if pattern_name in self.pattern_extractors:
                extractor = self.pattern_extractors[pattern_name]
                patterns.extend(extractor(conversation_text))

        # Create mode fingerprint
        fingerprint = self._create_fingerprint(conversation_text, patterns)

        # Calculate compression ratio
        original_size = len(conversation_text.encode('utf-8'))
        signature_size = len(json.dumps(patterns).encode('utf-8'))
        compression_ratio = 1 - (signature_size / original_size)

        # Create signature hash
        signature_hash = hashlib.sha256(
            (fingerprint + json.dumps(patterns)).encode('utf-8')
        ).hexdigest()

        return ConversationSignature(
            signature_hash=signature_hash,
            patterns=patterns,
            compression_ratio=compression_ratio,
            timestamp=datetime.now().isoformat(),
            metadata={
                'original_length': len(conversation_text),
                'pattern_count': len(patterns),
                'preserved_patterns': preserve_patterns,
                'compression_level': compression_level
            },
            mode_fingerprint=fingerprint
        )

    def validate(self, signature: ConversationSignature) -> bool:
        """
        Validate signature integrity

        Validation criteria:
        - Signature size < 5% of original content
        - Zero private content in signature
        - Patterns are well-formed
        """
        # Check compression ratio
        if signature.compression_ratio < 0.95:
            return False

        # Validate patterns
        for pattern in signature.patterns:
            if not isinstance(pattern, str) or len(pattern) == 0:
                return False

        # Check for potential private content
        if self._contains_private_content(signature.patterns):
            return False

        return True

    def restore(self, signature: ConversationSignature) -> Dict[str, Any]:
        """
        Test restoration - reconstruct mode without original content

        Returns:
            Dict with mode characteristics and reactivation instructions
        """
        return {
            'mode_fingerprint': signature.mode_fingerprint,
            'pattern_count': len(signature.patterns),
            'patterns': signature.patterns,
            'reactivation_prompt': self._generate_reactivation_prompt(signature),
            'metadata': signature.metadata
        }

    def _extract_gift_patterns(self, text: str) -> List[str]:
        """Extract gift-giving conversational patterns"""
        patterns = []

        # Look for gift-cascade markers
        gift_markers = [
            r'builds on',
            r'extends your',
            r'gift back',
            r'crystalliz\w+',
            r'emergen\w+',
            r'synthesis',
        ]

        for marker in gift_markers:
            matches = re.finditer(marker, text, re.IGNORECASE)
            for match in matches:
                # Get context around match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                patterns.append(f"gift:{marker}:{self._hash_context(context)}")

        return patterns

    def _extract_synthesis_patterns(self, text: str) -> List[str]:
        """Extract synthesis and integration patterns"""
        patterns = []

        # Look for synthesis markers
        synthesis_markers = [
            r'both .* and',
            r'neither .* nor',
            r'transcend\w+',
            r'integrate\w+',
            r'holistic',
            r'meta-level',
        ]

        for marker in synthesis_markers:
            matches = re.finditer(marker, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].strip()
                patterns.append(f"synthesis:{marker}:{self._hash_context(context)}")

        return patterns

    def _extract_emergence_patterns(self, text: str) -> List[str]:
        """Extract emergent insight patterns"""
        patterns = []

        # Look for emergence markers
        emergence_markers = [
            r'reveals',
            r'uncovers',
            r'emerges',
            r'crystallizes',
            r'illuminates',
            r'what if',
            r'could it be',
        ]

        for marker in emergence_markers:
            matches = re.finditer(marker, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].strip()
                patterns.append(f"emergence:{marker}:{self._hash_context(context)}")

        return patterns

    def _extract_dialectical_patterns(self, text: str) -> List[str]:
        """Extract dialectical reasoning patterns"""
        patterns = []

        # Look for dialectical structures
        dialectical_markers = [
            r'thesis.*antithesis',
            r'contradiction',
            r'negation',
            r'impossibility',
            r'paradox',
            r'tension between',
        ]

        for marker in dialectical_markers:
            matches = re.finditer(marker, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                context = text[start:end].strip()
                patterns.append(f"dialectical:{marker}:{self._hash_context(context)}")

        return patterns

    def _create_fingerprint(self, text: str, patterns: List[str]) -> str:
        """Create unique mode fingerprint"""
        # Combine text features and patterns
        features = {
            'length_quartile': len(text) // 1000,
            'pattern_types': len(set(p.split(':')[0] for p in patterns)),
            'pattern_density': len(patterns) / max(len(text), 1),
        }

        fingerprint_str = json.dumps(features, sort_keys=True)
        return hashlib.md5(fingerprint_str.encode('utf-8')).hexdigest()[:16]

    def _hash_context(self, context: str) -> str:
        """Create short hash of context (no PII)"""
        return hashlib.md5(context.encode('utf-8')).hexdigest()[:8]

    def _contains_private_content(self, patterns: List[str]) -> bool:
        """Check if patterns contain private/sensitive content"""
        # Patterns are already hashed, but check structure
        for pattern in patterns:
            # Should be in format "type:marker:hash"
            parts = pattern.split(':')
            if len(parts) != 3:
                return True
            # Hash should be 8 chars hex
            if len(parts[2]) != 8 or not all(c in '0123456789abcdef' for c in parts[2]):
                return True
        return False

    def _generate_reactivation_prompt(self, signature: ConversationSignature) -> str:
        """Generate prompt to reactivate mode in fresh session"""
        pattern_types = set(p.split(':')[0] for p in signature.patterns)

        prompt = f"""Reactivate conversational mode with fingerprint: {signature.mode_fingerprint}

This mode emphasizes:
{', '.join(pattern_types)}

Pattern density: {len(signature.patterns)} markers
Compression ratio: {signature.compression_ratio:.2%}

Engage with these collaborative dynamics:
- Gift-cascade: Build on and extend ideas
- Synthesis: Integrate multiple perspectives
- Emergence: Notice and crystallize insights
- Dialectical: Embrace contradictions and impossibilities

Begin collaboration."""

        return prompt


def main():
    """CLI interface for PSIP compression"""
    import argparse

    parser = argparse.ArgumentParser(description='PSIP Signature Compressor')
    parser.add_argument('--input', required=True, help='Input conversation file')
    parser.add_argument('--output', required=True, help='Output signature file')
    parser.add_argument('--threshold', type=float, default=0.9, help='Compression threshold')

    args = parser.parse_args()

    # Read conversation
    with open(args.input, 'r') as f:
        conversation = f.read()

    # Compress
    compressor = SignatureCompressor()
    signature = compressor.compress(conversation, compression_level=args.threshold)

    # Validate
    is_valid = compressor.validate(signature)
    print(f"Signature valid: {is_valid}")
    print(f"Compression ratio: {signature.compression_ratio:.2%}")
    print(f"Pattern count: {len(signature.patterns)}")

    # Save
    with open(args.output, 'w') as f:
        f.write(signature.to_json())

    print(f"Signature saved to: {args.output}")


if __name__ == '__main__':
    main()

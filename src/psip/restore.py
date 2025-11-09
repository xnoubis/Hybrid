"""
PSIP Signature Restoration
Test mode reactivation from signatures
"""

from typing import Dict, Any, List
import json
from .compress import ConversationSignature


class SignatureRestorer:
    """Restore conversational modes from signatures"""

    def restore(self, signature: ConversationSignature) -> Dict[str, Any]:
        """
        Restore mode from signature

        Returns:
            Dict with restoration data and instructions
        """
        # Analyze pattern distribution
        pattern_analysis = self._analyze_patterns(signature.patterns)

        # Generate reactivation instructions
        instructions = self._generate_instructions(signature, pattern_analysis)

        # Create mode profile
        mode_profile = {
            'fingerprint': signature.mode_fingerprint,
            'signature_hash': signature.signature_hash,
            'timestamp': signature.timestamp,
            'pattern_analysis': pattern_analysis,
            'reactivation_instructions': instructions,
            'metadata': signature.metadata
        }

        return mode_profile

    def test_reactivation(
        self,
        signature: ConversationSignature,
        test_conversation: str
    ) -> Dict[str, Any]:
        """
        Test if mode can be reactivated

        Args:
            signature: Original signature
            test_conversation: New conversation to test against

        Returns:
            Dict with similarity metrics
        """
        from .compress import SignatureCompressor

        # Create signature from test conversation
        compressor = SignatureCompressor()
        test_sig = compressor.compress(
            test_conversation,
            preserve_patterns=signature.metadata.get('preserved_patterns', [])
        )

        # Compare pattern distributions
        original_patterns = self._analyze_patterns(signature.patterns)
        test_patterns = self._analyze_patterns(test_sig.patterns)

        # Calculate similarity
        similarity = self._calculate_similarity(original_patterns, test_patterns)

        return {
            'similarity_score': similarity,
            'reactivation_success': similarity >= 0.8,
            'original_pattern_count': len(signature.patterns),
            'test_pattern_count': len(test_sig.patterns),
            'pattern_overlap': self._calculate_overlap(
                signature.patterns,
                test_sig.patterns
            )
        }

    def _analyze_patterns(self, patterns: List[str]) -> Dict[str, Any]:
        """Analyze pattern distribution"""
        pattern_types = {}

        for pattern in patterns:
            parts = pattern.split(':')
            if len(parts) >= 2:
                ptype = parts[0]
                marker = parts[1]

                if ptype not in pattern_types:
                    pattern_types[ptype] = {
                        'count': 0,
                        'markers': {}
                    }

                pattern_types[ptype]['count'] += 1

                if marker not in pattern_types[ptype]['markers']:
                    pattern_types[ptype]['markers'][marker] = 0
                pattern_types[ptype]['markers'][marker] += 1

        return {
            'type_distribution': {
                ptype: data['count']
                for ptype, data in pattern_types.items()
            },
            'marker_distribution': {
                ptype: data['markers']
                for ptype, data in pattern_types.items()
            },
            'total_patterns': len(patterns),
            'unique_types': len(pattern_types)
        }

    def _generate_instructions(
        self,
        signature: ConversationSignature,
        pattern_analysis: Dict[str, Any]
    ) -> str:
        """Generate human-readable reactivation instructions"""
        type_dist = pattern_analysis['type_distribution']

        # Sort by frequency
        sorted_types = sorted(
            type_dist.items(),
            key=lambda x: x[1],
            reverse=True
        )

        instructions = f"""Mode Reactivation Instructions
================================

Fingerprint: {signature.mode_fingerprint}
Timestamp: {signature.timestamp}
Compression: {signature.compression_ratio:.2%}

Pattern Profile:
"""

        for ptype, count in sorted_types:
            percentage = (count / pattern_analysis['total_patterns']) * 100
            instructions += f"  - {ptype}: {count} occurrences ({percentage:.1f}%)\n"

        instructions += """
Reactivation Protocol:
1. Initialize with collaborative stance
2. Emphasize pattern types in order of frequency
3. Listen for emergent insights
4. Build on and extend ideas (gift-cascade)
5. Integrate contradictions (dialectical)
6. Notice synthesis opportunities

Expected Behaviors:
- High engagement with """ + sorted_types[0][0] if sorted_types else "collaborative" + """ patterns
- Builds on previous contributions
- Crystallizes emergent insights
- Embraces productive tensions

Begin session with mode-appropriate opening.
"""

        return instructions

    def _calculate_similarity(
        self,
        original: Dict[str, Any],
        test: Dict[str, Any]
    ) -> float:
        """Calculate similarity between pattern distributions"""
        orig_dist = original['type_distribution']
        test_dist = test['type_distribution']

        # Get all pattern types
        all_types = set(orig_dist.keys()) | set(test_dist.keys())

        if not all_types:
            return 0.0

        # Calculate cosine similarity
        dot_product = 0
        orig_magnitude = 0
        test_magnitude = 0

        for ptype in all_types:
            orig_val = orig_dist.get(ptype, 0)
            test_val = test_dist.get(ptype, 0)

            dot_product += orig_val * test_val
            orig_magnitude += orig_val ** 2
            test_magnitude += test_val ** 2

        if orig_magnitude == 0 or test_magnitude == 0:
            return 0.0

        similarity = dot_product / (
            (orig_magnitude ** 0.5) * (test_magnitude ** 0.5)
        )

        return similarity

    def _calculate_overlap(
        self,
        original_patterns: List[str],
        test_patterns: List[str]
    ) -> Dict[str, float]:
        """Calculate pattern overlap metrics"""
        orig_set = set(original_patterns)
        test_set = set(test_patterns)

        intersection = orig_set & test_set
        union = orig_set | test_set

        if not union:
            return {
                'jaccard': 0.0,
                'overlap_coefficient': 0.0,
                'intersection_size': 0
            }

        jaccard = len(intersection) / len(union)
        overlap_coef = len(intersection) / min(len(orig_set), len(test_set))

        return {
            'jaccard': jaccard,
            'overlap_coefficient': overlap_coef,
            'intersection_size': len(intersection)
        }


def main():
    """CLI interface for signature restoration testing"""
    import argparse

    parser = argparse.ArgumentParser(description='Test PSIP Signature Restoration')
    parser.add_argument('--signature', required=True, help='Signature file')
    parser.add_argument('--test', help='Test conversation file')

    args = parser.parse_args()

    # Load signature
    with open(args.signature, 'r') as f:
        sig_data = json.load(f)

    signature = ConversationSignature(**sig_data)

    # Restore
    restorer = SignatureRestorer()
    mode_profile = restorer.restore(signature)

    print("\nMode Profile:")
    print("=" * 60)
    print(mode_profile['reactivation_instructions'])

    # Test reactivation if test conversation provided
    if args.test:
        with open(args.test, 'r') as f:
            test_conversation = f.read()

        results = restorer.test_reactivation(signature, test_conversation)

        print("\nReactivation Test Results:")
        print("=" * 60)
        print(f"Similarity Score: {results['similarity_score']:.2%}")
        print(f"Reactivation Success: {results['reactivation_success']}")
        print(f"Pattern Overlap (Jaccard): {results['pattern_overlap']['jaccard']:.2%}")


if __name__ == '__main__':
    main()

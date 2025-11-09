"""
PSIP Signature Validation
Ensure signature integrity and privacy
"""

from typing import Dict, Any, List
import json
from .compress import ConversationSignature


class SignatureValidator:
    """Validate PSIP signatures"""

    def __init__(self):
        self.validation_rules = {
            'compression_ratio': self._validate_compression_ratio,
            'pattern_count': self._validate_pattern_count,
            'privacy': self._validate_privacy,
            'structure': self._validate_structure,
        }

    def validate(
        self,
        signature: ConversationSignature,
        strict: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive validation

        Args:
            signature: Signature to validate
            strict: If True, all rules must pass

        Returns:
            Dict with validation results
        """
        results = {}

        for rule_name, rule_func in self.validation_rules.items():
            try:
                passed, message = rule_func(signature)
                results[rule_name] = {
                    'passed': passed,
                    'message': message
                }
            except Exception as e:
                results[rule_name] = {
                    'passed': False,
                    'message': f'Error: {str(e)}'
                }

        # Overall pass/fail
        all_passed = all(r['passed'] for r in results.values())
        any_passed = any(r['passed'] for r in results.values())

        results['overall'] = {
            'passed': all_passed if strict else any_passed,
            'strict_mode': strict
        }

        return results

    def _validate_compression_ratio(
        self,
        signature: ConversationSignature
    ) -> tuple[bool, str]:
        """Validate compression ratio meets threshold"""
        # Adaptive threshold based on original length
        original_length = signature.metadata.get('original_length', 0)

        # For very short conversations (< 500 chars), lower threshold
        if original_length < 500:
            threshold = 0.3
        # For medium conversations (500-2000 chars), medium threshold
        elif original_length < 2000:
            threshold = 0.7
        # For long conversations (> 2000 chars), high threshold
        else:
            threshold = 0.95

        if signature.compression_ratio < threshold:
            return False, f"Compression ratio {signature.compression_ratio:.2%} < {threshold:.0%} (adaptive threshold)"
        return True, f"Compression ratio {signature.compression_ratio:.2%} OK (threshold {threshold:.0%})"

    def _validate_pattern_count(
        self,
        signature: ConversationSignature
    ) -> tuple[bool, str]:
        """Validate pattern count is reasonable"""
        count = len(signature.patterns)
        if count == 0:
            return False, "No patterns extracted"
        if count > 10000:
            return False, f"Too many patterns: {count}"
        return True, f"Pattern count {count} OK"

    def _validate_privacy(
        self,
        signature: ConversationSignature
    ) -> tuple[bool, str]:
        """Validate no private content in signature"""
        # All patterns should be hashed
        for pattern in signature.patterns:
            parts = pattern.split(':')
            if len(parts) != 3:
                return False, f"Invalid pattern structure: {pattern}"

            # Check hash is properly formed
            pattern_hash = parts[2]
            if len(pattern_hash) != 8:
                return False, f"Invalid hash length: {pattern}"

            # Check hash is hex
            if not all(c in '0123456789abcdef' for c in pattern_hash):
                return False, f"Invalid hash format: {pattern}"

        return True, "Privacy check passed"

    def _validate_structure(
        self,
        signature: ConversationSignature
    ) -> tuple[bool, str]:
        """Validate signature structure"""
        # Check required fields
        if not signature.signature_hash:
            return False, "Missing signature hash"

        if not signature.mode_fingerprint:
            return False, "Missing mode fingerprint"

        if not signature.timestamp:
            return False, "Missing timestamp"

        # Check metadata
        required_metadata = ['original_length', 'pattern_count', 'preserved_patterns']
        for field in required_metadata:
            if field not in signature.metadata:
                return False, f"Missing metadata: {field}"

        return True, "Structure validation passed"


def main():
    """CLI interface for signature validation"""
    import argparse

    parser = argparse.ArgumentParser(description='Validate PSIP Signature')
    parser.add_argument('--signature', required=True, help='Signature file to validate')
    parser.add_argument('--strict', action='store_true', help='Strict validation mode')

    args = parser.parse_args()

    # Load signature
    with open(args.signature, 'r') as f:
        sig_data = json.load(f)

    signature = ConversationSignature(**sig_data)

    # Validate
    validator = SignatureValidator()
    results = validator.validate(signature, strict=args.strict)

    # Print results
    print("\nValidation Results:")
    print("=" * 60)

    for rule_name, result in results.items():
        if rule_name == 'overall':
            continue
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {rule_name}: {result['message']}")

    print("=" * 60)
    overall = results['overall']
    status = "PASSED" if overall['passed'] else "FAILED"
    print(f"\nOverall: {status} (strict={overall['strict_mode']})")


if __name__ == '__main__':
    main()

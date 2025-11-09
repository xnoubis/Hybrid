"""
Tests for PSIP compression module
"""

import pytest
from src.psip.compress import SignatureCompressor, ConversationSignature
from src.psip.validate import SignatureValidator
from src.psip.restore import SignatureRestorer


class TestSignatureCompressor:
    """Test PSIP signature compression"""

    def test_compress_basic(self):
        """Test basic compression"""
        compressor = SignatureCompressor()

        conversation = """
        This is a gift-cascade conversation where we build on each other's ideas.
        The synthesis emerges from our collaboration.
        What crystallizes here is a new understanding.
        """

        signature = compressor.compress(conversation)

        assert signature is not None
        assert isinstance(signature, ConversationSignature)
        # For short conversations, compression ratio will be lower
        assert 0 < signature.compression_ratio < 1
        assert len(signature.patterns) > 0

    def test_compress_with_patterns(self):
        """Test compression with specific patterns"""
        compressor = SignatureCompressor()

        conversation = """
        We're building on previous ideas in a gift-giving way.
        This synthesis transcends both perspectives.
        The emergent pattern reveals something new.
        """

        signature = compressor.compress(
            conversation,
            preserve_patterns=['gift-giving', 'synthesis', 'emergence']
        )

        assert len(signature.patterns) >= 3
        assert signature.metadata['preserved_patterns'] == ['gift-giving', 'synthesis', 'emergence']

    def test_validate_signature(self):
        """Test signature validation"""
        compressor = SignatureCompressor()
        validator = SignatureValidator()

        # Use a longer conversation for better compression
        conversation = """
        This is a test conversation with synthesis and emergence patterns.
        We're building on ideas in a collaborative gift-giving way.
        The synthesis transcends both perspectives beautifully.
        What emerges here is genuinely new and exciting.
        This collaborative pattern creates something beyond either of us alone.
        """ * 10  # Repeat to make it longer for better compression

        signature = compressor.compress(conversation)
        results = validator.validate(signature, strict=False)  # Use non-strict for test

        # Check that at least some validation rules pass
        assert 'privacy' in results
        assert results['privacy']['passed']
        assert 'structure' in results
        assert results['structure']['passed']

    def test_restore_signature(self):
        """Test signature restoration"""
        compressor = SignatureCompressor()
        restorer = SignatureRestorer()

        conversation = "Building on ideas, synthesis emerges, crystallizing insights."

        signature = compressor.compress(conversation)
        mode_profile = restorer.restore(signature)

        assert 'fingerprint' in mode_profile
        assert 'reactivation_instructions' in mode_profile
        assert mode_profile['fingerprint'] == signature.mode_fingerprint

    def test_privacy_preservation(self):
        """Test that no private content leaks"""
        compressor = SignatureCompressor()

        # Include "private" content
        conversation = """
        My email is user@example.com and my phone is 555-1234.
        But the synthesis of our ideas transcends personal details.
        """

        signature = compressor.compress(conversation)

        # Check that patterns are hashed
        for pattern in signature.patterns:
            assert '@example.com' not in pattern
            assert '555-1234' not in pattern
            # Should be in format type:marker:hash
            assert pattern.count(':') == 2


class TestSignatureValidator:
    """Test signature validation"""

    def test_validation_rules(self):
        """Test all validation rules"""
        compressor = SignatureCompressor()
        validator = SignatureValidator()

        conversation = "Synthesis emerges from collaborative gift-giving."
        signature = compressor.compress(conversation)

        results = validator.validate(signature, strict=False)

        assert 'compression_ratio' in results
        assert 'pattern_count' in results
        assert 'privacy' in results
        assert 'structure' in results


class TestSignatureRestorer:
    """Test signature restoration"""

    def test_pattern_analysis(self):
        """Test pattern analysis"""
        compressor = SignatureCompressor()
        restorer = SignatureRestorer()

        conversation = """
        Gift-giving builds on synthesis.
        Synthesis builds on emergence.
        Emergence builds on gift-giving.
        """

        signature = compressor.compress(conversation)
        mode_profile = restorer.restore(signature)

        analysis = mode_profile['pattern_analysis']

        assert 'type_distribution' in analysis
        assert 'total_patterns' in analysis
        assert analysis['total_patterns'] == len(signature.patterns)

    def test_reactivation_similarity(self):
        """Test reactivation similarity calculation"""
        compressor = SignatureCompressor()
        restorer = SignatureRestorer()

        original = "Synthesis emerges from gift-giving collaboration."
        test = "Collaborative gift-cascade creates emergent synthesis."

        signature = compressor.compress(original)
        results = restorer.test_reactivation(signature, test)

        assert 'similarity_score' in results
        assert 'reactivation_success' in results
        assert 0 <= results['similarity_score'] <= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

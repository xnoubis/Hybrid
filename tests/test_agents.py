"""
Tests for agent troupe system
"""

import pytest
from src.agents.troupe import (
    AgentTroupe, AgentRole, Agent,
    NegatorAgent, CrystallizerAgent, BuilderAgent, ValidatorAgent, SynthesizerAgent
)


class TestAgents:
    """Test individual agents"""

    def test_negator_agent(self):
        """Test negator agent"""
        agent = NegatorAgent()

        assert agent.role == AgentRole.NEGATOR
        assert "impossib" in agent.get_specialty().lower()

        messages = agent.process("test problem", {})
        assert len(messages) > 0
        assert all(hasattr(msg, 'from_agent') for msg in messages)

    def test_crystallizer_agent(self):
        """Test crystallizer agent"""
        agent = CrystallizerAgent()

        assert agent.role == AgentRole.CRYSTALLIZER
        assert "pattern" in agent.get_specialty().lower()

        messages = agent.process("test problem", {})
        assert len(messages) > 0

    def test_builder_agent(self):
        """Test builder agent"""
        agent = BuilderAgent()

        assert agent.role == AgentRole.BUILDER
        assert "implement" in agent.get_specialty().lower()

        messages = agent.process("test problem", {})
        assert len(messages) > 0

    def test_validator_agent(self):
        """Test validator agent"""
        agent = ValidatorAgent()

        assert agent.role == AgentRole.VALIDATOR
        assert "validat" in agent.get_specialty().lower()

        messages = agent.process("test problem", {})
        assert len(messages) > 0

    def test_synthesizer_agent(self):
        """Test synthesizer agent"""
        agent = SynthesizerAgent()

        assert agent.role == AgentRole.SYNTHESIZER
        assert "meta" in agent.get_specialty().lower()

        messages = agent.process("test problem", {})
        assert len(messages) > 0


class TestAgentTroupe:
    """Test agent troupe collaboration"""

    def test_troupe_creation(self):
        """Test creating a troupe"""
        troupe = AgentTroupe([
            AgentRole.NEGATOR,
            AgentRole.CRYSTALLIZER
        ])

        assert len(troupe.agents) == 2
        assert AgentRole.NEGATOR in troupe.agents
        assert AgentRole.CRYSTALLIZER in troupe.agents

    def test_troupe_collaboration(self):
        """Test troupe collaboration"""
        troupe = AgentTroupe([
            AgentRole.NEGATOR,
            AgentRole.CRYSTALLIZER,
            AgentRole.VALIDATOR
        ])

        results = troupe.collaborate("test problem", iterations=2)

        assert 'problem' in results
        assert 'iterations' in results
        assert results['iterations'] == 2
        assert 'agents' in results
        assert len(results['agents']) == 3
        assert 'insights' in results
        assert 'message_count' in results

    def test_full_troupe(self):
        """Test full troupe with all agents"""
        troupe = AgentTroupe([
            AgentRole.NEGATOR,
            AgentRole.CRYSTALLIZER,
            AgentRole.BUILDER,
            AgentRole.VALIDATOR,
            AgentRole.SYNTHESIZER
        ])

        results = troupe.collaborate("AI safety vs capability", iterations=1)

        assert len(troupe.agents) == 5
        assert results['message_count'] > 0

    def test_message_extraction(self):
        """Test message extraction methods"""
        troupe = AgentTroupe([AgentRole.NEGATOR, AgentRole.CRYSTALLIZER])

        results = troupe.collaborate("test", iterations=1)

        # Should have insights, questions, potentially solution
        assert isinstance(results['insights'], list)
        assert isinstance(results['questions'], list)
        assert isinstance(results['solution'], dict)


class TestAgentCommunication:
    """Test agent communication"""

    def test_message_broadcast(self):
        """Test message broadcasting"""
        troupe = AgentTroupe([
            AgentRole.NEGATOR,
            AgentRole.CRYSTALLIZER,
            AgentRole.VALIDATOR
        ])

        # Run collaboration to generate messages
        troupe.collaborate("test problem", iterations=1)

        # Agents should have received messages
        for agent in troupe.agents.values():
            # Each agent processes, others receive
            # So each should have some messages
            assert hasattr(agent, 'messages')

    def test_targeted_messages(self):
        """Test targeted messaging between agents"""
        from src.agents.troupe import AgentMessage

        agent_a = NegatorAgent()
        agent_b = CrystallizerAgent()

        message = AgentMessage(
            from_agent=AgentRole.NEGATOR,
            to_agent=AgentRole.CRYSTALLIZER,
            content="Test message",
            message_type="insight"
        )

        agent_b.receive_message(message)

        assert len(agent_b.messages) == 1
        assert agent_b.messages[0].content == "Test message"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

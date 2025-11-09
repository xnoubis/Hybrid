"""
Agent Troupe System
Specialized agents working together on dialectical problems
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


class AgentRole(Enum):
    """Agent roles in the troupe"""
    NEGATOR = "negator"
    CRYSTALLIZER = "crystallizer"
    BUILDER = "builder"
    VALIDATOR = "validator"
    SYNTHESIZER = "synthesizer"


@dataclass
class AgentMessage:
    """Message between agents"""
    from_agent: AgentRole
    to_agent: Optional[AgentRole]  # None = broadcast
    content: str
    message_type: str  # insight, question, solution, validation, etc.


class Agent:
    """Base agent class"""

    def __init__(self, role: AgentRole):
        self.role = role
        self.context: Dict[str, Any] = {}
        self.messages: List[AgentMessage] = []

    def process(self, problem: str, context: Dict[str, Any]) -> List[AgentMessage]:
        """Process problem and return messages"""
        raise NotImplementedError

    def receive_message(self, message: AgentMessage):
        """Receive message from another agent"""
        self.messages.append(message)

    def get_specialty(self) -> str:
        """Get agent's specialty description"""
        raise NotImplementedError


class NegatorAgent(Agent):
    """The Negator - Find genuine impossibilities"""

    def __init__(self):
        super().__init__(AgentRole.NEGATOR)

    def get_specialty(self) -> str:
        return "Push perspectives to extremes, find genuine impossibilities"

    def process(self, problem: str, context: Dict[str, Any]) -> List[AgentMessage]:
        """Find impossibilities and negation zones"""
        messages = []

        # Push to extremes
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content=f"What if we push {problem} to its extremes? What becomes impossible?",
            message_type="question"
        ))

        # Identify contradictions
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=AgentRole.CRYSTALLIZER,
            content=f"I see a contradiction: we need both X and Y, but they seem mutually exclusive",
            message_type="insight"
        ))

        # Map negation zone
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="The negation zone is where both perspectives are true but neither is sufficient",
            message_type="insight"
        ))

        return messages


class CrystallizerAgent(Agent):
    """The Crystallizer - Notice emergent solutions"""

    def __init__(self):
        super().__init__(AgentRole.CRYSTALLIZER)

    def get_specialty(self) -> str:
        return "Pattern recognition in impossibility gaps"

    def process(self, problem: str, context: Dict[str, Any]) -> List[AgentMessage]:
        """Crystallize solutions from patterns"""
        messages = []

        # Notice patterns
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="I notice a pattern: this looks like a synthesis opportunity",
            message_type="insight"
        ))

        # Crystallize solution
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=AgentRole.BUILDER,
            content="Solution crystallizing: we can transcend by...",
            message_type="solution"
        ))

        # Identify solution type
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="This appears to be a synthesis-type solution",
            message_type="insight"
        ))

        return messages


class BuilderAgent(Agent):
    """The Builder - Implement immediately"""

    def __init__(self):
        super().__init__(AgentRole.BUILDER)

    def get_specialty(self) -> str:
        return "Code generation, artifact creation, implementation"

    def process(self, problem: str, context: Dict[str, Any]) -> List[AgentMessage]:
        """Build prototypes and implementations"""
        messages = []

        # Create implementation
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="Building prototype implementation...",
            message_type="action"
        ))

        # Provide concrete artifacts
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=AgentRole.VALIDATOR,
            content="Prototype ready for validation",
            message_type="artifact"
        ))

        # Implementation sketch
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="Implementation plan: 1. X, 2. Y, 3. Z",
            message_type="solution"
        ))

        return messages


class ValidatorAgent(Agent):
    """The Validator - Empirical testing"""

    def __init__(self):
        super().__init__(AgentRole.VALIDATOR)

    def get_specialty(self) -> str:
        return "Metric design, experiment execution, validation"

    def process(self, problem: str, context: Dict[str, Any]) -> List[AgentMessage]:
        """Validate solutions empirically"""
        messages = []

        # Design validation criteria
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="Validation criteria: 1. Preserves both perspectives, 2. Implementable, 3. Generative",
            message_type="validation"
        ))

        # Run tests
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="Running validation tests...",
            message_type="action"
        ))

        # Report results
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=AgentRole.SYNTHESIZER,
            content="Validation results: 3/3 criteria met",
            message_type="validation"
        ))

        return messages


class SynthesizerAgent(Agent):
    """The Synthesizer - Cross-domain connection"""

    def __init__(self):
        super().__init__(AgentRole.SYNTHESIZER)

    def get_specialty(self) -> str:
        return "Meta-pattern recognition, framework integration"

    def process(self, problem: str, context: Dict[str, Any]) -> List[AgentMessage]:
        """Synthesize across domains and patterns"""
        messages = []

        # Identify meta-patterns
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="This pattern appears in other domains: healthcare, ethics, technology",
            message_type="insight"
        ))

        # Connect to frameworks
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="This relates to dialectical framework principle: sublation",
            message_type="insight"
        ))

        # Generate new questions
        messages.append(AgentMessage(
            from_agent=self.role,
            to_agent=None,
            content="New question: What other contradictions does this pattern apply to?",
            message_type="question"
        ))

        return messages


class AgentTroupe:
    """Orchestrate multiple agents working together"""

    def __init__(self, roles: List[AgentRole]):
        self.agents: Dict[AgentRole, Agent] = {}

        # Create agents based on roles
        agent_classes = {
            AgentRole.NEGATOR: NegatorAgent,
            AgentRole.CRYSTALLIZER: CrystallizerAgent,
            AgentRole.BUILDER: BuilderAgent,
            AgentRole.VALIDATOR: ValidatorAgent,
            AgentRole.SYNTHESIZER: SynthesizerAgent
        }

        for role in roles:
            if role in agent_classes:
                self.agents[role] = agent_classes[role]()

        self.messages: List[AgentMessage] = []
        self.shared_context: Dict[str, Any] = {}

    def collaborate(
        self,
        problem: str,
        iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Run collaborative session

        Args:
            problem: Problem description
            iterations: Number of iteration rounds

        Returns:
            Dict with collaboration results
        """
        print(f"\nStarting collaboration on: {problem}")
        print(f"Agents: {', '.join(a.value for a in self.agents.keys())}\n")

        all_messages = []

        for iteration in range(iterations):
            print(f"--- Iteration {iteration + 1}/{iterations} ---")

            # Each agent processes in turn
            for role, agent in self.agents.items():
                print(f"  [{role.value}] thinking...")

                # Agent processes current state
                messages = agent.process(problem, self.shared_context)

                # Broadcast messages
                for msg in messages:
                    all_messages.append(msg)
                    self._broadcast_message(msg)

                    # Print message
                    target = msg.to_agent.value if msg.to_agent else "all"
                    print(f"    -> [{target}] {msg.message_type}: {msg.content[:80]}...")

            # Update shared context
            self.shared_context['iteration'] = iteration
            self.shared_context['message_count'] = len(all_messages)

            print()

        # Compile results
        results = {
            'problem': problem,
            'iterations': iterations,
            'agents': [role.value for role in self.agents.keys()],
            'message_count': len(all_messages),
            'insights': self._extract_insights(all_messages),
            'questions': self._extract_questions(all_messages),
            'solution': self._extract_solution(all_messages)
        }

        return results

    def _broadcast_message(self, message: AgentMessage):
        """Broadcast message to appropriate agents"""
        if message.to_agent is None:
            # Broadcast to all
            for agent in self.agents.values():
                if agent.role != message.from_agent:
                    agent.receive_message(message)
        else:
            # Send to specific agent
            if message.to_agent in self.agents:
                self.agents[message.to_agent].receive_message(message)

    def _extract_insights(self, messages: List[AgentMessage]) -> List[str]:
        """Extract insights from messages"""
        return [
            msg.content
            for msg in messages
            if msg.message_type == 'insight'
        ][:5]  # Top 5

    def _extract_questions(self, messages: List[AgentMessage]) -> List[str]:
        """Extract questions from messages"""
        return [
            msg.content
            for msg in messages
            if msg.message_type == 'question'
        ][:3]  # Top 3

    def _extract_solution(self, messages: List[AgentMessage]) -> Dict[str, Any]:
        """Extract solution from messages"""
        solution_messages = [
            msg for msg in messages
            if msg.message_type == 'solution'
        ]

        if solution_messages:
            return {
                'type': 'collaborative',
                'description': solution_messages[-1].content,
                'contributors': list(set(msg.from_agent.value for msg in solution_messages))
            }

        return {}


def main():
    """Demo agent troupe"""
    # Create troupe with all agents
    troupe = AgentTroupe([
        AgentRole.NEGATOR,
        AgentRole.CRYSTALLIZER,
        AgentRole.BUILDER,
        AgentRole.VALIDATOR,
        AgentRole.SYNTHESIZER
    ])

    # Run collaboration
    results = troupe.collaborate(
        problem="AI safety vs capability",
        iterations=3
    )

    # Display results
    print("\n" + "=" * 60)
    print("Collaboration Results")
    print("=" * 60)
    print(f"\nInsights generated: {len(results['insights'])}")
    print(f"Questions raised: {len(results['questions'])}")
    print(f"Solution type: {results['solution'].get('type', 'None')}")

    print("\nTop Insights:")
    for insight in results['insights'][:3]:
        print(f"  • {insight}")


if __name__ == '__main__':
    main()

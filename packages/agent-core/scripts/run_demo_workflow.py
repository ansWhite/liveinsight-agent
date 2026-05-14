from liveinsight_core.agents.state import AgentWorkflowState
from liveinsight_core.agents.workflow import LiveInsightWorkflow
from liveinsight_core.multimodal.pipeline import MultimodalPipeline


def main() -> None:
    segments = MultimodalPipeline().parse_video("demo.mp4")
    state = AgentWorkflowState(project_id="demo", user_task="Analyze livestream and draft scripts", segments=segments)
    result = LiveInsightWorkflow().run(state)
    print(result.report)
    print("\nTrace:")
    for item in result.trace:
        print(f"- {item}")


if __name__ == "__main__":
    main()

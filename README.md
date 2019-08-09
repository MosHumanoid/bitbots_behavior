# bitbots_behavior

This is the behavior code of the RoboCup Humanoid League team Hamburg Bit-Bots.
It is divided into a behavior for the head and the body.
Both are programmed using the dynamic_stack_decider package (https://github.com/bit-bots/dynamic_stack_decider).

# TODO:
* Ask about the inverse kinematics of the head motors --> whether to do the computation inside the head node
* main.dsd does not contain KickBallStatic i.e. the robot does not kick ball --> need to talk about the low level motion implementation for msg passing
* Need to wait after the action has finished --> whether to do this part in behavior node or motion control node
* Retrieve the lua code for the FSM to add node of the the current tree
* Complete the code of nodes which only execute simple logic

# Package Usage
1. bitbots_body_behavior
2. bitbots_head_behavior
3. bitbots_blackboard
4. bitbots_stack_decider
5. bitbots_msgs
6. humanoid_league_msgs
7. bio_ik_msgs
8. bio_ik_service(in our case it may not be needed)


# Node
## Body
* Package: bitbots_body_behavior
* Name: body_behavior
* Type: body_behavior.py

### Publisher
* strategy_sender
  * topic: "strategy"
  * type: Strategy
* head_pub
  * topic: "head_mode"
  * type: HeadMode
* pathfinding_pub
  * topic:"move_base_simple/goal"
  * type: PoseStamped

### Subscriber
* About ball
  * topic: "ball_relative"
  * type: BallRelative
  * callback: blackboard.world_model.ball_callback
* About goal
  * topic: "goal_relative"
  * type: GoalRelative
  * callback: blackboard.world_model.goal_callback
* About game state
  * topic: "gamestate"
  * type: GameState
  * callback: blackboard.gamestate.gamestate_callback
* About team data
  * topic: "team_data"
  * type: TeamData
  * callback: blackboard.team_data.team_data_callback
* About pose
  * topic: "amcl_pose"
  * type: PoseWithCovarianceStamped
  * callback: blackboard.world_model.position_callback
* About robot state
  * topic: "robot_state"
  * type: RobotControlState
  * callback: blackboard.blackboard.robot_state_callback

## Head
* Package: bitbots_head_behavior
* Name: head_behavior
* Type: head_node.py
### Publisher
* position_publisher
  * topic: "/head_motor_goals"
  * type: JointCommand
* visual_compass_record_trigger
  * topic: "/visual_compass_ground_truth_trigger"
  * type: Header

### Subscriber
* About headmode
  * topic: "/head_mode"
  * type: HeadModeMsg
  * callback: blackboard.head_capsule.head_mode_callback
* About ball
  * topic: "/ball_relative"
  * type: BallRelative
  * callback: blackboard.world_model.ball_callback
* About head joints
  * topic: "/joint_states"
  * type: JointState
  * callback: blackboard.head_capsule.joint_state_callback

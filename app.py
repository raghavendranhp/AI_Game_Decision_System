import streamlit as st
import random
from game_env import TicTacToeEnv
from ai_engine import AIEngine

def initialize_session_state():
    """
    Initializes necessary variables in streamlit session state.
    """
    #check if environment exists in the session state initialize game environment and related tracking variables
    if 'env' not in st.session_state:
        st.session_state.env = TicTacToeEnv()
        st.session_state.ai_engine = AIEngine(ai_letter='O')
        st.session_state.q_engine_trained = False
        st.session_state.human_wins = 0
        st.session_state.ai_wins = 0
        st.session_state.draws = 0
        st.session_state.game_over = False

    #train the q learning model once if uninitialized simulate games to populate table properly
    if not st.session_state.q_engine_trained:
        st.session_state.ai_engine.train_q_learning(iterations=3000)
        st.session_state.q_engine_trained = True

def handle_click(i):
    """
    Handles a button click representing a user move.

    Args:
        i (int): The index of the clicked board square.
    """
    
    #verify the game is active and square available execute human player move utilizing selected position
    env = st.session_state.env
    if not st.session_state.game_over and env.board[i] == ' ':
        env.make_move(i, 'X')
        
        #check if human won or board full currently update scoreboard variables immediately
        if env.current_winner == 'X':
            st.session_state.human_wins += 1
            st.session_state.game_over = True
            return
        elif not env.empty_squares():
            st.session_state.draws += 1
            st.session_state.game_over = True
            return
            
        #trigger the ai move immediately after human turn evaluate new board conditions and conclude match if necessary
        ai_turn()

def ai_turn():
    """
    Executes the ai turn based on selected algorithm and difficulty.
    """
    
    #access environment and selected configuration parameters cleanly initialize move variable before logical evaluation blocks
    env = st.session_state.env
    ai = st.session_state.ai_engine
    algorithm = st.session_state.algorithm
    difficulty = st.session_state.difficulty
    
    #determine difficulty level routing safely handling constraints override algorithms dynamically depending upon selected difficulty
    if difficulty == "Easy":
        #execute purely random moves uniformly regardless algorithm this aligns exactly with expected easy configuration
        move = random.choice(env.available_moves())
    elif difficulty == "Medium":
        #route q learning to untrained probability parameter setting route remainder configuration safely routing toward heuristics
        if algorithm == "Q-Learning":
            move = ai.get_q_learning_move(env, is_trained=False)
        else:
            move = ai.get_heuristic_move(env)
    else:
        #route q learning utilizing fully populated table combinations override everything else utilizing optimal minimax solver
        if algorithm == "Q-Learning":
            move = ai.get_q_learning_move(env, is_trained=True)
        else:
            move = ai.get_minimax_move(env)

    #execute calculated move updating environment board sequentially check termination conditions attributing score correctly afterwards
    env.make_move(move, 'O')
    if env.current_winner == 'O':
        st.session_state.ai_wins += 1
        st.session_state.game_over = True
    elif not env.empty_squares():
        st.session_state.draws += 1
        st.session_state.game_over = True

def reset_game():
    """
    Resets the current game board to allow playing again.
    """
    
    #call environment specific reset logic method execution toggle game over boolean flag backward properly
    st.session_state.env.reset()
    st.session_state.game_over = False

def main():
    """
    Main function to render streamlit visual interface completely.
    """
    
    #configure foundational layout parameters strictly avoiding icons invoke state initialization ensuring backend capability presence
    st.set_page_config(page_title="AI Tic-Tac-Toe", layout="centered")
    initialize_session_state()

    #render main page title lacking additional visual artifacts render brief description detailing capability integration slightly
    st.title("AI-Powered Tic-Tac-Toe Decision System")
    st.markdown("Play against different artificial intelligence models utilizing algorithmic constraints.")

    #render sidebar routing parameters dropdown combination boxes persist algorithm and difficulty selections cleanly
    st.sidebar.title("Configuration Panel")
    st.session_state.algorithm = st.sidebar.selectbox("AI Algorithm", ["Minimax", "Heuristics", "Q-Learning"])
    st.session_state.difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

    #render sidebar tracked session scoreboard metrics clearly display numerical values cleanly within independent columns
    st.sidebar.markdown("---")
    st.sidebar.subheader("Session Scoreboard")
    col1, col2, col3 = st.sidebar.columns(3)
    col1.metric("Human Wins", st.session_state.human_wins)
    col2.metric("AI Wins", st.session_state.ai_wins)
    col3.metric("Draws", st.session_state.draws)

    #render interactive container managing grid visually distinct construct three corresponding row columns logically horizontally
    st.markdown("---")
    grid_container = st.container()
    
    with grid_container:
        
        #iterate vertically simulating corresponding matrix indices visually inject columns corresponding towards horizontal layout coordinates
        for row in range(3):
            cols = st.columns([1, 1, 1])
            for col in range(3):
                #calculate linear flat representation underlying numerical map assign rendering logic managing interactive visual buttons
                i = row * 3 + col
                with cols[col]:
                    st.button(
                        st.session_state.env.board[i] if st.session_state.env.board[i] != ' ' else ' ',
                        key=f"cell_{i}",
                        on_click=handle_click,
                        args=(i,),
                        use_container_width=True
                    )

    #verify concluding matches evaluating terminal status variable render concluding informational context block notifying participants
    if st.session_state.game_over:
        st.markdown("---")
        if st.session_state.env.current_winner == 'X':
            st.success("You win the game!")
        elif st.session_state.env.current_winner == 'O':
            st.error("The AI wins the game!")
        else:
            st.info("The match concludes as a draw.")
        
        #render subsequent interactive operational visual buttons cleanly invoke backend environment clearing protocol method safely
        st.button("Play Again", on_click=reset_game, use_container_width=True)

if __name__ == "__main__":
    #execute encapsulated visual representation directly upon initialization verify standalone execution script parameter logically completely
    main()

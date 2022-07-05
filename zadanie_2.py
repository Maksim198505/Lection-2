from lekciya2.game_class import GameBoard


def restart_game_dialogue():
    # Спросить пользователя, хочет ли он перезапустить игру.
    # Вернуть True если выберет yes, Вернуть False если выберет no.
    # В противном случае снова попросит выбрать yes или no.

    choice = input('Do you want to play again? Enter yes or no: ').strip().upper()
    if choice == 'YES':
        return True
    elif choice == 'NO':
        return False
    else:
        print('Enter YES or NO')
        return restart_game_dialogue()


def main():
    while True:
        new_board = GameBoard()
        new_board.start_game()
        print(new_board.draw_board())
        while True:
            row, column = new_board.current_player.select_cell(new_board)
            if not new_board.play_round(row, column):
                break
        if not restart_game_dialogue():
            break


if __name__ == '__main__':
    main()

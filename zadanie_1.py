from lekciya2.go_class import BruteForcePlanner, InputHandler


def main():
    planner = BruteForcePlanner(InputHandler.read_points())
    best_path = planner.find_best_path()
    print('Optimal path:')
    print(best_path)
    planner.draw_path_planing()


if __name__ == '__main__':
    main()

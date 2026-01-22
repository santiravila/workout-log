from controller import manager
import views


def main():
    manager.load_data()

    while True:
        views.print_menu()
        option = views.get_user_input()

        match option:
            case 1:
                views.create_session()
            case 2:
                views.consult_log(manager.get_sessions(), manager.get_routines())
            case 3:
                views.create_routine()
            case 4:
                views.consult_routines(manager.get_routines())
            case 5:
                # Workout reports
                ...
            case 6:
                manager.save_data()
                break


if __name__ == "__main__":
    main()

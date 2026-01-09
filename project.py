import views


def main():
    while True:
        views.print_menu()
        option = views.get_user_input()
        
        match option:
            case 1: views.create_session()
            case 2: views.consult_log()
            case 3: views.create_routine()
            case 4: views.consult_routines()
            case 5: break


if __name__ == "__main__":
    main()

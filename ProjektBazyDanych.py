import mysql.connector as mysql

#Lączenie z baza danych MySql
try:
    db = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'siemaeniu'
    )
    print("Successfully connected to MySQL server.")
except Exception as e:
    print(e)
    print("Could not connect to MySQL server.")

#mycursor = db.cursor()
#mycursor.execute("CREATE Database games")

#Lączenie się z bazą danych project
try:
    project = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'siemaeniu',
    database = 'project'
    )
    mycursor = project.cursor()
    print("Successfully connected to games DATABASE.")
except Exception as e:
    print(e)
    print("Could not connect to games DATABASE.")

mycursor = project.cursor()

#Funckja rejestracji i logowania użytkownika
def Register_Login():
    #Wybór opcji pomiędzy rejestracją a logowaniem
    while True:
        print("")
        print("1.Register your account")
        print("2.Login to your account")
        login_option = input("Option (number): ")
        #Rejestracja nowego użytownika podanie nazwy oraz hasla
        if login_option == "1":
            while True:
                nick_name = input(str("Type your user name: "))
                password = input(str("Type your password: "))
    
                # Sprawdzanie w bazie danych czy nie istnieje użytjownik o tej samej nazwie użytkownika
                check_query = "SELECT COUNT(*) FROM users WHERE nick_name = %s"
                mycursor.execute(check_query, (nick_name,))
                result = mycursor.fetchone()
                #Sprawdzenie czy nazwa użytkownika spełnia warunki
                if result[0] > 0:
                    print("Nick name already exists!")
                    print("Please try different nick name.")
                elif len(nick_name) > 25:
                    print("Your nick name is too long!")
                #Wprowadzenie użytkownika do bazy danych
                else:
                    query_vals = (nick_name, password)
                    mycursor.execute("INSERT INTO users (nick_name, password) VALUES (%s,%s)", query_vals)
                    project.commit()
                    print("User registered!")
                    break
        #Logowanie użytkownika do programu
        elif login_option == "2":
            print("")
            nick_name = input("Type your nick name: ")
            password = input("Type your password: ")
            #Sprawdzenie czy nazwa użytkownika == haśle użytkownika
            login_query= "SELECT * FROM users where nick_name = %s and password = %s"
            mycursor.execute(login_query, (nick_name, password))
            result = mycursor.fetchone()
            if result is None:
                print("Invalid login credentials!")
                continue
            #Zalogowanie użytkownika oraz wyciągniecię danej user_id
            else:
                print("Welcome to WeRateGames!")
                user_id = result[0]
                return user_id
        else:
            print("Wrong Option")
            continue

#Funckja ocenienia gry
def game_rating(user_id):
    #Wybór gry spośród dostępnych z tabeli games
    while True:
        rated = False
        print("")
        print("What game would you like to rate? ")
        print("")
        #Wyświetlenie gier
        mycursor.execute("SELECT * FROM games")
        for x in mycursor:
            formatted_game = f"{x[0]}: {x[1]} ({x[2]})"
            print(formatted_game)
        #Wybór gry oraz wyciągniecię danego wiersza gry z tabeli games poprzez wartość game
        game_option = input("Option (number): ")
        check_query = ("Select * from games where game_id = %s")
        mycursor.execute(check_query, (game_option,))
        game = mycursor.fetchone()
        if game != None:
            if game:
                #game_formatted = ", ".join(str(value) for value in game[1:]).replace(",", "")
                #print(game_formatted)
                game_formatted = f"{game[1]} ({game[2]})"
                print("")
                print("You chose " + game_formatted)
        else:
            print("")
            print("Wrong option")
            continue 
        
        print("")
        #Sprawdzenie czy użytkownik ocenił już gre (Nie jestem do końca pewny dlaczego wartość mycursor.fetchall() musi się tam pojawić ale jest niezbędna do działania)
        mycursor.execute("Select * from ratings where user_id = %s and game_id = %s", (user_id, game[0]))
        game_rate = mycursor.fetchone()
        mycursor.fetchall()
        #Spytanie się użytkownika czy chciałby zmienić wystawioną ocenę
        if game_rate != None:
            options = ["y", "n"]
            rate = round(game_rate[3])
            print("")
            print("You already rated " + f"{game[1]}" " for " + str(rate) + "/10")
            rating_question = input("Would you like to change your rating? (y/n): ").lower()

            while rating_question not in options:
                print("Invalid input")
                rating_question = input("Would you like to change your rating? (y/n): ").lower()
        
            if rating_question == "y":
                while True:
                    try:
                        print("")
                        user_update = int(input("How would you rate " + f"{game[1]}" + " on a scale from 1 to 10? : "))
                
                        if user_update not in range(0, 11):
                            print("Number should be in the range of 1 to 10, please try again")
                        else:
                            print("")
                            print("You rated " + f"{game[1]}" + " as a " + str(user_update) + "/10 game!")
                            print("Thanks for your opinion!")
                            print("")
                            #Aktualizacja poprzedniej oceny w tabeli ratings
                            mycursor.execute("UPDATE ratings SET game_rate = %s WHERE user_id = %s AND game_id = %s", (user_update, user_id, game[0]))
                            project.commit()
                            rated = True
                            break
                    except ValueError:
                        print("Invalid input, please try again")
            elif rating_question == "n":
                break
        #Wprowadzenie pierwszej oceny do tabeli ratings
        elif game_rate == None:
            while True:
                try:
                    print("")
                    user_rating = int(input("How would you rate " + f"{game[1]}" + " in scale from 1 to 10? : "))
                    if user_rating not in range(0, 11):
                        print("Number should be in range of 1 to 10 please try again")
                    else:
                        print("")
                        print("You rated " + f"{game[1]}" + " as a " + str(user_rating) + "/10 game!")
                        print("Thanks for your opinion!")
                        print("")
                        mycursor.execute("INSERT INTO ratings (user_id, game_id, game_rate) values (%s,%s,%s)", (user_id, game[0], user_rating))
                        project.commit()
                        rated = True
                        break
                except ValueError:
                    print("Invalid input, please try again")
        if rated == True:
            break
        
#Funcka wprowadzenia czasu przejścia gry
def game_time(user_id):
    #Wybór gry spośród dostępnych z tabeli games
    while True:
        print("")
        print("What game would you like to choose? ")
        #Wyświetlenie gier z tabeli games
        mycursor.execute("SELECT * FROM games")
        for x in mycursor:
            formatted_game = f"{x[0]}: {x[1]} ({x[2]})"
            print(formatted_game)
        #Wybór gry oraz wyciągniecię danego wiersza gry z tabeli games poprzez wartość game
        game_option = input("Option (number): ")
        check_query = ("Select * from games where game_id = %s")
        mycursor.execute(check_query, (game_option,))
        game = mycursor.fetchone()
        if game != None:
            if game:
                #game_formatted = ", ".join(str(value) for value in game[1:]).replace(",", "")
                #print(game_formatted)
                game_formatted = f"{game[1]} ({game[2]})"
                print("You chose " + game_formatted)
        else:
            print("Wrong option")
            continue 
        #Sprawdzenie czy użytkownik podał już czas, w którym przeszedł grę
        mycursor.execute("Select * from times where user_id = %s and game_id =%s ", (user_id, game[0]))
        user_time = mycursor.fetchone()
        mycursor.fetchall()
        #Spytanie się użytkownika czy chciałby zmienić czas przejścia gry
        if user_time != None:
            options = ["y", "n"]
            rate = round(user_time[3])
            print("")
            print("You already shared with us how long did it take for you to beat " + f"{game[1]}" + " (" + str(rate) + " hours)")
            time_question = input("Would you like to change your time? (y/n): ").lower()

            while time_question not in options:
                print("Invalid input")
                time_question = input("Would you like to change your rating? (y/n): ").lower()
        
            if time_question == "y":
                while True:
                    try:
                        print("")
                        user_time = int(input("How long did it take to beat " + f"{game[1]}?: "))
                        print("(Type only hours not minutes and seconds, thanks!)")
                        print("")
                        print("It took you " + str(user_time) + " to beat " + f"{game[1]}" )
                        print("Thanks for sharing it with us!")
                        print("")
                        #Aktualizacja czasu przejścia gry
                        mycursor.execute("UPDATE times SET time_played = %s WHERE user_id = %s AND game_id = %s", (user_time, user_id, game[0]))
                        project.commit()
                        rated = True
                        break
                    except ValueError:
                        print("Invalid input, please try again")
                        continue
            elif time_question == "n":
                print("")
                break
        #Wprowadzenie po raz pierwszy czasu w jakim użytkownik przeszedł grę
        elif user_time == None:
            while True:
                try:
                    print("")
                    user_time = int(input("How long did it take to beat " + f"{game[1]}?: "))
                    print("(Type only hours not minutes and seconds, thanks!)")
                    print("")
                    print("It took you " + str(user_time) + " hours to beat " + f"{game[1]}" )
                    print("Thanks for sharing it with us!")
                    print("")
                    mycursor.execute("Insert into times (time_played, user_id, game_id) values (%s, %s, %s)", (user_time, user_id, game[0]))
                    project.commit()
                    rated = True
                    break
                except ValueError:
                    print("Invalid input, please try again")
                    continue
                
        if rated == True:
            break

#Funcka, która wyświetla dane na temat gier  
def games_informations(user_id):
    #Wybór opcji
    while True:
        print("")
        print("1.Show game ratings!")
        print("2.How long did take to beat the game? ")
        print("3.Leave")
        user_option = input("Option (number): ")
        #Pokazanie średniej ocen graczy
        if user_option == "1":
            while True:
                print("")
                print("What game would you like to choose? ")
                #Wyświetlenie gier
                mycursor.execute("SELECT * FROM games")
                for x in mycursor:
                    formatted_game = f"{x[0]}: {x[1]} ({x[2]})"
                    print(formatted_game)
                game_option = input("Option (number): ")
                #Wybór gry oraz wyciągniecię danego wiersza gry z tabeli games poprzez wartość game
                check_query = ("Select * from games where game_id = %s")
                mycursor.execute(check_query, (game_option,))
                game = mycursor.fetchone()

                print("")
                #Wyciągniecie informacji o tym czy zalogowany użytkownik ocenił daną grę
                mycursor.execute("Select game_rate from ratings where game_id = %s AND user_id = %s ", (game[0], user_id))
                try:
                    personal_rating = mycursor.fetchone()[0]
                    personal_rating = round(personal_rating)
                except TypeError:
                    pass
                
                #Wyciągnięcie infromacji o ilości graczy, którzy ocenili gre
                mycursor.execute("SELECT COUNT(*) FROM ratings WHERE game_id = %s", (game[0],))
                users_count_rating = mycursor.fetchone()[0]

                #Sprawdzamy czy istnieją jacykolwiek użytkownicy którzy ocenili gre jeśli tak sumujemy ich wyniki
                if users_count_rating > 0:
                    mycursor.execute("SELECT SUM(game_rate) FROM ratings WHERE game_id = %s", (game[0],))
                    total_rating = mycursor.fetchone()[0]
                    #Dzielenie wynikiów graczy przez ilość uzytkowników, którzy ocenili grę
                    average_rating = total_rating / users_count_rating
                    print("")
                    print("Average user rating:", round(average_rating, 1), "based on " + str(users_count_rating) +" ratings")
                    print()
                    #Wyświetlenie własnej oceny
                    try:
                        print("You rated this game as " + str(personal_rating) + "/10 game")
                        break
                    #Jej brak lapiemy przez except UnboundLocalErro aby uniknąć błedu
                    except UnboundLocalError:
                        print("")
                        print("You still didn't share with us your opinion about this game or didn't play it. What are you waiting for?!")
                        break
                else:
                    print("No ratings available for this game.")
                    break
        #Pokazanie średniego czasu przejścia gry
        elif user_option == "2":
            while True:
                print("")
                print("What game would you like to choose? ")
                #Wyświetlenie gier
                mycursor.execute("SELECT * FROM games")
                for x in mycursor:
                    formatted_game = f"{x[0]}: {x[1]} ({x[2]})"
                    print(formatted_game)
                game_option = input("Option (number): ")
                #Wybór gry oraz wyciągniecię danego wiersza gry z tabeli games poprzez wartość game
                check_query = ("Select * from games where game_id = %s")
                mycursor.execute(check_query, (game_option,))
                game = mycursor.fetchone()

                print("")
                #Wyciągniecie informacji o tym czy zalogowany użytkownik podał czas w którym przeszedł grę
                mycursor.execute("Select time_played from times where game_id = %s AND user_id = %s ", (game[0], user_id))
                try:
                    personal_time = mycursor.fetchone()[0]
                except TypeError:
                    pass
                
                #Wyciągnięcie infromacji o ilości graczy, którzy podali czas w jakim przeszli grę 
                mycursor.execute("Select COUNT(*) from times where game_id = %s", (game[0],))
                users_count_time = mycursor.fetchone()[0]

                #Sprawdzamy czy istnieją jacykolwiek użytkownicy, którzy podali czas w jakim przeszli grę, jeśli tak sumujemy ich wyniki
                if users_count_time > 0:
                    mycursor.execute("Select SUM(time_played) from times where game_id = %s ", (game[0],))
                    user_times = mycursor.fetchone()[0]
                    #Dzielenie wynikiów graczy przez ilość uzytkowników, którzy podali czas w jakim przeszli grę 
                    average_time_played = user_times/users_count_time
                    average_time_played = round(average_time_played) 
                    
                    print("")
                    print("It takes " + str(average_time_played) + " hours to complete the " + str(game[1]) + " based on", users_count_time, "users answers")
                    print("")
                    print("")
                    #Wyświetlenie własnego wyniki
                    try:
                        print("Your personal time is", personal_time, "hours!" )
                        print("")
                    #Jego brak lapiemy przez except UnboundLocalErro aby uniknąć błedu
                    except UnboundLocalError:
                        print("")
                        print("You still didn't share with us your time about this game or didn't play it. What are you waiting for?!")
                        break
                else:
                    print("No data available for this game.")
                    break
        #Wyjście z loopa
        elif user_option == "3": 
            print("")
            break
        else:
            print("")
            print("Wrong option")


#Głowna funkca programu, która łączy wszystko razem
def main():
    print("")
    print("Welcome to WeRateGames! Here you can rate your favorite games and share how long did it take to beat it!")
    print("") 
    #Rejestracja lub logowanie użytkownika
    user_id = Register_Login()
    #Wyświetlenie opcji
    while True:
        print("1.Rate your favorites games!")
        print("2.How long did it take ? Share with us how long did u play your games!")
        print("3.Show games informations!")
        print("4.Logout")
        user_option = input(str("Option (number): "))
        if user_option == "1":
            #Funcka oceny gry
            game_rating(user_id)
        if user_option == "2":
            #Funkcja podania czasu w jakim użytkownik przeszedl grę
            game_time(user_id)
        if user_option == "3":
            #Funcka wyświetlająca informacje o grach
            games_informations(user_id)
        if user_option == "4":
            #Wyjście z programu
            print("")
            print("Visit us again! ")
            #Wyjście z bazy danych MySql
            try:
                db.close()
                print("Successfuly dissconnected with Database")
            except Exception as e:
                print(e)
                print("Could not disconnect with Database")
            quit()

#Inicjacja programu
main()
    






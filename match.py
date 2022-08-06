class Match:

    def case(self, inputCommand):
        default = "default()"
        return getattr(self, 'case_' + str(inputCommand), lambda: default)()

    def case_help(self):
        return "print_help()"

    def case_login(self):
        return "login()"

    def case_getpass(self):
        return "getpass()"

    def case_setpass(self):
        return "setpass()"

    def case_quit(self):
        return "quit()"

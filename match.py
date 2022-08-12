class Match:

    def case(self, inputCommand):
        default = "default()"
        return getattr(self, 'case_' + str(inputCommand), lambda: default)()

    def case_help(self):
        return "print_help()"

    def case_login(self):
        return "login()"

    def case_getacc(self):
        return "getacc()"

    def case_setacc(self):
        return "setacc()"

    def case_listacc(self):
        return "listacc()"

    def case_quit(self):
        return "quit()"

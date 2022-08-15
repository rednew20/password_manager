class Match:

    def case(self, inputCommand):
        default = "default()"
        return getattr(self, 'case_' + str(inputCommand), lambda: default)()

    def case_help(self):
        return "print_help()"

    def case_login(self):
        return "login()"

    def case_recover(self):
        return "recover()"

    def case_getacc(self):
        return "getacc()"

    def case_addacc(self):
        return "addacc()"

    def case_updacc(self):
        return "updacc()"

    def case_listacc(self):
        return "listacc()"

    def case_delacc(self):
        return "delacc()"

    def case_quit(self):
        return "quit()"

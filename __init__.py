from mycroft import MycroftSkill, intent_file_handler


class Robomove(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('robomove.intent')
    def handle_robomove(self, message):
        self.speak_dialog('robomove')


def create_skill():
    return Robomove()

